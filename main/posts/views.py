from rest_framework.views import APIView

from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateAPIView,
    DestroyAPIView,
    ListAPIView,
    RetrieveAPIView
)
from rest_framework.response import Response

from .models import (Post,
                     Likes
                     )
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework import status

from .seralizers import ListSerializer, AddSerializer, ShowSerializer, DeleteSerializer, UpdateSerializer, \
    LikeSerializer, UnlikeSerializer


class PostListAPIView(ListAPIView):
    serializer_class = ListSerializer
    queryset = Post.objects.all()


class AddPost(CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddSerializer
    queryset = Post.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ShowPost(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = ShowSerializer
    lookup_field = 'id'


class DeletePost(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = DeleteSerializer
    lookup_field = 'id'


class UpdatePost(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = UpdateSerializer
    lookup_field = 'id'


class LikePost(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        serializer = LikeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            data = serializer.save()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = UnlikeSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            user = request.user
            post_id = request.data.get('post_id', 1)
            like_to_delete = Likes.objects.get(post__pk=post_id, user=user)
            like_to_delete.delete()
            return Response("deleted", status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class StartBot(APIView):
# 	def get(self, request, format=None):


# 		return Response('hi', status=status.HTTP_201_CREATED)
