from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.group, name='group'),
    url(r'^load_group_list', views.load_group_list, name='load_group_list'),
    url(r'^add_group', views.add_group, name='add_group'),
    url(r'^update_group_info', views.update_group_info, name='update_group_info'),
    url(r'^download_group_list', views.download_group_list, name='download_group_list'),
    url(r'^remove_group/(?P<_id>[\w\-]+)/', views.remove_group, name='remove_group'),

]
