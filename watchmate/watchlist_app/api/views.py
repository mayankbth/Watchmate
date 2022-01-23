# from django.shortcuts import get_object_or_404
from rest_framework.response import Response
# from rest_framework.decorators import api_view
# this "from rest_framework.decorators import api_view" is for function based view
from rest_framework.views import APIView
# this "from rest_framework.views import APIView" is for class based view
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework import generics
# from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
# this is for throttling (local level throttling) by this way we can implement throttling on individuals classes
# instead of applying throttling on all the classes by using global setting.
# UserRateThrottle: is for registered users
# AnonRateThrottle: is for unregistered user

from django_filters.rest_framework import DjangoFilterBackend
# django filtering
from rest_framework import filters

from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
# from watchlist_app.models import Movie
from watchlist_app.models import WatchList, StreamPlatform, Review
# from watchlist_app.api.serializers import MovieSerializer
from watchlist_app.api.serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle


""" Filtering """

class UserReview(generics.ListAPIView):
    # for explanation see "class ReviewList(generics.ListAPIView):"

    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # permission_classes = [IsAuthenticated]
    # throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    # def get_queryset(self):
    #     # Here instead of "pk" we are going to perform search on "username" in "pk = self.kwargs['pk']"
    #     # So, here I am utilizing the username...
    #     # and for that we are going to utilize this "review_user" form "class Review" under model.py
    #     username = self.kwargs['username']
    #     # return Review.objects.filter(review_user=username)
    #     # Here I am performing the filter based on username provided by the user through the request via URL.
    #     # here, "review_user" is a foreign key so, with this we are getting the error like...
    #     # Field 'id' expected a number but got 'mayank'. here, 'mayank' is "username" what we passed through URL.
    #     # So, we need to define what this "username" mean to foreign key.
    #     return Review.objects.filter(review_user__username=username)
    #     # So, here it will first jump on this "review_use" foreign key and the "username" field of the different model
    #     # to match it.

    def get_queryset(self):
        username = self.request.query_params.get('username')
        # here, I am mapping the parameter directly instead of mapping the value.
        return Review.objects.filter(review_user__username=username)


""" ModelViewSets """

class StreamPlatformVS(viewsets.ModelViewSet):
    # The ModelViewSet class inherits from GenericAPIView and includes implementations for various actions, by mixing in
    # the behavior of the various mixin classes. The actions provided by the ModelViewSet class are .list(),
    # .retrieve(), .create(), .update(), .partial_update(), and .destroy().

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    # using "ModelViewSet" we have control of everything in just few lines of code.
    permission_classes = [IsAdminOrReadOnly]




# class StreamPlatformVS(viewsets.ReadOnlyModelViewSet):
#     # ReadOnlyModelViewSet
#     # The ReadOnlyModelViewSet class also inherits from GenericAPIView. As with ModelViewSet it also includes
#     # implementations for various actions, but unlike ModelViewSet only provides the 'read-only' actions, .list() and
#     # .retrieve().
#
#     queryset = StreamPlatform.objects.all()
#     serializer_class = StreamPlatformSerializer



""" ViewSets """
# Django REST framework allows you to combine the logic for a set of related views in a single class, called a ViewSet.
# In other frameworks you may also find conceptually similar implementations named something like 'Resources' or
# 'Controllers'. A ViewSet class is simply a type of class-based View, that does not provide any method handlers such as
# .get() or .post(), and instead provides actions such as .list() and .create(). The method handlers for a ViewSet are
# only bound to the corresponding actions at the point of finalizing the view, using the .as_view() method.

# class StreamPlatformVS(viewsets.ViewSet):
#
#     def list(self, request):
#         queryset = StreamPlatform.objects.all()
#         serializer = StreamPlatformSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = StreamPlatform.objects.all()
#         watchlist = get_object_or_404(queryset, pk=pk)
#         serializer = StreamPlatformSerializer(watchlist)
#         return Response(serializer.data)
#
#     def create(self, request):
#         serializer = StreamPlatformSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)


"""Concrete View Classes"""
# NOTE: We are going to import "Concrete View Classes" from "Generic Views classes" Class it self.
# So, this is a part of "Generic View Class" it self.
# When we are going to use this "Concrete View Classes" we do need to write, list or anything else because they already
# have them. That is we do not need to import "Mixins" because they already have them.

class ReviewCreate(generics.CreateAPIView):
    # Used for create-only endpoints.
    # Provides a post method handler.

    # Here, we are overriding the the current function because we need to pass the specific movie ID for creation of
    # review for a specifics movies.
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]

    def get_queryset(self):
        return Review.objects.all()
    # here, we have defined this because,
    # Every view needs a queryset defined to know what objects to look for. You define the view's queryset by using the
    # queryset attribute or returning a valid queryset from a get_queryset method.

    def perform_create(self, serializer):
        # we can use this "perform_create" method to override our create method.
        # NOTE:
        # perform_create(self, serializer) - Called by CreateModelMixin when saving a new object instance.
        # perform_update(self, serializer) - Called by UpdateModelMixin when saving an existing object instance.
        # perform_destroy(self, instance) - Called by DestroyModelMixin when deleting an object instance.
        pk = self.kwargs.get('pk')
        # here I am using "self.kwargs" because everything is going to be inside here and then I am selecting my "pk"
        watchlist = WatchList.objects.get(pk=pk)

        # Here, I am checking whether the current user has already submitted the review or not for the for movie.
        # that is "watchlist".

        # Here, I am going to get the information about the current user.
        # here, inside this "review_user" I am storing all the in formation related to current user.
        review_user = self.request.user
        # now i have access to current user.

        # now i need to check if the current user has done the review for this particular movie or this "watchlist".
        # here, I am filtering on two basis. first "movie", which is my watchlist. and then second is user,
        # which is "review_user".
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)

        if review_queryset.exists():
            raise ValidationError("You have already reviewed this movie!")

        if watchlist.number_rating == 0:
            watchlist.avg_rating = serializer.validated_data['rating']
        else:
            watchlist.avg_rating = (watchlist.avg_rating + serializer.validated_data['rating'])/2

        watchlist.number_rating = watchlist.number_rating + 1
        watchlist.save()

        serializer.save(watchlist=watchlist, review_user=review_user)

        serializer.save(watchlist=watchlist, review_user=review_user)
        # Here, I am saving my serializer. Where my watchlist is equal to "watchlist" object inside my "Review" model
        # and also saving the user current user in the serializer.


class ReviewList(generics.ListAPIView):
    # ListAPIView
    # Used for read-only endpoints to represent a collection of model instances.
    # Provides a get method handler.
# class ReviewList(generics.ListCreateAPIView):
    # ListCreateAPIView
    # Used for read-write endpoints to represent a collection of model instances.
    # Provides get and post method handlers.

    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    # authentication policy on a per-view, or per-viewset basis, using the APIView class-based views.
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [IsAuthenticated]
    # # Now, only authenticated user can access the "ReviewList".

    # here we are writing a function "get_queryset" for getting all the reviews for a particular movie.
    # here we are overriding our current queryset "queryset = Review.objects.all()"
    # throttle_classes = [UserRateThrottle, AnonRateThrottle]

    throttle_classes = [ReviewListThrottle, AnonRateThrottle]

    filter_backends = [DjangoFilterBackend]
    # once we add "filter_backend" we need to mention which fields we need to filter
    # So, this "filter_backends" defines that, this filter "DjangoFilterBackend" we are going to use but which fields
    # we are going to filter. So, if I am talking about "class Review" form "models.py" then we have the options...
    # review_user, rating, description, watchlist, active, created, update. That is any field of selected model.
    # and to do that we need to use "filterset_fields"
    filterset_fields = ['review_user__username', 'active']

    def get_queryset(self):
        pk = self.kwargs['pk']
        # here I am using "self.kwargs" because everything is going to be inside here and then I am selecting my "pk"

        # Now, I am going to select my "pk" (Primary Key) and then I am going to select my review.
        # Specifically, where my "WatchList" is this "pk" ID. So, i am going to use a "filter" and instead of "(pk=pk)"
        # I need to select this "watchlist" from "Review" model.
        return Review.objects.filter(watchlist=pk)
        # Here, instead on returning all the objects "Review.objects.all()", i am going to filter my object according to
        # the movie. Because we know the ID (<int:pk>) in
        # "path('stream/<int:pk>/review/', ReviewList.as_view(), name='review-list')," is my movie.
        # That is my "watchlist".


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    # RetrieveUpdateDestroyAPIView
    # Used for read-write-delete endpoints to represent a single model instance.
    # Provides get, put, patch and delete method handlers.
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]
    # IsAuthenticatedOrReadOnly:
    # The IsAuthenticatedOrReadOnly will allow authenticated users to perform any request. Requests for unauthorised
    # users will only be permitted if the request method is one of the "safe" methods; GET, HEAD or OPTIONS.
    # This permission is suitable if you want to your API to allow read permissions to anonymous users, and only allow
    # write permissions to authenticated users.

    # throttle_classes = [UserRateThrottle, AnonRateThrottle]

    throttle_classes = [ScopedRateThrottle]
    # The ScopedRateThrottle class can be used to restrict access to specific parts of the API. This throttle will only
    # be applied if the view that is being accessed includes a .throttle_scope property. The unique throttle key will
    # then be formed by concatenating the "scope" of the request with the unique user id or IP address.
    #
    # Now, we need to mentioned.
    throttle_scope = 'review-detail'
    # Note:
    # we are adding restrings according to "ScopedRateThrottle"


"""Generic Views"""

# # we have created a "ReviewList" class, Now we are going to utilize this import of generic view.
# # NOTE: this "generics.GenericAPIView" is going to be in the last. Like...
# # class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
# # initials all will be our mixins and then we will have our "GenericAPIView" class
# # so here I am going to import all the method mixins that i am going to perform.
# # here i am imported "ListModelMixin" that means i am going to perform a get request for list
# # and "CreateModelMixin" it means i am going to perform a post request request. which is going to be create
# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     # Now, I need to define my "queryset" in which I am going to collect all the object
#     # then i need to define my "serializer_class"
#     # NOTE: "queryset" and "serializer_class" are attribute name and we can not change the.
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)


""" Class Based Views """

class StreamPlatformAV(APIView):
    permission_classes = [IsAdminOrReadOnly]


    def get(self, request):
        platform = StreamPlatform.objects.all()
        # Serializer = StreamPlatformSerializer(platform, many=True)
        # Serializer = StreamPlatformSerializer(platform, many=True, context={'request': request})


        # # For "HyperlinkedModelSerializer"
        # # At the time of initiating our serializer I need to add this "request" like "context={'request': request}"
        # # So, we basically need this "request" content.
        # # So, this will give access to URLs of
        Serializer = StreamPlatformSerializer(platform, many=True)
        # error: serializers.HyperlinkedModelSerializer
        # Serializer = StreamPlatformSerializer(platform, many=True, context={'request': request})
        return Response(Serializer.data)

    def post(self, request):
        serializer = StreamPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class StreamDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            platform = StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = StreamPlatformSerializer(platform)
        return Response(serializer.data)

    def put(self, request, pk):
        platform = StreamPlatform.objects.get(pk=pk)
        serializer = StreamPlatformSerializer(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        platform = WatchList.objects.get(pk=pk)
        platform.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Creating this class for filtering test purpose only
# SearchFilter
class WatchListGV(generics.ListAPIView):
    # queryset = WatchList.objects.all()
    queryset = WatchList.objects.all()
    serializer_class = WatchListSerializer

    # this is for "filter"
    # filter_backends = [DjangoFilterBackend]
    # # to search anything all we need to do is define our "filter_backends" with "SearchFilter" like...
    # filter_fields = ['title', 'platform__name']

    # # this is for "Search Filter"
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['title', 'platform__name']

    # this is for "Ordering Filter"
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['avg_rating']


class WatchListAV(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [AnonRateThrottle]


    def get(self, request):
        movies = WatchList.objects.all()
        Serializer = WatchListSerializer(movies, many=True)
        return Response(Serializer.data)

    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class WatchDetailAV(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data)

    def put(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        serializer = WatchListSerializer(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


""" Class Based Views"""
# the first thing i am doing here is creating a class called "MovieListAV"
# class MovieListAV(APIView):
#     # here in "MovieListAV" AV stands for API View, the thing is there will be different more classes and there will be
#     # many more classes and i do not want to mix them.
#     # to inherit the class we need to use "APIView" like, "class MovieListAV(APIView):"
#     # as we have done in our function based view, we used the "if" "else" conditions for defining our methods. like...
#     #
#     # def movie_list(request):
#     #     if request.method == 'GET':
#     #         movies = Movie.objects.all()
#     #         Serializer = MovieSerializer(movies, many=True)
#     #         return Response(Serializer.data)
#     #
#     # So, here in our class based view, instead of using the if condition what i can do is, i can directly define the
#     # method. like, i can directly define "def get()" method to do all the task. and same goes for post and as well as
#     # others.
#     # NOTE:
#     # we are not going to utilize any type of decorator with our class based view. and also we do not need to define
#     # conditions like, "['GET', 'POST']", as we defined in our decorator used in function based view
#     # "@api_view(['GET', 'POST'])", because if we have defined this "def get(self, request):" method that means our
#     # class based view supports "get()" method and same goes for the post method.
#
#     def get(self, request):
#         movies = Movie.objects.all()
#         Serializer = MovieSerializer(movies, many=True)
#         return Response(Serializer.data)
#
#     def post(self, request):
#         serializer = MovieSerializer(data=request.data)
#         # request.data Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
#         # because in "POST", "PUT" and "PATCH" we are getting the data from user.
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
#
# class MovieDetailAV(APIView):
#
#     def get(self, request, pk):
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#
#     def put(self, request, pk):
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


""" Function Based Views"""
# @api_view(['GET', 'POST'])
# # here "@api_view(['GET', 'POST'])" we are defining the requests. i.e. if i have a "GET" request i need to do a certain
# # thing and if i have a "POST" request i need to do a certain thing.
# # @api_view()
# # Signature: @api_view(http_method_names=['GET'])
#
# # The core of this functionality is the api_view decorator, which takes a list of HTTP methods that your view should respond to. For example, this is how you would write a very simple view that just manually returns some data:
#
# # from rest_framework.decorators import api_view
#
# # @api_view()
# # def hello_world(request):
# #     return Response({"message": "Hello, world!"})
# # This view will use the default renderers, parsers, authentication classes etc specified in the settings.
#
# # By default only GET methods will be accepted. Other methods will respond with "405 Method Not Allowed". To alter this behaviour, specify which methods the view allows, like so:
#
# # @api_view(['GET', 'POST'])
# # def hello_world(request):
# #     if request.method == 'POST':
# #         return Response({"message": "Got some data!", "data": request.data})
# #     return Response({"message": "Hello, world!"})
#
# def movie_list(request):
#
#     if request.method == 'GET':
#         movies = Movie.objects.all()
#         # here I am selecting the complex data.
#         # if we are going to have multiple objects. Then we need to pass the "many= True",
#         # in "Serializer = MovieSerializer(movies, many= True)"
#         Serializer = MovieSerializer(movies, many=True)
#         # if we have multiple objects then we need to pass "many=True".
#         # pass the complex data into serializer
#         # print(Serializer)
#         # print(Serializer.data)
#         return Response(Serializer.data)
#         # Serializer.data returns a copy of the validated data
#         # to access all the information held by "Serializer" we need to use ".data" because all the information held by
#         # "Serializer" is i the form of object.
#         # REST framework supports HTTP content negotiation by providing a Response class which allows you to return
#         # content that can be rendered into multiple content types, depending on the client request.
#
#     if request.method == 'POST':
#         # when post request, we are going to receive the data from user
#         # and in that case we need to save the data and for that I am saving the data into "serializer".
#         # and the data we are getting with "request" so we will need to utilize this "request" and for that we will
#         # need to access the data associated with the "request" and to access the data and store it in data i am doing
#         # "data=request.data" and then passing it to "MovieSerializer" in our "MovieSerializer" class to serialize
#         # the data. and then tha serialize data is getting stored in "serializer".
#         serializer = MovieSerializer(data=request.data)
#         # request.data  # Handles arbitrary data.  Works for 'POST', 'PUT' and 'PATCH' methods.
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)
#
# @api_view(['GET', 'PUT', 'DELETE'])
# # in "PUT" request we rewrite everything
# # in "DELETE" we delete the object
# def movie_details(request, pk):
#
#     if request.method == 'GET':
#
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
#
#     if request.method == 'PUT':
#         # when we are working with the serializer, we also need to pass which object we are trying to update.
#         # that means we need to select the exact object that we are going to update. which is going to be our particular
#         # ID i.e. pk id.
#         # so, if i am updating id 1 i need to pass it in "serializer = MovieSerializer(data=request.data)"
#         movie = Movie.objects.get(pk=pk)
#         serializer = MovieSerializer(movie, data=request.data)
#         # when we are working with the serializer, we also need to pass which object we are trying to update. that means
#         # i need to select the exact object, that we are going to update. which is going to be our particular ID
#         # (i.t. pk ID). Suppose, if i am updating ID 1 I need to pass it here with my serializer and we are doing this
#         # by passing "movie" in "serializer = MovieSerializer(movie, data=request.data)".
#         #
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

