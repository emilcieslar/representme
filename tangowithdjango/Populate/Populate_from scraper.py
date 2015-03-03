__author__ = '2168879m'
'''
This will delete all tables and populate the following tables:
Law, Topic, Party, Constituency, MSP, MSPVote,
'''

import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tangowithdjango.settings")
from representME.models import *
from data import *
from dateutil import parser


def delete_data():
    Law.objects.all().delete()
    Topic.objects.all().delete()
    Party.objects.all().delete()
    Constituency.objects.all().delete()
    MSP.objects.all().delete()
    MSPVote.objects.all().delete()
    User.objects.all().delete()
    UserVote.objects.all().delete()
    Comment.objects.all().delete()

def populate_constituency():
    with open(settings.STATIC_PATH + '/test_data/districts.csv') as f:
        next(f)
        for line in f:
            line = line.split(',')
            id = int(float(line[0]))
            parent = int(float(line[1]))
            name = line[2].strip(" \"\'\r\n")

            if parent == 0:
                c = Constituency(id=id, parent=None, name=name)
                c.save()

            else:
                pere = Constituency.objects.get(id=parent)
                c = Constituency(id=id, parent=pere, name=name)
                c.save()


def populate_current_msps():
    with open(settings.PROJECT_PATH + '/scraper/msp_scraper/msps.csv', mode='r') as infile:
        reader = csv.reader(infile)
        i = 0
        for row in reader:
            i += 1
            row = row[0].split(';')
            p = Party.objects.get_or_create(name=row[2].strip())[0]
            p.save()
            c = Constituency.objects.get(name=row[3].strip())
            m = MSP(firstname=row[1].strip(), lastname=row[0], constituency=c, party=p, foreignid=i, status=MSP.MEMBER,         # basic data, sufficient to run visualisations & website
                    member_startdate = parser.parse('5 May 2011').date(), member_enddate = parser.parse('5 May 2016').date(),   # (as they should allow nulls for other fields)
                    party_startdate = parser.parse('5 May 2011').date(), party_enddate = parser.parse('5 May 2016').date())     # default ranges, will be overwritten for the few msps that move about
            m.save()


def main():
    delete_data()
    print "All tables empty, will now start populating"

    print "done"
    

if __name__ == '__main__':
    main()    