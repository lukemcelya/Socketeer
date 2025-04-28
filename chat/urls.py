from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from chat import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('create/', views.create_room, name="create_room"),
    path("<str:room_name>/", views.chat_room, name="chat_room"),
    path('', LoginView.as_view(template_name="chat/login.html"), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]