from django.conf import settings
from django.urls import path
from TaskApp import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


urlpatterns = [
    path('', views.login_page, name='login'),
    path('patient_signup', views.patient_signup_page, name='patient_signup'),
    path('doctor_signup', views.doctor_signup_page, name='doctor_signup'),
    path('doctor_home', views.doctor_home_page, name='doctor_home'),
    path('patinet_home', views.patient_home_page, name='patient_home'),
    path('upload_blog', views.blog_post_page, name='upload_blog'),
    path('blog_view', views.display_blog_page, name='blog_view'),
    path('blog_list', views.blog_list_page, name='blog_list'),
    path('logout', views.logout_fun, name='logout'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root = settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()    