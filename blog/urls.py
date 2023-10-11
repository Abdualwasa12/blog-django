from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.post_list, name='post_list'),
    path('tag/<slug:tag_slug>/',views.post_list, name='post_list_by_tag'),
    path('<slug:slug>', views.post_detail, name='post_detail'),
    path('<int:id>', views.post_detail, name='post_detail'),
    path('add/',views.add_post, name='add_post'),
    path('<int:post_id>/comment',views.comment_post, name='comment_post'),
    path('category/<int:id>',views.category_list,name='category_list'),

    # path('<int:post_id>/comment/reply',views.reply_comment, name='reply_comment'),

    
]