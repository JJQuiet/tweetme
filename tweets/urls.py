from django.urls import path, re_path #url()
from .views import home_view, tweet_detail_view, tweet_list_view, tweet_create_view, tweet_delete_view

# urlpatterns = [
#     path('', home_view),
#     path('tweets/<int:tweet_id>', tweet_detail_view),
#     path('tweets', tweet_list_view),
#     path('create-tweet', tweet_create_view),
# ]
