__author__ = 'Cristina'

# What tests to run?
tests = ['test1']

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tangowithdjango.settings")
import django

django.setup()
from representME.models import MSP
from data import number_of_msps

'''
Check if the numbers of MSPs match (Db vs data.py)
'''


def test1():
    if MSP.objects.count() == number_of_msps:
        return True
    return False


'''
calls all the functions definitions in the tests list
'''


def main():
    i = 0
    for test in tests:
        if eval(test):
            print "Test " + i.__str__() + " OK"
        else:
            print "Text " + i.__str__() + " FAIL!"


if __name__ == '__main__':
    main()