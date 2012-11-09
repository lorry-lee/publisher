from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.sites.models import Site, RequestSite
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from publisher.apps.post.models import Profile, LevelInfo

# Create your views here.

def register(request, redirect_field_name=REDIRECT_FIELD_NAME,
          user_creation_form=UserCreationForm):
    """Displays the user creation form and handles the create action."""

    redirect_to = request.REQUEST.get(redirect_field_name, '')

    if request.method == "POST":
        form = user_creation_form(data=request.POST)
        if form.is_valid():
            if not redirect_to or ' ' in redirect_to:
                redirect_to = settings.LOGIN_REDIRECT_URL

            # Heavier security check -- redirects to http://example.com should
            # not be allowed, but things like /view/?param=http://example.com
            # should be allowed. This regex checks if there is a '//' *before* a
            # question mark.
            elif '//' in redirect_to and re.match(r'[^\?]*//', redirect_to):
                    redirect_to = settings.LOGIN_REDIRECT_URL

            # Save the user
            new_user = form.save()
            profile = Profile(user=new_user, is_boy=True, level=LevelInfo.objects.order_by('-exp_required')[0])
            profile.save()

            new_user.backend='django.contrib.auth.backends.ModelBackend'
            login(request, new_user)

            return HttpResponseRedirect(redirect_to)
    else:
        form = user_creation_form(request)

    if Site._meta.installed:
        current_site = Site.objects.get_current()
    else:
        current_site = RequestSite(request)

    return render_to_response('auth/register.html', {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }, context_instance=RequestContext(request))

def findpassword(request):
    return render_to_response('auth/findpassword.html', {}, context_instance=RequestContext(request))

# def password_reset(request, password_reset_form=PasswordResetForm):
    # """Reset the user's password by email"""
