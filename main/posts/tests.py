from django.test import TestCase
from .models import Post, Likes
from django.contrib.auth.models import User
from faker import Faker

import random
from django.conf import settings


class LikeTestCase(TestCase):

    def setUp(self):

        user = 's'

    def test_user_like(self):

        number_of_users = settings.NUMBER_OF_USERS
        max_posts_per_user = settings.MAX_POSTS_PER_USER
        max_likes_per_user = settings.MAX_LIKES_PER_USER

        # create x users
        create_users(number_of_users)
        all_users = User.objects.all()

        # create post for list of users
        for current_user in all_users:

            # create random max_post,  max_post == 1,2,3.... max_posts_per_user
            max_posts_random = random.randint(1, max_posts_per_user)
            print("max_posts", max_posts_random, "for user", current_user)

            # all post by author current_user
            user_posts_count = Post.objects.filter(author=current_user).count()

            # if we have 0 posts
            if user_posts_count == 0:
                # create max_posts_random posts, author is current_user,
                create_posts(current_user, max_posts_random)

            # if user already has posts, maximum post - users posts = new posts for create
            # new posts for create is max_post_final
            if max_posts_random > user_posts_count > 0:
                max_post_final = max_posts_random - user_posts_count

                # create max_post_final posts, author is current_user,
                create_posts(current_user, max_post_final)

        # print all posts count
        all_posts_count = Post.objects.all().count()
        print('all posts', all_posts_count)

        # if we have 2 posts, and 3 likes, we need reset likes to 2
        if all_posts_count < max_likes_per_user:
            max_likes_per_user = all_posts_count
            print('all_posts_count < max_likes_per_user')

        # set likes for list of users
        for real_user in all_users:
            print('_______________all posts for like________________', real_user)
            # create random max_likes,  max_likes == 1,2,3.... max_likes_per_user
            max_likes_random = random.randint(1, max_likes_per_user)
            # all likes by author real_user
            likes_count = Likes.objects.filter(user=real_user).count()

            # if user likes >=max_likes_random, go to next user
            if likes_count >= max_likes_random:
                continue
            # if user have 0 likes
            if likes_count == 0:
                # set max_likes_random likes, author is real_user,
                set_likes(real_user, max_likes_random)
            # if user already liked posts, maximum like - liked count = need for like
            # need for like is final_max_likes
            if max_likes_random > likes_count > 0:
                final_max_likes = max_likes_random - likes_count
                # set final_max_likes likes, author is real_user,
                set_likes(real_user, final_max_likes)


def create_posts(real_user, post_count):
    # Create post_count posts, author is real_user, generate fake title, fake text
    for i in range(post_count):
        fake = Faker()
        Post.objects.create(title=fake.text(), text=fake.text(), author=real_user)


def create_users(number_of_users):
    # Create number_of_users users, generate fake name, fake email
    for i in range(number_of_users):
        fake = Faker()
        fake.email()
        user = User.objects.create_user(fake.name(), fake.email(), fake.name())


def set_likes(real_user, max_likes):
    # save all posts for like
    posts_for_like = []
    print('max_likes', max_likes)
    # like posts if we have less than max_likes
    while len(posts_for_like) < max_likes:

        # search all posts
        for single_post in Post.objects.all():
            # check if post is liked, if liked go to next post
            like_qs = Likes.objects.filter(post=single_post, user=real_user)
            if like_qs.exists():
                continue
            else:
                # if post is not liked
                # get random boolean True or False
                must_liked = random.choice([True, False])
                # if must_liked == TRUE, we need like post
                if must_liked:
                    # add single_post post for like, to list
                    posts_for_like.append(single_post)
                    # if posts_for_like.length == max_like, stop for,
                    # we get all posts for like
                    if len(posts_for_like) == max_likes:
                        break
        # we get all posts for lik, posts_for_like.length == max_like,
        if len(posts_for_like) == max_likes:
            # like all posts in posts_for_like
            for single_post in posts_for_like:
                print('post id for like:', single_post.id)
                Likes.objects.create(post=single_post, user=real_user)
