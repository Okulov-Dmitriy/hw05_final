from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from ..models import Post, Group, Follow
from django.urls import reverse
from django.core.cache import cache


User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create_user(username='Test_user')
        super().setUpClass()
        cls.group = Group.objects.create(
            title='TEST GROUP',
            slug='test_group'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Test text',
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        cache.clear()
        self.templates_url_guest_client_url = {
            '/': 'posts/index.html',
            f'/group/{PostURLTests.group.slug}/': 'posts/group_list.html',
            f'/profile/{self.user}/': 'posts/profile.html',
            f'/posts/{self.post.pk}/': 'posts/post_detail.html',
        }
        self.templates_url_authorized_client_url = {
            f'/posts/{self.post.pk}/edit/': 'posts/create_post.html',
            '/create/': 'posts/create_post.html',
        }

    def test_url_guest_user(self):
        for adress in self.templates_url_guest_client_url:
            with self.subTest(adress=adress):
                response = self.client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_authorized_client(self):
        for adress in self.templates_url_guest_client_url:
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_404(self):
        response = self.client.get('/some_page_404/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_guest_client_correct_template(self):
        for address, template in self.templates_url_guest_client_url.items():
            with self.subTest(address=address):
                response = self.client.get(address, follow=True)
                self.assertTemplateUsed(response, template)

    def test_urls_authorized_client_correct_template(self):
        for address, template in (
                self.templates_url_authorized_client_url.items()
        ):
            with self.subTest(address=address):
                response = self.authorized_client.get(address, follow=True)
                self.assertTemplateUsed(response, template)

    def test_follow_pages_available(self):
        urls = [
            reverse('posts:profile_follow',
                    kwargs={'username': self.user}),
            reverse('posts:profile_unfollow',
                    kwargs={'username': self.user})
        ]
        for url in urls:
            response = self.authorized_client.post(url)
            with self.subTest(url=url):
                self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_in_feed(self):
        new_author = User.objects.create(username='new_author')
        Follow.objects.create(user=self.user, author=new_author)
        post = Post.objects.create(author=new_author)
        response = self.authorized_client.get(reverse('posts:follow_index'))
        object = response.context.get('page_obj').object_list
        self.assertIn(post, object)
