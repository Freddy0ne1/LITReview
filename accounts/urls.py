from accounts import views
from django.urls import path

urlpatterns = [
    path("login/", views.login_page, name="login"),
    path("signup/", views.signup_page, name="signup"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile_page, name="profile"),
    path("profile/edit/", views.edit_profile_page, name="edit_profile"),
    path("profile/change-password/", views.change_password_page, name="change_password"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("follow/<int:user_id>/", views.follow_user, name="follow_user"),
    path("unfollow/<int:user_id>/", views.unfollow_user, name="unfollow_user"),
    path("block/<int:user_id>/", views.block_user, name="block_user"),
    path("unblock/<int:user_id>/", views.unblock_user, name="unblock_user"),
    path("bloked-users/", views.blocked_users, name="blocked_users"),
]