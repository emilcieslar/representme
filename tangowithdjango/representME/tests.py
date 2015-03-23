# Create your tests here.
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



class IndexTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_index_access(self):
        response = self.c.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

class MSPsTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_msps_access(self):
        response = self.c.get(reverse('msps'))
        self.assertEqual(response.status_code, 200)

class MSPTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_msp_access(self):
        response = self.c.get(reverse('msp', args=('bob-doris',)))
        self.assertEqual(response.status_code, 200)

class LawsTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_laws_access(self):
        response = self.c.get(reverse('laws'))
        self.assertEqual(response.status_code, 200)

class LawTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_law_access(self):
        response = self.c.get(reverse('law', args=('S4M-11507',)))
        self.assertEqual(response.status_code, 200)

class SearchTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_search_access(self):
        response = self.c.get(reverse('search'))
        self.assertEqual(response.status_code, 200)

    #def test_search_msp(self):


class AboutTest(TestCase):

    def setUp(self):
        self.c = Client()

    def test_about_access(self):
        response = self.c.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

class AddCommentTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    # Only logged in user can access
    def test_add_comment_access(self):
        response = self.c.get(reverse('add_comment'))
        self.assertEqual(response.status_code, 302)

    # Only logged in user can access
    def test_add_comment_access_logged_in(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('add_comment'), {'law_id': '', 'text': '', 'comment_id':''})
        self.assertEqual(response.status_code, 200)

class UserVoteTest(TestCase):

    def setUp(self):
        self.c = Client()

    # Only logged in user can access
    def test_user_vote_access(self):
        response = self.c.get(reverse('user_vote'))
        self.assertEqual(response.status_code, 302)


class LogoutTest(TestCase):

    def setUp(self):
        self.c = Client()

    # Only logged in user can access
    def test_logout_access(self):
        response = self.c.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
