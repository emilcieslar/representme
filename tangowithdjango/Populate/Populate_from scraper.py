import importlib
from xml.dom import minidom
from django.contrib.staticfiles.utils import get_files
import representME

__author__ = '2168879m'
'''
This will delete all tables and populate the following tables:
Law, Topic, Party, Constituency, MSP, MSPVote,
'''


import csv
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tangowithdjango.settings")
import django
django.setup()
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


def absent_votes(law):
    """
    For each msp that did not express a vote for a division, populate the vote table with an ABSENT vote
    :param division: division instance
    :return:
    """
    # if an msp did not have a vote read, he/she was absent
    # get votes read until now
    votes_read = MSPVote.objects.filter(law=law)
    # get msps that didn't vote
    absentMSPs = MSP.objects.all()
    for vote in votes_read:
        absentMSPs = absentMSPs.exclude(foreignid=int(vote.msp.foreignid))
    # those msps had an absent vote
    for msp in absentMSPs:
        v = MSPVote(msp=msp, law=law, vote=MSPVote.ABSENT)
        v.save()


def get_votes(parsing_law, law, type, result):
    """
    Populates the vote table with result vote, for all votes of some type, from parsing_law, for division
    :param parsing_law : a minidom element from the scraped file
    :param division : the division instance already created for which we are parsing votes
    :param type : the type of vote parsed: "for", "against", "abstention"
    :param result: the type of vote to be saved in the db: "YES", "NO", "ABSENT"
    :return:
    """
    if len(parsing_law.getElementsByTagName(type)):
        msps = parsing_law.getElementsByTagName(type)[0].getElementsByTagName("msp")
        for msp in msps:
            firstname = msp.getElementsByTagName("name")[0].firstChild
            lastname = msp.getElementsByTagName("surname")[0].firstChild
            if firstname and lastname:
                firstname = str(firstname.data)
                lastname = str(lastname.data)
                # check for recorded errors with scraper
                if lastname == 'Mackenzie':
                    lastname = 'MacKenzie'
                if lastname == 'GIBson':
                    lastname = 'Gibson'
                if lastname != 'Copy':
                    try:
                        msp = MSP.objects.get(firstname=firstname, lastname=lastname)
                        v = MSPVote(msp=msp, law=law, vote=result)
                        v.save()
                    except MSP.DoesNotExist:
                        pass


def populate_law(files_location, startdate, enddate):
    """
    reads all files within an interval from a location
    :param files_location : path to the folder where the scraped files are at
    :param startdate : first date for which to read files
    :param enddate : last date for which to read files
    :returns : populates division and vote tables
    """
    currentsession = False

    files = [os.path.join(files_location, f) for f in os.listdir(files_location)]

    for f in files:
        # get date
        doc = minidom.parse(f)
        date = doc.getElementsByTagName("date")[0].firstChild.data
        dt = parser.parse(date).date()
        st = parser.parse(startdate).date()
        ed = parser.parse(enddate).date()
        currentsession = False

        # date between startdate and enddate
        if st <= dt <= ed:
            currentsession = True

        if currentsession:
            laws = doc.getElementsByTagName("law")
            # parse each law
            for lawread in laws:

                motionid = lawread.getElementsByTagName("id")[0].firstChild.data
                # keep only motions
                if not ('.' in motionid):
                    # motiontopic = law.getElementsByTagName("topic")[0].firstChild.data.encode('latin1','backslashreplace').replace("\\u2019", "\'").replace("\\u2014", "-").replace("\u201d", "\"").replace("\u201c", "\"")
                    text_raw = lawread.getElementsByTagName("text")
                    if text_raw == []:
                        text = 'n/a'
                    else:
                        text = text_raw[0].firstChild.data.encode('latin1', 'backslashreplace').replace("\\u2019",
                                                                                                        "\'").replace(
                            "\\u2014", "-").replace("\u201d", "\"").replace("\u201c", "\"")
                    # parsed most info for this law, put it in
                    law = Law(name=motionid, text=text.decode('latin1'), date=dt)
                    # get result for this law
                    yup = lawread.getElementsByTagName("agreed")[0].firstChild
                    if yup:
                        if yup.data == "agreed":
                            law.result = 1
                        else:
                            law.result = 2
                    # get topic for this law
                    extracter = importlib.import_module(topic_extracter_name, topic_extracter_location)
                    topic = extracter.get_topic_from_text(law.text)
                    law.topic = Topic.objects.get(name=topic)
                    # done with division
                    law.save()
                    # read the votes
                    get_votes(lawread, law, "for", MSPVote.YES)
                    get_votes(lawread, law, "against", MSPVote.NO)
                    get_votes(lawread, law, "abstention", MSPVote.ABSTAIN)
                    absent_votes(law)


def populate_topic():
    for topic, description in topics.items():
        t = Topic(name=topic, description=description)
        t.save()


def populate_constituency():
    constituency_path = os.path.join(settings.STATIC_PATH, 'data', 'districts.csv')
    with open(constituency_path) as f:
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
    msps_path = os.path.join(settings.PROJECT_PATH, 'tangowithdjango', 'scraper', 'msp_scraper', 'msps.csv')
    with open(msps_path, mode='r') as infile:
        reader = csv.reader(infile)
        i = 0
        for row in reader:
            i += 1
            row = row[0].split(';')
            party = row[2].strip()
            try:
                p = Party.objects.get(name=party)
            except Party.DoesNotExist:
                p = Party(name=party)
                p.save()
            c = Constituency.objects.get(name=row[3].strip())
            m = MSP(firstname=row[1].strip(), lastname=row[0], constituency=c, party=p, foreignid=i)
            img = msp_img_urls[m.firstname + " " + m.lastname]
            m.img = img
            m.save()


def main():
    delete_data()
    print "All tables empty, will now start populating"
    populate_topic()
    print "Topic table done"
    populate_constituency()
    print "Constituency table done"
    populate_current_msps()
    print "Party table done"
    print "MSP table done"
    populate_law(divisions_location, startdate, enddate)
    print "Law table done"
    print "MSP vote done"
    print "done"


if __name__ == '__main__':
    main()    