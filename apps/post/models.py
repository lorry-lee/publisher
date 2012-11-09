from django.db.models import *
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from publisher.apps.fckeditor.fields import RichTextField
from photologue.models import ImageModel
from django.http import Http404
from django.shortcuts import get_list_or_404

# Create your models here.

class PostType(Model):
    name = CharField(max_length=32)

    def __unicode__(self):
        return self.name

class ProductType(Model):
    name = CharField(max_length=32)

    def __unicode__(self):
        return self.name

class Publisher(Model):
    has_publish = BooleanField(default=False)
    publish_url = CharField(max_length=256, default="")

class Post(Model):
    "Post in home page"
    user = ForeignKey(User,default=None,null=True,blank=True)
    title = CharField(max_length=200)
    category = CharField(max_length=200, default='')
    type = IntegerField()
    post_type = ForeignKey(PostType,default=None,null=True,blank=True)
    product_type = ForeignKey(ProductType,default=None,null=True,blank=True)
    pic_or_flash = RichTextField(default='')
    headline_pic = RichTextField(default='')
    preview = RichTextField(default='')
    content = RichTextField()
    is_public = BooleanField(default=False)
    need_roll = BooleanField(default=False)
    pub_date = DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.title

    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()

    def have_voted(self, ip_addr):
        have_voted = True
        have_neg_voted = True
        this_time = datetime.now()

        votes = self.vote_set.filter(ip=ip_addr).order_by('-vote_date')
        if votes.count() is 0:
            have_voted = False
        elif abs(votes[0].vote_date - this_time) > timedelta(hours=24):
            have_voted = False
        negvotes = self.negvote_set.filter(ip=ip_addr).order_by('-negvote_date')
        if negvotes.count() is 0:
            have_neg_voted = False
        elif abs(negvotes[0].negvote_date - this_time) > timedelta(hours=24):
            have_neg_voted = False
        return (have_voted or have_neg_voted)

class Vote(Model):
    "Votes for post"
    post = ForeignKey(Post)
    ip = CharField(max_length=64)
    vote_date = DateTimeField(_("vote"),default=datetime.now)

class NegVote(Model):
    "NegVotes for post"
    post = ForeignKey(Post)
    ip = CharField(max_length=64)
    negvote_date = DateTimeField(_("negvoted"),default=datetime.now)

class PostImage(ImageModel):
    user = ForeignKey(User)
    upload_date = DateTimeField(_("upload_date"),default=datetime.now)

class Reply(Model):
    "Post's Reply"
    user = ForeignKey(User, default=None,null=True,blank=True)
    content = RichTextField(_("Content"))
    is_public = BooleanField(_('is_public'),default='True')
    post = ForeignKey(Post)
    parent = ForeignKey('self',related_name='children',default=None,null=True,blank=True)
    created = DateTimeField(_("created"),default=datetime.now())
    pub_date = DateTimeField(_("pub_date"),default=datetime.now)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        return self.content

    def to_dict(self):
        result = {}
        if self.user != None:
            result['user'] = self.user.__unicode__()
        else:
            result['user'] = 'anonymous'
        result['content'] = self.content
        result['created'] = str(self.created)
        return result

class LevelInfo(Model):
    "The level information relate to experience that define the available behavior of user"
    exp_required = IntegerField(_('experience required'))
    level = IntegerField(_('level'))
    level_name = TextField(_('level name'), max_length=64)
    max_input_post = IntegerField(_('max input post'))
    max_input_reply = IntegerField(_('max input reply'))

class Profile(Model):
    "User's extend profile"
    user = OneToOneField(User)
    level = ForeignKey(LevelInfo)
    is_boy = BooleanField(_('sex'),default='True')
    cur_exp = IntegerField(_('experience'),default=0)

    def refresh_level(self):
        post_exp = 5
        reply_exp = 1
        self.cur_exp = self.user.post_set.filter(is_public=True).count() * post_exp
        self.cur_exp += self.user.reply_set.filter(is_public=True).count() * reply_exp
        self.level = LevelInfo.objects.filter(exp_required__lte=self.cur_exp).order_by('exp_required')[0]
        self.save()
