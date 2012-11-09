from django.conf.urls.defaults import *

urlpatterns = patterns('',
    # Make /auth/ as index
    (r'^$', 'publisher.apps.post.views.index'),

    # authorization urls
    (r'^login/', 'django.contrib.auth.views.login', {'template_name': 'auth/login.html'}),
    (r'^logout/', 'django.contrib.auth.views.logout_then_login'),
    # (r'^register/', 'apps.auth.views.register'),

    # for reset password
    (r'^password_reset/$', 'django.contrib.auth.views.password_reset'),
    (r'^password_reset_done/$', 'django.contrib.auth.views.password_reset_done'),
    (r'^password_reset_confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    (r'^password_reset_complete/$', 'django.contrib.auth.views.password_reset_complete'),
    (r'^password_change/$', 'django.contrib.auth.views.password_change'),
    (r'^password_change_done/$', 'django.contrib.auth.views.password_change_done'),
)
