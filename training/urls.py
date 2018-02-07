from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.training_list, name='training_list'),
    url(r'^load_training_list', views.load_training_list, name='load_training_list'),
    url(r'^create_training', views.create_training, name='create_training'),
    url(r'^update_training', views.update_training, name='update_training'),
    url(r'^download_training_list', views.download_training_list, name='download_training_list'),
    url(r'^remove_training/(?P<training_id>[\w\-]+)/', views.remove_training, name='remove_training'),
    url(r'^remove_training_register/(?P<register_id>[\w\-]+)/', views.remove_training_register, name='remove_training_register'),
    url(r'^register_list/(?P<training_id>[\w\-]+)/', views.training_register_list, name='training_register_list'),
    url(r'^register/', views.register_training, name='register_training'),

]
