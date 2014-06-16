from django.conf.urls import patterns, include, url
from fms.views import *

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'archi.views.home', name='home'),
    # url(r'^archi/', include('archi.foo.urls')),

    url(r'^login/', login),
    #url(r'^home/', home),
    url(r'^error/', error),
    url(r'^issue-books/', issue_books),
    url(r'^book_issued_slip/(?P<issue_id>\d+)/', book_issued_slip),
    url(r'^issued-person/search/', issued_persons_search),
    url(r'^submit-books/', submit_books),
    url(r'^public/book-search/', public_book_search),
    url(r'^books-search/', search_books),
    url(r'^book-search/book-data/', get_book_data),
    url(r'^book-list/', books_list),
    url(r'^get_book_issued_data/', get_book_issued_data),
    url(r'^list-all-book-issues/', list_book_issues),

    #url(r'^google-login/$', 'django_openid_auth.views.login_begin', name='openid-login'),
    #url(r'^login-complete/$', 'django_openid_auth.views.login_complete', name='openid-complete'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/fms/login/',}, name='logout'),
    #url(r'', include('social_auth.urls')),

)

