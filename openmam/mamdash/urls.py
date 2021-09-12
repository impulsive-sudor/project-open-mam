from django.urls import path  
from . import views
from django.conf import settings
from django.conf.urls.static import static
 


urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('trylogin', views.trylogin),
    path('registration', views.registration),
    path('dashboard', views.dashboard),
    path('showusers', views.show_users),
    path("deleteuser/<int:user_id>", views.deleteuser),
    path("deletevideo/<int:video_id>", views.deletevideo),
    path('uploadfile', views.upload_file),
    path('edit_video/<int:video_id>', views.edit_video),
    path('edit_video/<int:video_id>/update', views.update_video),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)