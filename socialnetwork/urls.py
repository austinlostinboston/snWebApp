from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'socialnetwork.views.frontPage', name="home"),
    url(r'^login$', 'django.contrib.auth.views.login', {'template_name':'socialnetwork/login.html'}, name='login'),
    url(r'^register$', 'socialnetwork.views.register', name='register'),
    url(r'^frontPage$', 'socialnetwork.views.frontPage', name="frontPage"),
    url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name='logout'),
    url(r'^squeak$', 'socialnetwork.views.squeak',name="squeak"),
    url(r'^account/(?P<account>\S+)$', 'socialnetwork.views.profile', name="profile"),
    url(r'^edit_profile$', 'socialnetwork.views.edit_profile',name="edit_profile"),
    url(r'^photo/(?P<account>\S+)$', 'socialnetwork.views.get_photo', name='photo'),
    url(r'^follow/(?P<account>\S+)$', 'socialnetwork.views.follow', name="follow"),
    url(r'^get-posts-json$', 'socialnetwork.views.get_posts_json'),
    url(r'^get-posts-xml$', 'socialnetwork.views.get_posts_xml'),
    url(r'^comment/(?P<post_id>\d+)$', 'socialnetwork.views.comment',name="comment"),
    url(r'^register/confirm/(?P<username>[a-zA-Z0-9_@\+\-]+)/(?P<token>[a-z0-9\-]+)$', 'socialnetwork.views.confirm_registration', name='confirm'),
)