from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("register/", views.RegisterApi.as_view(), name="register"),
    path("login/", views.LoginApi.as_view(), name="login"),
    path("me/", views.UserApi.as_view(), name="me"),
    path("logout/", views.LogoutApi.as_view(), name="logout"),
]



# from django.urls import path
# from . import views

# urlpatterns = [
#     path('login/', views.login, name='login'),
#     path('logout/', views.logout, name='logout'),
#     path('register/', views.register, name="register"),
# ]
