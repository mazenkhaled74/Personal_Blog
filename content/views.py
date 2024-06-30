from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, CustomUser
from .serializers import CreatePostSerializer, GetPostSerializer, CommentSerializer, UserSerializer, PostSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

class PostListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        posts = Post.objects.all()
        serializer = GetPostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializer = CreatePostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = GetPostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk= pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = GetPostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikePostAPIView(APIView):
    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.likes_count += 1
        post.save()
        return Response({'likes_count': post.likes_count}, status=status.HTTP_200_OK)
    
class CommentPostAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = CommentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            comment = serializer.save()
            post.comments.add(comment)
            post.save()
            serializedPost = GetPostSerializer(post)
            return Response(serializedPost.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class SearchAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        searchQuery = request.query_params.get('query')

        posts = Post.objects.filter(
            Q(title__icontains=searchQuery) | Q(content__icontains=searchQuery) |
            Q(categories__name__icontains=searchQuery) | Q(tags__name__icontains=searchQuery)
        ).distinct()

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
