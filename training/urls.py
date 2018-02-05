from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.training_list, name='training_list'),
    url(r'^load_training_list', views.load_training_list, name='load_training_list'),
    url(r'^create_training', views.create_training, name='create_training'),
    url(r'^update_training', views.update_training, name='update_training'),
    url(r'^download_training_list', views.download_training_list, name='download_training_list'),
    url(r'^remove_training/(?P<training_id>[\w\-]+)/', views.remove_training, name='remove_training'),

]
