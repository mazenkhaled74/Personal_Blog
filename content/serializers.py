from rest_framework import serializers
from .models import Post, Category, Tag,CustomUser, Comment


class CreatePostSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), many=True)
    tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'categories', 'tags', 'likes_count']
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class GetPostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(slug_field='username', queryset=CustomUser.objects.all())
    categories = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), many=True)
    tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True)
    comments = serializers.StringRelatedField(many=True)
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'content', 'created_at', 'updated_at', 'categories', 'tags', 'comments' , 'likes_count']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    

class PostSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), many=True)
    tags = serializers.SlugRelatedField(slug_field='name', queryset=Tag.objects.all(), many=True)
    comments = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), many=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'created_at', 'updated_at', 'categories', 'tags', 'comments' , 'likes_count']

class UserSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True, source='post_set')

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'posts']
