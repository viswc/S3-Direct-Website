# tests.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from Authenticate.models import Account
from Core.models import Post, Attachments, Comment
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
