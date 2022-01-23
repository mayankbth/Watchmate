# here we are creating a serializer, and this will handle everything regarding the conversion.

from rest_framework import serializers
# from watchlist_app.models import Movie
from watchlist_app.models import WatchList, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    # StringRelatedField:
    # StringRelatedField may be used to represent the target of the relationship using its __str__ method.
    #
    # For example, the following serializer:
    #
    # class AlbumSerializer(serializers.ModelSerializer):
    #     tracks = serializers.StringRelatedField(many=True)
    #
    #     class Meta:
    #         model = Album
    #         fields = ['album_name', 'artist', 'tracks']
    # Would serialize to the following representation:
    #
    # {
    #     'album_name': 'Things We Lost In The Fire',
    #     'artist': 'Low',
    #     'tracks': [
    #         '1: Sunflower',
    #         '2: Whitetail',
    #         '3: Dinosaur Act',
    #         ...
    #     ]
    # }
    # This field is read only.
    #
    # Arguments:
    #
    # many - If applied to a to-many relationship, you should set this argument to True.

    class Meta:
        model = Review
        exclude = ('watchlist',)
        # fields = "__all__"


class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True, read_only=True)

    # to access the name of the platform instead of the ID of the platform and to get that I am overriding the platform
    # field here
    platform = serializers.CharField(source='platform.name')
    # with this source i need to mention to which model and which field we are going to target.
    # We have overridden this platform field which was by default showing us the ID. Now it will show us the name of the
    # platform instead of the ID value.

    # len_name = serializers.SerializerMethodField()
    class Meta:
        model = WatchList
        fields = "__all__"


class StreamPlatformSerializer(serializers.ModelSerializer):

    # here we are creating relationship between the both serializers ("StreamPlatformSerializer" and "WatchListSerializer")
    # I.e. I want relationship between all the movies and platforms.
    # So, that at this page "http://127.0.0.1:8000/watch/stream/", I want Netflix to show all the movies to show all the
    # movies it has and same goes for Prime Videos and None.
    # and for that we can create relationship in there respective serializer.
    # For an example one movie can have only one platform but one platform can have many movies.
    # So, it means this is ("StreamPlatformSerializer") our platform and it can have many movies.
    # and this relationship is called "Nested Relationship"
    # So here, we are defining one streaming platform can have many movies and web shows.
    watchlist = WatchListSerializer(many=True, read_only=True)
    # here we have taken "watchlist" from "class WatchList(models.Model):" from models.py
    # "platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")"
    # So, here "watchlist = WatchListSerializer(many=True, read_only=True)" what we did is.
    # We created a new item, means a new field here in which we are going to have all the elements regarding this
    # watchlist. So, if we have selected Netflix it is going to show all the movies and all that Netflix currently has.
    # NOTE:
    # this "watchlist" name is very important because we have defined it in our "WatchList" model as related name.
    # suppose if i try to use any other name like "watch" it will not work. like...
    # watch = WatchListSerializer(many=True, read_only=True)

    # # The above line of code will return all the content because we are directly using our serializer
    # # but to get the specific field. Suppose we only want the title field or any other specific field
    # # NOTE (documentation): https://www.django-rest-framework.org/api-guide/relations/#api-reference
    # # StringRelatedField
    # # StringRelatedField may be used to represent the target of the relationship using its __str__ method.
    # # that is it will return whatever we have defined in our "__str__"
    # watchlist = serializers.StringRelatedField(many=True)
    # # and same goes for (see the documentation)
    # # PrimaryKeyRelatedField, HyperlinkedRelatedField
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-details'
    # )

    # here we are

    class Meta:
        model = StreamPlatform
        fields = "__all__"


"""erroe: serializers.HyperlinkedModelSerializer"""
# HyperlinkedModelSerializer
# The HyperlinkedModelSerializer class is similar to the ModelSerializer class except that it uses hyperlinks to
# represent relationships, rather than primary keys.
# class StreamPlatformSerializer(serializers.HyperlinkedModelSerializer):
#
#     watchlist = WatchListSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = StreamPlatform
#         fields = "__all__"
#         # # fields = ['id', 'watchlist', 'name', 'about', 'website']
#         # fields = ['id', 'url', 'name', 'about', 'website']


"""serializer.ModelSerializer"""
# class MovieSerializer(serializers.ModelSerializer):
#
#     # Custom Serializer field: is a field which is used to provided some information based on existing field in model
#     # In our case we are going to create a custom serializer field to provide the length of value stored in
#     # the "name" field. So, for that, here I am creating a custom serializer field named "len_name" to show the length
#     # of "name" field.
#     len_name = serializers.SerializerMethodField()
#     # by using "serializers.SerializerMethodField()", we can define a method, which calculates the length of our name.
#
#     # Note:
#     # In "serializers.ModelSerializer", "ModelSerializer" contains everything about our create, update and all the
#     # fields. So, that means we do not have to write everything. all we need to do is just mention, which model we
#     # are using. Here, that means our "Movie" model and what type of field we need to work with.
#     # So, if we use all that means all fields and if we want to exclude any we can do that.
#     # So, we have all the control here with this "ModelSerializer".
#     #
#     #     A `ModelSerializer` is just a regular `Serializer`, except that:
#     #     * A set of default fields are automatically populated.
#     #     * A set of default validators are automatically populated.
#     #     * Default `.create()` and `.update()` implementations are provided.
#     class Meta:
#         model = Movie
#         fields = "__all__"
#         # here I am hiding the field "active". for that instead of "__all__" i will define each field individually.
#         # fields = ['id', 'name', 'description']
#
#         # we can define the field individually or can use "__all__" for defining all the fields.
#         # and this is all we need to define our "ModelSerializer".
#
#         # suppose, if there is 20 field and we need to define 19 only then we can use "exclude" instead of defining 19
#         # fields individually. in "exclude" we just need to mention that which field we do not want.
#         # exclude = ['active']
#
#     # # Now, we can define a custom method which is going to calculate this "len_name" (length of our name) and we will
#     # # get this name field in our response.
#     # # now i need to define our method. So, I am going to define a method here, and I am going to call it as
#     # # "get_" and this exact name "len_name" like, "get_len_name", which is my variable name right now. and this method
#     # # is going to take "self" and "object" as a parameter.
#     # def get_len_name(self, object):
#     #     # Now, this "object" has access to everything. i.e. our ID, Name as well as description for each element.
#     #     # So, suppose if I need to return the length of our name
#     #     return len(object.name)
#
#     # # if we need to add validations. we have to define them separately. like this...
#     # # other wise there is no chance our serializer will be aware of it.
#     # # Here, we are going to use validation in our serializer.py and these validation will be called whenever we are
#     # # going to use them in views i.e. whenever we will call this "serializer.is_valid()" in our view.
#     # # in "Field Level" validation we only check a particular field.
#     # # when we add a validation on a complete object we like stating that, name and description should not be same and so
#     # # on is called "Object Level Validation"
#     #
#     # # Field-level validation
#     # # You can specify custom field-level validation by adding .validate_<field_name> methods to your Serializer
#     # # subclass. These are similar to the .clean_<field_name> methods on Django forms.
#     # # These methods take a single argument, which is the field value that requires validation.
#     # # Your validate_<field_name> methods should return the validated value or raise a serializers.ValidationError.
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short!")
#     #     else:
#     #         return value
#     #
#     # # Object-level validation
#     # # To do any other validation that requires access to multiple fields, add a method called .validate() to your
#     # # Serializer subclass. This method takes a single argument, which is a dictionary of field values. It should raise a
#     # # serializers.ValidationError if necessary, or just return the validated values.
#     # def validate(self, data):
#     #     if data['name'] == data['description']:
#     #         raise serializers.ValidationError("Title and description should be different!")
#     #     else:
#     #         return data

"""serializer.Serializer"""
# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")
#
#
# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     # name = serializers.CharField()
#     # Validators
#     # Individual fields on a serializer can include validators, by declaring them on the field instance
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()
#     # here we have already defined the class "class MovieSerializer(serializers.Serializer):" and this will work for get
#     # request however, for "POST" and "PUT" request we need to define two methods as per "django-rest-framework"s
#     # documentation:
#     # POST: "def create(self, validated_data):"
#     # PUT: "def update(self, instance, validated_data):"
#
#     def create(self, validated_data):
#         # for "POST" request we need this "create" function.
#         # "validated_data" carries the data posted by user
#         # this "validated_data" will have everything our name, description as well as active
#         # data : is a dict and you can see it only after is_valid() (you can see only not validated values)
#         # validated_data: is an OrderedDict and you can see it only after is_valid() and is_valid() == True
#         # once we get this "validated_data" all we have to do is create an instance in my object. that is in our
#         # database and just return that instance.
#         return Movie.objects.create(**validated_data)
#         # here by "Movie.objects.create()" we are creating an instance and after that we needed to pass the
#         # "**validated_data". so, now this data will have everything our name description as well active.
#         # **kwargs
#         # The special syntax **kwargs in function definitions in python is used to pass a keyword, variable-length
#         # argument list.
#         # To create and save an object in a single step, use the create() method.
#
#     def update(self, instance, validated_data):
#         # here the "instance" carries the old values and "validated_data" carries the new values provided by user.
#         # so, we need to map everything old with new.
#         instance.name = validated_data.get('name', instance.name)
#         # "instance.name" is old name and i need to just update it with new one which is my "validated_data" and to get
#         # the new name "get('name')". So, "validated_data.get('name')" and also we need to pass the old instance with
#         # the new name. that is "instance.name = validated_data.get('name', instance.name)".
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#         # here in "return" we are just using the instance like "return instance" because it contains all the values.
#
#     # Here, we are going to use validation in our serializer.py and these validation will be called whenever we are
#     # going to use them in views i.e. whenever we will call this "serializer.is_valid()" in our view.
#     # in "Field Level" validation we only check a particular field.
#     # when we add a validation on a complete object we like stating that, name and description should not be same and so
#     # on is called "Object Level Validation"
#
#     # # Field-level validation
#     # # You can specify custom field-level validation by adding .validate_<field_name> methods to your Serializer
#     # # subclass. These are similar to the .clean_<field_name> methods on Django forms.
#     # # These methods take a single argument, which is the field value that requires validation.
#     # # Your validate_<field_name> methods should return the validated value or raise a serializers.ValidationError.
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short!")
#     #     else:
#     #         return value
#
#     # Object-level validation
#     # To do any other validation that requires access to multiple fields, add a method called .validate() to your
#     # Serializer subclass. This method takes a single argument, which is a dictionary of field values. It should raise a
#     # serializers.ValidationError if necessary, or just return the validated values.
#     def validate(self, data):
#         if data['name'] == data['description']:
#             raise serializers.ValidationError("Title and description should be different!")
#         else:
#             return data

