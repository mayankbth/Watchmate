from django.urls import path, include
# from watchlist_app.api.views import movie_list, movie_details
# from watchlist_app.api.views import MovieListAV, MovieDetailAV
# from watchlist_app.api.views import (WatchListAV, WatchDetailAV,
#                                      StreamPlatformAV, StreamDetailAV,
#                                      ReviewCreate, ReviewList, ReviewDetail, StreamPlatformVS)
from watchlist_app.api.views import (WatchListAV, WatchDetailAV,
                                     ReviewCreate, ReviewList, ReviewDetail,
                                     StreamPlatformVS,
                                     UserReview,
                                     WatchListGV)

from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('stream', StreamPlatformVS, basename='streamplatform')
# by default, here the names will be "streamplatform-list" for the first part
# and for the second "streamplatform-detail".

urlpatterns = [
    # function based view
    # path('list/', movie_list, name='movie-list'),
    # path('<int:pk>/', movie_details, name='movie-details')

    # class based view
    # path('list/', MovieListAV.as_view(), name='movie-list'),
    # path('<int:pk>/', MovieDetailAV.as_view(), name='movie-details')
    # Note:
    # in class based view we need to utilize ".as_view()" like, "MovieListAV.as_view()"

    path('list/', WatchListAV.as_view(), name='movie-list'),
    path('<int:pk>/', WatchDetailAV.as_view(), name='movie-details'),
    path('list2/', WatchListGV.as_view(), name='watch-list'),

    # here I am creating Router
    # we can create a router for a different requirement. So basically our router helps us to combine all type of link.
    # so, whenever we are using router we do not need to create a separate links, like this...
    #     path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    #     path('stream/<int:pk>/', StreamDetailAV.as_view(), name='stream-details'),
    # we can combine them in one.
    # first i need to import "from rest_framework.routers import DefaultRouter"
    # then I need to define router, like...
    # "router = DefaultRouter()"
    # that's it. I have created the router
    # Now we need to register our URLs with router. like...
    # router.register('stream', StreamPlatformVS, basename='streamplatform')
    # here, for link i have provided "stream", with this I have passed our views "StreamPlatformVS"
    # basename:
    # basename - The base to use for the URL names that are created. If unset the basename will be automatically generated
    # based on the queryset attribute of the viewset, if it has one. Note that if the viewset does not include a queryset
    # attribute then you must set basename when registering the viewset.
    #
    # Why we need basename?
    # https://stackoverflow.com/questions/22083090/what-base-name-parameter-do-i-need-in-my-route-to-make-this-django-api-work
    #
    # and the last thing we have to do is include these router in our urlpatterns.
    path('', include(router.urls)),

    # path('stream/', StreamPlatformAV.as_view(), name='stream-list'),
    # path('stream/<int:pk>/', StreamDetailAV.as_view(), name='stream-details'),

    # path('review/', ReviewList.as_view(), name='review-list'),
    # path('review/<int:pk>', ReviewDetail.as_view(), name='review-detail'),

    # path('stream/<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    # path('stream/<int:pk>/review/', ReviewList.as_view(), name='review-list'),
    # # here we are getting all the reviews for a particular movie
    # path('stream/review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),
    # # here we will get a particular review

    path('<int:pk>/review-create/', ReviewCreate.as_view(), name='review-create'),
    path('<int:pk>/reviews/', ReviewList.as_view(), name='review-list'),
    path('review/<int:pk>/', ReviewDetail.as_view(), name='review-detail'),

    # path('reviews/<str:username>/', UserReview.as_view(), name='user-review-detail'),
    path('reviews/', UserReview.as_view(), name='user-review-detail'),
]


