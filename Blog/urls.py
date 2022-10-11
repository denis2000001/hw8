from django.contrib import admin
from django.urls import path
from posts.views import MainView, CreatePostView, PostDetailView, EditPostView
from django.conf.urls.static import static
from django.conf import settings
from users.views import RegisterView, LoginView, LogoutView, PersonalView, ChangePass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('posts/<pk>/detail/', PostDetailView.as_view()),
    path('posts/create/', CreatePostView.as_view()),
    path('users/register/', RegisterView.as_view()),
    path('users/login/', LoginView.as_view()),
    path('users/logout/', LogoutView.as_view()),
    path('posts/<pk>/detail/edit/', EditPostView.as_view()),
    path('users/<pk>/change_password/', ChangePass.as_view()),
    path('personal/', PersonalView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)