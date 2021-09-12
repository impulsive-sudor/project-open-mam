from django.urls import path  
from . import views
urlpatterns = [
    path('', views.home),
    path('login', views.login),
    path('logout', views.logout),
    path('register', views.register),
    path('trylogin', views.trylogin),
    path('registration', views.registration),
    path('dashboard', views.dashboard),
    path('showusers', views.show_users),
    path("deleteuser/<int:user_id>", views.deleteuser)
    # path('usermanager/<int:id>', views.usermanger)
]