from publisher.apps.post.models import *
from django.template import Context, loader
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.http import Http404
from django.core.paginator import Paginator
from datetime import datetime
from django.views.static import serve
from django.forms.models import model_to_dict
from publisher.apps import json_response
from publisher.apps.post import scan_picture_url, html_to_text
from photologue.models import Gallery, Photo

# Create your views here.

def index(request, post_type=u'0', page_num=1):
    if request.user.is_authenticated():
        try:
            request.user.profile.refresh_level()
        except:
            print "Warning, user refresh level failed!"
    try:
        all_objects = Post.objects.filter(is_public=True).order_by('-pub_date')
        if post_type != u'0':
            all_objects = all_objects.filter(post_type=post_type)
        paginator = Paginator(all_objects, 10)
        page = paginator.page(page_num)
        latest_post_list = page.object_list
        post_type_list = PostType.objects.all()
    except:
        raise Http404
    return render_to_response('post/index.html', locals(), context_instance=RequestContext(request))

def get_publish_info(request):
    publisher = Publisher.objects.get_or_create(id=1)[0]
    return json_response(dict(has_publish=publisher.has_publish, publish_url=settings.INSTANCE_URL + publisher.publish_url))

def post_type_list(request):
    post_types = PostType.objects.all()
    return json_response(dict(post_types=[model_to_dict(i) for i in post_types]))

def product_type_list(request):
    product_types = ProductType.objects.all()
    return json_response(dict(product_types=[model_to_dict(i) for i in product_types]))

def get_post_list_by_type(type, page_num, is_product):
    all_objects = Post.objects.filter(is_public=True).order_by('-pub_date')
    if is_product:
        product_type = ProductType.objects.get(pk=type)
        all_objects = all_objects.filter(product_type=product_type)
    else:
        post_type = PostType.objects.get(pk=type)
        all_objects = all_objects.filter(post_type=post_type)
    paginator = Paginator(all_objects, 10)
    page = paginator.page(page_num)
    result = posts_to_dict(page.object_list, True)
    result['num_pages'] = paginator.num_pages
    return json_response(result)

def posts_to_dict(post_list, is_preview):
    result = {}
    posts = []
    for post in post_list:
        post_dict = {}
        post_dict['post_id'] = post.pk
        if is_preview:
            post_dict['picture'] = scan_picture_url(post.pic_or_flash)
        else:
            post_dict['picture'] = scan_picture_url(post.headline_pic)
        post_dict['preview'] = html_to_text(post.preview)
        post_dict['reply_count'] = post.reply_set.count()
        post_dict['post_url'] = settings.INSTANCE_URL + '/post/' + str(post.pk) + '/detail/'
        post_dict['title'] = post.title
        posts.append(post_dict)
    result['posts'] = posts
    return result

def post_list(request, post_type, page_num=1):
    return get_post_list_by_type(post_type, page_num, False)

def product_list(request, product_type, page_num=1):
    return get_post_list_by_type(product_type, page_num, True)

def rolling_post(request, post_type):
    post_list = Post.objects.filter(is_public=True, post_type=post_type, need_roll=True).order_by('-pub_date')[0:3]
    return json_response(posts_to_dict(post_list, False))

def gallery_list(request, page_num=1):
    all_objects = Gallery.objects.order_by('-date_added')
    paginator = Paginator(all_objects, 10)
    page = paginator.page(page_num)
    object_list = page.object_list
    result = {}
    objects = []
    for obj in object_list:
        object_dict = {}
        object_dict['id'] = obj.pk
        object_dict['title'] = obj.title
        object_dict['photo_count'] = obj.photo_count()
        object_dict['sample_url'] = obj.latest(1)[0].image.url
        objects.append(object_dict)
    result['galleries'] = objects
    result['num_pages'] = paginator.num_pages
    return json_response(result)

def photo_list(request, gallery_id):
    gallery = Gallery.objects.get(pk=gallery_id)
    object_list = gallery.photos.filter(is_public=True).order_by('-date_added')
    result = {}
    objects = []
    for obj in object_list:
        object_dict = {}
        object_dict['id'] = obj.pk
        object_dict['url'] = obj.image.url
        object_dict['name'] = obj.title
        object_dict['link'] = settings.INSTANCE_URL
        objects.append(object_dict)
    result['photos'] = objects
    return json_response(result)

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id, is_public=True)
    return json_response(dict(title=post.title, pub_date=str(post.pub_date), content=post.content, reply_count=post.reply_set.count()))

def get_user_name(user):
    nickname = 'unknown_user'
    if user:
        nickname = user.username
        #if user.profile.nickname:
        #    nickname = user.profile.nickname
    return nickname

def get_head_url(user):
    url = settings.INSTANCE_URL + "/pic/head/missing.png"
    #if user:
    #    if user.profile.head:
    #        url = user.profile.head.get_thumbnail_url()
    return url

def post_reply(request, post_id, page_id):
    post = Post.objects.get(pk=post_id)
    all_reply = post.reply_set.filter(is_public=True).order_by('-pub_date')
    paginator = Paginator(all_reply, 10)
    page = paginator.page(page_id)
    reply_list = page.object_list

    replies = []
    # Store the replies and it's references into json object
    for reply in reply_list:
        # Store all reference reply first
        parent = reply.parent
        parents = []
        while parent != None:
            parent_dict = {}
            parent_dict['parent_id'] = parent.pk
            parent_dict['user'] = get_user_name(parent.user)
            parent_dict['head'] = get_head_url(parent.user)
            parent_dict['content'] = parent.content
            parent_dict['pub_date'] = parent.pub_date.strftime("%Y-%m-%d %H:%M")
            parents.append(parent_dict)
            parent = parent.parent

        reply_dict = {}
        reply_dict['parents'] = parents
        reply_dict['reply_id'] = reply.pk
        reply_dict['user'] = get_user_name(reply.user)
        reply_dict['head'] = get_head_url(reply.user)
        reply_dict['content'] = html_to_text(reply.content)
        reply_dict['pub_date'] = reply.pub_date.strftime("%Y-%m-%d %H:%M")
        replies.append(reply_dict)

    return json_response(dict(replies=replies, num_pages=paginator.num_pages))

def show_reply(request, post_id, page_id=-1):
    response_dict = {}
    post = get_object_or_404(Post, pk=post_id)

    # Get the reply list need to show
    all_reply = post.reply_set.filter(is_public=True).order_by('pub_date')
    reply_list = all_reply
    if page_id != -1:
        paginator = Paginator(all_reply, 10)
        page = paginator.page(page_id)
        reply_list = page.object_list

    # Store the replies and it's references into json object
    i = 0
    for reply in reply_list:
        # Store all reference reply first
        ref_reply = reply.parent
        reply_references = {}
        j = 0
        while ref_reply != None:
            ref_reply_content = {
                    'parent_id' : 'ref_reply_%d%d' % (i , j),
                    'user' : get_user_name(ref_reply.user),
                    'head' : get_head_url(ref_reply.user),
                    'content' : html_to_text(ref_reply.content),
                    'pub_date': ref_reply.pub_date.strftime("%Y-%m-%d %H:%M")}
            reply_references.update({'parent_%d' % j : ref_reply_content})
            ref_reply = ref_reply.parent
            j = j + 1

        # Store the current reply
        reply_content = {
                'reply_ref_count': j,
                'reply_index': 'reply_%d' % i,
                'reply_id': reply.id,
                'user' : get_user_name(reply.user),
                'head' : get_head_url(reply.user),
                'content' : html_to_text(reply.content),
                'ref_reply' : reply_references,
                'pub_date': reply.pub_date.strftime("%Y-%m-%d %H:%M")}

        response_dict.update({'reply_%d' % i : reply_content})
        i = i + 1
    response_dict.update({'reply_count' : reply_list.count()})
    return json_response(response_dict)

def submit_reply(request):
    result = 200
    try:
        parent_reply = None
        if request.POST.has_key('parent'):
            parent_reply = Reply.objects.get(pk=request.POST['parent'])
        reply = Reply(content=request.POST['content'], is_public=True, post=get_object_or_404(Post, pk=request.POST['post_id']), parent=parent_reply)
        if request.user != None and request.user.is_authenticated():
            reply.user=request.user
        reply.save()
    except:
        result = 404
    #return dict(result=result)
    return json_response(dict(result=result))

@login_required
def submitpost(request):
    return render_to_response('post/submitpost.html', {}, context_instance=RequestContext(request))

@login_required
def browsegallery(request, page_id=1):
    try:
        all_image = PostImage.objects.all().order_by('-upload_date')
        paginator = Paginator(all_image, 50)
        page = paginator.page(page_id)
        post_image_list = page.object_list
    except:
        raise Http404
    return render_to_response('post/gallery.html', locals(), context_instance=RequestContext(request))

@login_required
def uploadtogallery(request):
    if request.method == 'POST':
        try:
            f = request.FILES['image']
        except:
            raise Http404
        current_date = datetime.now()
        storepath = 'photologue/photos/' + request.user.username + '/' + current_date.strftime("%Y.%m.%d") + '/' + f.name
        # Save the image on the disk
        default_storage.save(storepath, f)
        # Create the thumbnails by thumbnail sizes
        post_image = PostImage(image=storepath, user=request.user, upload_date=current_date)
        post_image.save()
    return HttpResponseRedirect(reverse('publisher.apps.post.views.browsegallery', args=()))

def submitresult(request):
    submit_user = None
    if request.user.is_authenticated():
        submit_user = request.user
    post = Post(user=submit_user, title=request.POST['title'], type=request.POST['type'], pic_or_flash=request.POST['pic_or_flash'], preview=request.POST['preview'], content=request.POST['content'], is_public=False)
    post.save()
    return HttpResponseRedirect(reverse('publisher.apps.post.views.results', args=(post.id,)))

def results(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render_to_response('post/results.html', {'post': post}, context_instance=RequestContext(request))

def update_score_dict(post):
    response_dict = {}
    response_dict.update({'post_id' : post.id})
    response_dict.update({'vote_num' : post.vote_set.all().count()})
    response_dict.update({'neg_vote_num' : post.negvote_set.all().count()})
    return response_dict

def vote(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    if not p.have_voted(request.META['REMOTE_ADDR']):
        vote = Vote(post = p, ip = request.META['REMOTE_ADDR'])
        vote.save()
        p.vote_set.add(vote)
        p.save()
    return json_response(update_score_dict(p))

def neg_vote(request, post_id):
    p = get_object_or_404(Post, pk=post_id)
    if not p.have_voted(request.META['REMOTE_ADDR']):
        negvote = NegVote(post = p, ip = request.META['REMOTE_ADDR'])
        negvote.save()
        p.negvote_set.add(negvote)
        p.save()
    return json_response(update_score_dict(p))

def detail(request, post_id, page_id=1):
    try:
        post = get_object_or_404(Post, pk=post_id, is_public=True)
        all_reply = post.reply_set.filter(is_public=True).order_by('-pub_date')
        paginator = Paginator(all_reply, 10)
        page = paginator.page(page_id)
        reply_list = page.object_list
    except:
        raise Http404
    return render_to_response('post/detail.html', locals(), context_instance=RequestContext(request))

def reply(request, post_id):
    redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '')
    parent_reply = None
    try:
        parent_reply = get_object_or_404(Reply, pk=request.POST['parent'])
    except:
        print "ignore the reply no parent..."

    try:
        reply = Reply(content=request.POST['content'], is_public=True, post=get_object_or_404(Post, pk=post_id), parent=parent_reply)
        if request.user.is_authenticated():
            reply.user=request.user
        reply.save()

    except (KeyError, Post.DoesNotExist):
        # Redisplay the index
        return HttpResponseRedirect(reverse('publisher.apps.post.views.index', args=()))
    else:
        return HttpResponseRedirect(redirect_to)

def replyresult(request, post_id):
    reply = get_object_or_404(Reply, pk=post_id)
    return render_to_response('post/replyresult.html', {'reply': reply}, context_instance=RequestContext(request))

def test(request, path, document_root):
    lower_path = path.lower()
    return serve(request, path=lower_path, document_root=document_root)

