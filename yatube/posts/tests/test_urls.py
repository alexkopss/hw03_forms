from django.contrib.auth import get_user_model
from django.test import TestCase, Client

from posts.models import Post, Group

User = get_user_model()


class StaticURLTests(TestCase):
    """Тестирование статичных страниц"""
    def setUp(self):
        self.guest_client = Client()

    def test_homepage(self):
        """Проверка доступности домашней страницы неавторизованному
        пользователю"""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_static_page_accessability_and_template(self):
        """Проверка статичных страниц"""
        templates_urls = {
            '/about/author/': 'about/author.html',
            '/about/tech/': 'about/tech.html',
        }
        for url, template in templates_urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)


class PostUrlsTests(TestCase):
    """Тестирование URLs в приложении Posts"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.post = Post.objects.create(
            author=User.objects.create_user(username='SomeUser'),
            text='Тестовый текст'
        )
        cls.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='Something'
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.author_client = Client()
        self.author_client.force_login(self.post.author)

    def test_page_accessability_and_template_client(self):
        """Проверка доступности и шаблонов всех страниц для гостя"""
        templates_urls = {
            '/group/Something/': 'posts/group_list.html',
            '/profile/HasNoName/': 'posts/profile.html',
            '/posts/1/': 'posts/post_detail.html',
        }
        for url, template in templates_urls.items():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_page_accessability_and_template_auth_client(self):
        """Проверка доступности и шаблонов всех страниц для авторизованного"""
        templates_urls = {
            '/create/': 'posts/post_create.html',
        }
        for url, template in templates_urls.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)

    def test_page_accessability_and_template_author(self):
        """Проверка доступности и шаблонов всех страниц для автора поста"""
        templates_urls = {
            '/posts/1/edit/': 'posts/post_create.html',
        }
        for url, template in templates_urls.items():
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, template)
