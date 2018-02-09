from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.volunteer, name='volunteer'),
    url(r'^load_volunteer_list', views.load_volunteer_list, name='load_volunteer_list'),
    url(r'^get_volunteer_list', views.get_volunteer_list, name='get_volunteer_list'),
    # url(r'^add_group', views.add_group, name='add_group'),
    url(r'^update_volunteer_info', views.update_volunteer_info, name='update_volunteer_info'),
    url(r'^download_volunteer_list', views.download_volunteer_list, name='download_volunteer_list'),
    url(r'^remove_volunteer/(?P<openid>[\w\-]+)/', views.remove_volunteer, name='remove_volunteer'),
    url(r'^volunteer_profile/(?P<openid>[\w\-]+)/', views.volunteer_profile, name='volunteer_profile'),
    url(r'^register/(?P<qrcode_id>[\w\-]+)/', views.register, name="register"),
    url(r'^signup/(?P<activity_id>[\w\-]+)/', views.signup, name="signup"),
    url(r'^register_volunteer', views.register_volunteer, name="register_volunteer"),
    url(r'^get_qrcode', views.get_qrcode, name='get_qrcode'),
    url(r'^error', views.mobile_error, name="error")

]
