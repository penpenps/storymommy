from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.activity, name='activity'),
    url(r'^register/', views.register_activity, name='register_activity'),
    url(r'^register_list/(?P<activity_id>[\w\-]+)/', views.activity_register_list, name='activity_register_list'),
    url(r'^load_activity_list', views.load_activity_list, name='load_activity_list'),
    url(r'^load_register_list/(?P<activity_id>[\w\-]+)/', views.load_activity_register_list, name='load_activity_register_list'),
    url(r'^create_activity', views.create_activity, name='create_activity'),
    url(r'^update_activity$', views.update_activity, name='update_activity'),
    url(r'^update_activity_register$', views.update_activity_register, name='update_activity_register'),
    url(r'^download_activity_list$', views.download_activity_list, name='download_activity_list'),
    url(r'^download_activity_register_list/(?P<activity_id>[\w\-]+)/', views.download_activity_register_list, name='download_activity_register_list'),
    url(r'^remove_activity/(?P<activity_id>[\w\-]+)/', views.remove_activity, name='remove_activity'),
    url(r'^remove_activity_register/(?P<register_id>[\w\-]+)/', views.remove_activity_register, name='remove_activity_register'),

]
