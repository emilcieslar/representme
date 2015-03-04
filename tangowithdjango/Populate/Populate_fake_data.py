__author__ = '2168879m'

# should the app become functional, this will not be used.
# uses fake data from fake_data (d'oh)

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tangowithdjango.settings")
import django

django.setup()
from representME.models import *
from fake_data import *

'''
This will delete and populate the following tables:
User, UserVote, Comment
'''


def delete_data():
    User.objects.all().delete()
    UserVote.objects.all().delete()
    Comment.objects.all().delete()


def populate_User():
    print "User not yet :("


def populate_UserVote():
    print "UserVote not yet :("


def populate_Comment():
    print "Comment not yet :("

def main():
    delete_data()
    print "All user data deleted, will populate with fake data"
    populate_User()
    print "User table done"
    populate_UserVote()
    print "UserVote table done"
    populate_Comment()
    print "Comment table done"
    print "done"


if __name__ == '__main__':
    main()  