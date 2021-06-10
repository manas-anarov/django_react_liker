from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import (
    ModelSerializer,
)
from .models import (Post,
                     Likes
                     )

from django.conf import settings


class ListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'category',
            'title',
            'text',
        ]


class AddSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'text',
        ]

    def validate(self, data):
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        all_posts = Post.objects.filter(author=user).count()
        if all_posts >= 5:
            raise serializers.ValidationError("MAX_LIKES_PER_USER Limit")
        return data


class ShowSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'category',
            'title',
            'text',
        ]


class DeleteSerializer(ModelSerializer):
    class Meta:
        model = Post


class UpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'category',
            'title',
            'text',
        ]


class LikeSerializer(ModelSerializer):
    post_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Likes
        fields = [
            'post_id',
        ]

    def validate_post_id(self, value):
        # if post does not exist return error
        post_id = value
        post_qs = Post.objects.filter(id=post_id)
        if not post_qs.exists():
            raise ValidationError("Post does  not exists")

        # if likes exists, return error
        current_user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            current_user = request.user

        like_qs = Likes.objects.filter(post__pk=post_id, user=current_user)
        if like_qs.exists():
            raise ValidationError("Already Liked")
        return value

    def create(self, validated_data):

        current_user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            current_user = request.user

        post_id = validated_data['post_id']
        post = Post.objects.get(pk=post_id)

        likes = Likes.objects.filter(post__pk=post_id, user=current_user).count()

        if likes == settings.MAX_LIKES_PER_USER:
            raise ValidationError("MAX_LIKES_PER_USER Limit")
        if likes < settings.MAX_LIKES_PER_USER:
            new_like = Likes(
                post=post,
                user=current_user
            )
            new_like.save()

        return post_id


class UnlikeSerializer(ModelSerializer):
    post_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Likes
        fields = [
            'post_id',
        ]

    def validate_post_id(self, value):
        # if post does not exist return error
        post_id = value
        post_qs = Post.objects.filter(id=post_id)
        if not post_qs.exists():
            raise ValidationError("Post does not exists")

        # if likes exists, return error
        current_user = self.context.get("request").user
        like_qs = Likes.objects.filter(post__pk=post_id, user=current_user)
        if not like_qs.exists():
            raise ValidationError("Like does not exists")
        return value
