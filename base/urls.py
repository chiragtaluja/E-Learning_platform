from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginPage, name="login"), 
    path("register/", views.RegisterUser, name="register"),  # Login/Register route
    path("", views.index, name="index"),  # Home page route
    path("room/<str:room_id>/", views.room, name="room"),
    path("create-room/", views.create_room, name="create-room"),  # Dynamic room route
    path("update-room/<str:room_id>/", views.update_room, name="update-room"),  # Dynamic room route
    path("delete-room/<str:room_id>/", views.delete_room, name="delete-room"),
    path("logout/", views.logoutUser, name="logout"),
    path("delete-message-room/<str:message_id>/", views.delete_message_room, name="delete-message-room"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("add-topics/", views.add_topics, name="add_topics"),
    path("update-user/<str:username>/", views.update_user, name="update_user"),  # Update user profile route
    path("about-us/", views.about_us, name="about_us"),  # About Us page route
    path("home/", views.home, name="home"),  # Home page route
    path("contact-us/", views.contact_us, name="contact_us"),  # Contact Us page route
]
