from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'archi.views.home', name='home'),
    # url(r'^archi/', include('archi.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fms/', include('fms.urls')),
)


from manasaram.settings import DEBUG
if DEBUG:
	urlpatterns += patterns('', 
      (r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': 'static'}),

		(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': 'media'}
    ),)

