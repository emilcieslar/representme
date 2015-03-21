__author__ = 'Cristina'

# What tests to run?
tests = ['test1()', 'test2()', 'test3()', 'test4()', 'test5()', 'test6()', 'test7()']

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tangowithdjango.settings")
import django
django.setup()
from representME.models import Law, Topic, Party, Constituency, MSP, MSPVote, User, UserVote, Comment, Position
from data import number_of_msps, topics, positions

'''
Check if the numbers of MSPs match (Db vs data.py)
'''
def test1():
    if MSP.objects.count() == number_of_msps:
        return True
    return False


'''
Check if Alex Salmond is in (random MSP)
'''


def test2():
    if MSP.objects.filter(lastname='Salmond', firstname='Alex'):
        return True
    return False

'''
Check if there are only 8 regions
'''


def test3():
    if Constituency.objects.filter(parent=None).count() == 8:
        return True
    return False


'''
Check if Glasgow is the parent of Glasgow Kelvin
'''


def test4():
    if Constituency.objects.filter(name='Glasgow'):
        parent = Constituency.objects.filter(name='Glasgow')
        if Constituency.objects.filter(name='Glasgow Kelvin', parent=parent):
            return True
    return False


'''
Check if same number of topic as in data
'''


def test5():
    if Topic.objects.count() == topics.__sizeof__():
        return True
    return False


'''
Check if SNP and independent in Parties
'''


def test6():
    if Party.objects.get(name='Independent') and Party.objects.get(name='Scottish National Party'):
        return True
    return False


def test7():
    if Position.objects.all().count() > 0:
        return True
    return False

'''
calls all the functions definitions in the tests list
'''
def main():
    print Constituency.objects.filter(parent=None).count()
    i = 0
    for test in tests:
        i = i + 1
        if eval(test):
            print "Test " + i.__str__() + " OK"
        else:
            print "Text " + i.__str__() + " FAIL!"
    print "done"


if __name__ == '__main__':
    main()