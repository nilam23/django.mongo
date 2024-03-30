from django.urls import path
from blog import views

urlpatterns = [
  path('blog', views.create_blog, name='create_blog'),
  path('blogs', views.get_all_blogs, name='get_all_blogs'),
  path('blogs/<str:blog_id>', views.get_specific_blog, name='get_specific_blog'),
  path('blogs/<str:blog_id>/edit', views.update_specific_blog, name='update_specific_blog'),
  path('blogs/<str:blog_id>/remove', views.delete_specific_blog, name='delete_specific_blog'),
]