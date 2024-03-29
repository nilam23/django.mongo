from django.urls import path
from blog import views

urlpatterns = [
  path('blog', views.create_blog, name='create_blog'),
  path('blogs', views.get_all_blogs, name='get_all_blogs'),
]