from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.activity_type, name='activity_type'),
    url(r'^load_activity_type_list', views.load_activity_type_list, name='load_activity_type_list'),
    url(r'^create_activity_type', views.create_activity_type, name='create_activity_type'),
    url(r'^update_activity_type', views.update_activity_type, name='update_activity_type'),
    url(r'^download_ctivity_type_list', views.download_activity_type_list, name='download_ctivity_type_list'),
    url(r'^remove_activity_type/(?P<type_id>[\w\-]+)/', views.remove_activity_type, name='remove_activity_type'),

]
