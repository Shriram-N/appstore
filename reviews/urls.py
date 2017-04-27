from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /wine/
    url(r'^marketapp$', views.marketapp_list, name='marketapp_list'),
    # ex: /wine/5/
    url(r'^marketapp/(?P<marketapp_id>[0-9]+)/$', views.marketapp_detail, name='marketapp_detail'),
    url(r'^marketapp/(?P<marketapp_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    url(r'^review/user/(?P<username>\w+)/$', views.user_review_list, name='user_review_list'),
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
]
