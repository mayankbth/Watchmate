# from django.shortcuts import render
# from watchlist_app.models import Movie
# from django.http import JsonResponse

# # Create your views here.

# def movie_list(request):
#     movies = Movie.objects.all()
#     # here at "movies = Movie.objects.all()", we are getting complex data (queryset).
#     # A QuerySet is a list of objects of a given model, QuerySet allow you to read data from database. 
#     data = {'movies': list(movies.values())}
    # '''
    #     values()¶
    #     values(*fields, **expressions)¶
    #     Returns a QuerySet that returns dictionaries, rather than model instances, when used as an iterable.

    #     Each of those dictionaries represents an object, with the keys corresponding to the attribute names of model objects.

    #     This example compares the dictionaries of values() with the normal model objects:

    #     # This list contains a Blog object.
    #     >>> Blog.objects.filter(name__startswith='Beatles')
    #     <QuerySet [<Blog: Beatles Blog>]>

    #     # This list contains a dictionary.
    #     >>> Blog.objects.filter(name__startswith='Beatles').values()
    #     <QuerySet [{'id': 1, 'name': 'Beatles Blog', 'tagline': 'All the latest Beatles news.'}]>
    # '''
#     print(data)
#     return JsonResponse(data)


# def movie_details(request, pk):
#     movie = Movie.objects.get(pk=pk)
#     # print(movie) 
#     data = {
#         'name': movie.name,
#         'description': movie.description,
#         'active': movie.active,
#     }
#     return JsonResponse(data)
