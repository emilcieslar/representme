# Create your tests here.
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test.client import Client
from django.contrib.auth.models import User
from representME.models import Law, Topic, Party, Constituency, UserProfile, UserVote, MSP


'''
TEST whether LAW is saved properly
'''
class LawTests(TestCase):

    def setUp(self):
        self.topic = Topic(name='Topic1', description='Description1')
        self.topic.save()

    def test_ensure_law_is_saved_properly(self):

        law = Law(name='ABCD', text='', topic=self.topic, result=Law.CARRIED )
        law.save()

        self.assertEqual(law.name, 'ABCD')
        self.assertEqual(law.text, '')
        self.assertEqual(law.topic, self.topic)
        self.assertEqual(law.score, None)
        self.assertEqual(law.date, None)
        self.assertEqual(law.result, 1)

        law.result = Law.DEFEATED

        self.assertEqual(law.result, 2)

'''
TEST whether Topic is saved properly
'''
class TopicTests(TestCase):

    def test_ensure_topic_is_saved_properly(self):

        topic = Topic(name='Name1', description='Description1')
        topic.save()

        self.assertEqual(topic.name, 'Name1')
        self.assertEqual(topic.description, 'Description1')

'''
TEST whether Party is saved properly
'''
class PartyTests(TestCase):

    def test_ensure_party_is_saved_properly(self):

        party = Party(name='Name1', description='Description1', colour='FFFFFF')
        party.save()

        self.assertEqual(party.name, 'Name1')
        self.assertEqual(party.description, 'Description1')
        self.assertEqual(party.colour, 'FFFFFF')

'''
TEST whether UserProfile is saved properly
'''
class UserProfileTests(TestCase):

    def setUp(self):
        self.user = User(username='user1', password='password', email='test@test.com')
        self.user.save()

    def test_ensure_userprofile_is_saved_properly(self):

        userprofile = UserProfile(postcode='G38QJ', msptype=False, user=self.user)
        userprofile.save()

        self.assertEqual(userprofile.postcode, 'G38QJ')
        self.assertEqual(userprofile.msptype, False)
        self.assertEqual(userprofile.user, self.user)

'''
TEST whether UserVote is saved properly
'''
class UserVoteTests(TestCase):

    def setUp(self):
        self.user = User(username='user1', password='password', email='test@test.com')
        self.user.save()
        self.topic = Topic(name='Topic1', description='Description1')
        self.topic.save()
        self.law = Law(name='ABCD', text='', topic=self.topic, result=Law.CARRIED )
        self.law.save()

    def test_ensure_uservote_is_saved_properly(self):

        uservote = UserVote(user=self.user, law=self.law, vote=True)
        uservote.save()

        self.assertEqual(uservote.user, self.user)
        self.assertEqual(uservote.law, self.law)
        self.assertEqual(uservote.vote, True)

        self.assertEqual(UserVote.is_true(uservote), True)
        self.assertEqual(UserVote.is_false(uservote), False)

'''
TEST whether Constituency is saved properly
'''
class ConstituencyTests(TestCase):

    def test_ensure_constituency_is_saved_properly(self):

        constituency = Constituency(name='name1')
        constituency.save()

        self.assertEqual(constituency.name, 'name1')

'''
TEST whether MSP is saved properly
'''
class MSPTests(TestCase):

    def setUp(self):
        self.constituency = Constituency(name='name1')
        self.constituency.save()
        self.party = Party(name='Name1', description='Description1', colour='FFFFFF')
        self.party.save()

    def test_ensure_msp_is_saved_properly(self):

        msp = MSP(foreignid=1234, constituency=self.constituency, party=self.party, firstname='name1', lastname='lastname1',)
        msp.save()

        self.assertEqual(msp.foreignid, 1234)
        self.assertEqual(msp.constituency, self.constituency)
        self.assertEqual(msp.party, self.party)
        self.assertEqual(msp.firstname, 'name1')
        self.assertEqual(msp.lastname, 'lastname1')


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
