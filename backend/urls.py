from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^index', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^auth', views.auth, name='auth'),
    url(r'^admin', views.admin, name='admin'),
    url(r'^load_admin_list', views.load_admin_list, name='load_admin_list'),
    url(r'^create_admin', views.create_admin, name='create_admin'),
    url(r'^update_admin_info', views.update_admin_info, name='update_admin_info'),
    url(r'^remove_admin/(?P<username>\w+)/', views.remove_admin, name='remove_admin'),
    url(r'^download_admin_template', views.download_admin_template, name='download_admin_template'),
    url(r'^upload_batch_admin', views.upload_batch_admin, name='upload_batch_admin'),
    url(r'^download_admin_list', views.download_admin_list, name='download_admin_list'),
    url(r'^no_permission', views.no_permission, name='no_permission'),
]
