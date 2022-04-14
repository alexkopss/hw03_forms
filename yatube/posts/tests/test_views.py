from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms

from posts.models import Post, Group

User = get_user_model()


class PostPagesTests(TestCase):
    """Тестирование страниц во вью-функциях в приложении Posts"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='SomeUser')
        cls.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='Something'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group
        )
        cls.group_1 = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='test_group'
        )

    def setUp(self):
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_in_the_right_group(self):
        """ Проверяем что пост попал в нужную группу """
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'Something'}))
        self.assertEqual(len(response.context['page_obj']), 1)

    def test_post_not_in_the_other_group(self):
        """ Проверяем что пост не попал в другую группу """
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test_group'}))
        self.assertEqual(len(response.context['page_obj']), 0)

    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'posts/index.html': reverse('posts:main'),
            'posts/group_list.html': reverse(
                'posts:group_list', kwargs={'slug': 'Something'}
            ),
            'posts/profile.html': reverse(
                'posts:profile', kwargs={'username': 'StasBasov'}
            ),
            'posts/post_detail.html': reverse(
                'posts:post_detail', kwargs={'post_id': '1'}
            ),
            'posts/post_create.html': reverse('posts:post_create'),

        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template) 

    def test_create_page_show_correct_context(self):
        """Шаблон create сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)

    def test_edit_page_show_correct_context(self):
        """Шаблон edit сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': self.post.pk}
        ))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Проверяет, что поле формы является экземпляром
                # указанного класса
                self.assertIsInstance(form_field, expected)


class PaginatorViewsTest(TestCase):
    """Тест паджинатора страниц"""
    def setUp(self):
        self.user = User.objects.create_user(username='StasBasov')
        self.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='Something'
        )
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for i in range(13):
            Post.objects.create(
                author=self.user,
                text='(Тестовый текст)*i',
                group=self.group,
            )

    def test_first_page_contains_ten_records_index(self):
        """Тестируем первую страницу главной страницы"""
        response = self.client.get(reverse('posts:main'))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records_index(self):
        """Тестируем вторую страницу главной страницы"""
        response = self.client.get(reverse('posts:main') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_page_contains_ten_records_group_list(self):
        """Тестируем первую страницу group_ist"""
        response = self.client.get(reverse(
            'posts:group_list', kwargs={'slug': 'Something'}
        ))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records_group_list(self):
        """Тестируем вторую страницу траницу group_ist"""
        response = self.client.get(reverse(
            'posts:group_list', kwargs={'slug': 'Something'}
        ) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)

    def test_first_page_contains_ten_records_profile(self):
        """Тестируем первую страницу gprofile"""
        response = self.client.get(reverse(
            'posts:profile', kwargs={'username': 'StasBasov'}
        ))
        self.assertEqual(len(response.context['page_obj']), 10)

    def test_second_page_contains_three_records_profile(self):
        """Тестируем вторую страницу траницу profile"""
        response = self.client.get(reverse(
            'posts:profile', kwargs={'username': 'StasBasov'}
        ) + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 3)


class YatubePagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='SomeUser')
        cls.group = Group.objects.create(
            title='Тестовый заголовок группы',
            slug='Something',
            description='Тестовое описание'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый текст',
            group=cls.group
        )

    def setUp(self):
        self.user = User.objects.create_user(username='StasBasov')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_home_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:main'))
        first_object = response.context['page_obj'][0]
        task_title_0 = first_object.author.username
        task_text_0 = first_object.text
        task_slug_0 = first_object.group.title
        task_description_0 = first_object.group.description
        self.assertEqual(task_title_0, 'SomeUser')
        self.assertEqual(task_text_0, 'Тестовый текст')
        self.assertEqual(task_slug_0, 'Тестовый заголовок группы')
        self.assertEqual(task_description_0, 'Тестовое описание')

    def test_group_list_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'Something'}
        ))
        first_object = response.context['page_obj'][0]
        title_1 = first_object.author.username
        text_1 = first_object.text
        tslug_1 = first_object.group.title
        description_1 = first_object.group.description
        self.assertEqual(title_1, 'SomeUser')
        self.assertEqual(text_1, 'Тестовый текст')
        self.assertEqual(tslug_1, 'Тестовый заголовок группы')
        self.assertEqual(description_1, 'Тестовое описание')

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'SomeUser'}
        ))
        first_object = response.context['page_obj'][0]
        title_2 = first_object.author.username
        text_2 = first_object.text
        tslug_2 = first_object.group.title
        description_2 = first_object.group.description
        self.assertEqual(title_2, 'SomeUser')
        self.assertEqual(text_2, 'Тестовый текст')
        self.assertEqual(tslug_2, 'Тестовый заголовок группы')
        self.assertEqual(description_2, 'Тестовое описание')

    def test_post_detail_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': self.post.pk}
        ))
        self.assertEqual(response.context.get('post').text, self.post.text)

    
