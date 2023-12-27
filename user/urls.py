from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name="register"),
    path('login/', views.UserLoginView.as_view(), name="login"),
    path('me/', views.ProfileView.as_view(), name="me"),
    path('update/profile/', views.UpdateProfileView.as_view(), name="update-profile"),
    path('logout/', views.UserLogoutView.as_view(), name="logout"),

    path('create/user/', views.UserCreate.as_view(), name='create-user'),
    path('create/team/', views.TeamCreate.as_view(), name='create-team'),

    path('manage/users/', views.UserList.as_view(), name='list-users'),
    path('manage/users/<int:pk>/', views.UserDetail.as_view(), name='detail-user'),
    path('manage/users/<int:id>/change-password/', views.UserChangePassword.as_view(), name='update-user-password'),

    path('manage/teams/', views.TeamList.as_view(), name='list-teams'),
    path('manage/teams/<int:pk>/', views.TeamDetail.as_view(), name='detail-team'),
]
