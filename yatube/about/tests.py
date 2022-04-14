# from django.test import TestCase, Client


# class StaticURLTests(TestCase):
#     def setUp(self):
#         # Устанавливаем данные для тестирования
#         # Создаём экземпляр клиента. Он неавторизован.
#         self.guest_client = Client()

#     def test_static_page_about_accessability(self):
#         """Проверка доступности статичной страницы about"""
#         response = self.guest_client.get('/author/')

#         self.assertEqual(response.status_code, 200)

#     def test_static_page_tech_accessability(self):
#         """Проверка доступности статичной страницы tech"""
#         response = self.guest_client.get('/tech/')

#         self.assertEqual(response.status_code, 200)
