# tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Authenticate.models import Account
from Core.models import Post, Attachments, Comment, Reviews
from django.core.files.uploadedfile import SimpleUploadedFile
import tempfile
import os

class ForumTests(TestCase):

    def setUp(self):
        # Create a test user and account
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.account = Account.objects.create(Username=self.user, isActive=True, email='testuser@example.com', firstName='Test', lastName='User')
        
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

    def test_forum_view(self):
        # Test the forum view with default sorting
        response = self.client.get(reverse('Public:ForumPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/Forum/Forum.html')

    def test_forum_create_post(self):
        # Test creating a forum post
        title = "Test Title"
        content = "Test Content"

        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            temp_image.write(b'This is a test image')
            temp_image.seek(0)
            response = self.client.post(reverse('Public:ForumCreatePage'), {
                'Title': title,
                'Content': content,
                'Attachments': [SimpleUploadedFile(temp_image.name, temp_image.read())]
            })

        self.assertEqual(response.status_code, 302)  # Redirect after successful post creation
        self.assertTrue(Post.objects.filter(Title=title, Content=content).exists())

    def test_forum_detail_view(self):
        # Test viewing the details of a forum post
        post = Post.objects.create(Profile=self.account, Title="Detail Test Title", Content="Detail Test Content")
        post.save()
        response = self.client.get(reverse('Public:ForumDetailPage', args=[post.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/Forum/ForumDetail.html')

    def test_forum_comment(self):
        # Test commenting on a forum post
        post = Post.objects.create(Profile=self.account, Title="Comment Test Title", Content="Comment Test Content")
        post.save()
        comment_content = "This is a test comment"

        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            temp_image.write(b'This is a test image')
            temp_image.seek(0)
            response = self.client.post(reverse('Public:ForumAddComment', args=[post.slug]), {
                'Content': comment_content,
                'Attachments': [SimpleUploadedFile(temp_image.name, temp_image.read())]
            })

        self.assertEqual(response.status_code, 302)  # Redirect after successful comment creation
        self.assertTrue(Comment.objects.filter(Post=post, Content=comment_content).exists())

    def test_forum_edit(self):
        # Test editing a forum post
        post = Post.objects.create(Profile=self.account, Title="Edit Test Title", Content="Edit Test Content")
        post.save()
        new_title = "Edited Title"
        new_content = "Edited Content"

        with tempfile.NamedTemporaryFile(suffix=".jpg") as temp_image:
            temp_image.write(b'This is a test image')
            temp_image.seek(0)
            response = self.client.post(reverse('Public:ForumEditPage', args=[post.slug]), {
                'Title': new_title,
                'Content': new_content,
                'Attachments': [SimpleUploadedFile(temp_image.name, temp_image.read())]
            })

        self.assertEqual(response.status_code, 302)  # Redirect after successful post edit
        post.refresh_from_db()
        self.assertEqual(post.Title, new_title)
        self.assertEqual(post.Content, new_content)

    def test_forum_delete(self):
        # Test deleting a forum post
        post = Post.objects.create(Profile=self.account, Title="Delete Test Title", Content="Delete Test Content")
        post.save()
        response = self.client.post(reverse('Public:ForumDeletePage', args=[post.slug]))

        self.assertEqual(response.status_code, 302)  # Redirect after successful post deletion
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())

    def test_forum_action_upvote(self):
        # Test upvoting a forum post
        post = Post.objects.create(Profile=self.account, Title="Upvote Test Title", Content="Upvote Test Content")
        post.save()

        response = self.client.post(reverse('Public:ForumActionPage', args=[post.slug]), {
            'Action': 'Upvote'
        })

        self.assertEqual(response.status_code, 302)  # Redirect after upvote action
        post.refresh_from_db()
        self.assertEqual(post.UpvotesCount, 1)
        self.assertTrue(post.Upvotes.filter(pk=self.account.pk).exists())

    def test_forum_action_downvote(self):
        # Test downvoting a forum post
        post = Post.objects.create(Profile=self.account, Title="Downvote Test Title", Content="Downvote Test Content")
        post.save()

        response = self.client.post(reverse('Public:ForumActionPage', args=[post.slug]), {
            'Action': 'Downvote'
        })

        self.assertEqual(response.status_code, 302)  # Redirect after downvote action
        post.refresh_from_db()
        self.assertEqual(post.DownVotesCount, 1)
        self.assertTrue(post.Downvotes.filter(pk=self.account.pk).exists())

class ReviewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.account = Account.objects.create(Username=self.user, email='testuser@example.com', firstName='Test', lastName='User', isActive=True)
        self.review = Reviews.objects.create(Profile=self.account, Content='Great product!', Rating=5)
        self.reviews_url = reverse('Public:ReviewsPage')
        self.reviews_update_url = reverse('Public:ReviewsUpdatePage')

    def test_reviews_func_get_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.reviews_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/Reviews/Reviews.html')
        self.assertIn('isAuthenticated', response.context)
        self.assertTrue(response.context['isAuthenticated'])
        self.assertEqual(response.context['Account'], self.account)
        self.assertEqual(response.context['UserReviews'], self.review)
        # self.assertIn(self.review, response.context['Reviews'])

    def test_reviews_func_get_unauthenticated(self):
        response = self.client.get(self.reviews_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/Reviews/Reviews.html')
        self.assertIn('isAuthenticated', response.context)
        self.assertFalse(response.context['isAuthenticated'])
        self.assertIn(self.review, response.context['Reviews'])

    def test_reviews_update_get_authenticated(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(self.reviews_update_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'Public/Reviews/ReviewsUpdate.html')
        self.assertEqual(response.context['Account'], self.account)
        self.assertEqual(response.context['Reviews'], self.review)

    def test_reviews_update_get_unauthenticated(self):
        response = self.client.get(self.reviews_update_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reviews_url)

    def test_reviews_update_post_authenticated_existing_review(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.reviews_update_url, {
            'Content': 'Updated review content',
            'Rating': 4
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reviews_url)

        updated_review = Reviews.objects.get(Profile=self.account)
        self.assertEqual(updated_review.Content, 'Updated review content')
        self.assertEqual(updated_review.Rating, 4)

    def test_reviews_update_post_authenticated_new_review(self):
        self.review.delete()  # Remove the existing review to test creating a new one
        self.client.login(username='testuser', password='password123')
        response = self.client.post(self.reviews_update_url, {
            'Content': 'New review content',
            'Rating': 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reviews_url)

        new_review = Reviews.objects.get(Profile=self.account)
        self.assertEqual(new_review.Content, 'New review content')
        self.assertEqual(new_review.Rating, 5)

    def test_reviews_update_post_unauthenticated(self):
        response = self.client.post(self.reviews_update_url, {
            'Content': 'Unauthenticated review content',
            'Rating': 3
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.reviews_url)
        self.assertFalse(Reviews.objects.filter(Content='Unauthenticated review content').exists())