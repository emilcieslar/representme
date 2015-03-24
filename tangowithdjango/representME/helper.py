import re
import json
from datetime import date
from decimal import Decimal

import requests

from models import User, UserVote, UserProfile, MSPVote, MSP, Comment, Law, Constituency, Position
from representME.forms import UserForm, UserProfileForm


__author__ = 'Cristina'


def get_time_tag(law):
    """
    Compares the data of the law to the date of today and returns a tag
    :param law: an object from the Law table
    :return: a string, either "Past" or "Upcoming"
    """
    today = date.today()
    return "Past" if law.date < today else "Upcoming"


def computeMatch(user, msp):
    """
    Assumptions:
     - If the user didn't express any opinions 100%
     - If the MSP was absent, the user Vote cannot be used for the similarity measure
    Method:
     - 'build' two vectors (for all the laws where the user expressed a vote and the msp was present)
     - The similarity measure is the number of matches/ number of votes expressed by the user
    This measure can be further improved in the future, by introducing NLP and ML techniques to predict the users opinion on other laws.
    :param user: A User object
    :param msp: A MSP object
    :return: A value between 0 and 100 representing the percentage of similarity between user and MSP
    """
    try:
        user_votes = UserVote.objects.filter(user=user).exclude(vote=None)
        number_of_dimensions = len(user_votes)
        same = 0
        for vote in user_votes:
            try:
                msp_vote = MSPVote.objects.get(msp=msp, law=vote.law)
                if msp_vote.vote == '4':
                    number_of_dimensions += -1
                elif vote.vote and msp_vote.vote == '1':
                    same += 1
                elif not vote.vote and msp_vote.vote == '2':
                    same += 1
            except MSPVote.DoesNotExist:
                number_of_dimensions += -1
        if number_of_dimensions > 0:
            return 100 * same / Decimal(number_of_dimensions)
    except UserVote.DoesNotExist:
        pass
    return 100


def computeUserBadge(user):
    """
    At the moment the badge is computed based on the number of comments
    In the future this can be extended
    :param user: an object from the User table
    :return: A tag to be used as a user badge
    """
    number_of_comments = Comment.objects.filter(user=user).count()
    if number_of_comments < 5:
        return 'Noob'
    elif number_of_comments < 10:
        return 'Newbie'
    else:
        return 'Master'


def get_laws(request, msp):
    laws = []
    try:
        # Assume laws will continue to be named increasing in number
        # This sorts them new to old
        MSP_votes = MSPVote.objects.filter(msp=msp).exclude(vote=MSPVote.ABSENT).order_by('-law')
        # default, in case sth fails
        if request.user.is_authenticated():
            try:
                user_votes = UserVote.objects.filter(user=request.user)
            except UserVote.DoesNotExist:
                pass
        for vote in MSP_votes:
            law_excerpt = vote.law.text[:200]
            # default, in case sth fails
            user_vote = 'None'
            if request.user.is_authenticated():
                try:
                    user_vote = user_votes.get(law=vote.law)
                except UserVote.DoesNotExist:
                    pass
            laws.append([vote, law_excerpt, user_vote])
    except MSPVote.DoesNotExist:
        pass
    return laws


def get_positions(msp):
    positions = []
    try:
        positions = Position.objects.filter(msp=msp)
    except Position.DoesNotExist:
        pass
    return positions


def get_score(msp):
    # this needs to be rewritten
    all_users = User.objects.all()
    this_msp_users = []
    for user in all_users:
        try:
            user_profile = UserProfile.objects.get(user=user)
            if msp in get_msps(user_profile.postcode):
                this_msp_users.append(user)
        except:  # no postcode
            pass
    if len(this_msp_users) > 0:
        return round(sum([computeMatch(user, msp) for user in this_msp_users]) / len(this_msp_users), 2)
    return 0


def get_vote_is_msp(user, law):
    vote = MSPVote.ABSENT
    try:
        msp = MSP.objects.get(firstname=user.first_name, lastname=user.last_name)
        try:
            vote = MSPVote.objects.get(msp=msp, law=law)
        except MSPVote.DoesNotExist:
            pass
    except MSP.DoesNotExist:
        pass
    return vote


def get_index_page(user, logged_in):
    """
    this is used for both possible index pages (not logged in and logged in)
    :param user: A user instance (or null)
    :param logged_in: boolean which is True if the user is logged in
    :return: The data for the index page
    """
    context_dict = {}
    latest_laws_results = []
    latest_laws = Law.objects.order_by('-date')[:10]

    # for each of those laws get the excerpt and add the pair to the dictionary to be returned
    for law in latest_laws:
        law_excerpt = law.text[:200]
        latest_laws_results.append([law, law_excerpt])

    latest_comments_results = []
    # If user is logged in, load only the user's comments
    if logged_in:
        latest_comments = Comment.objects.filter(user=user).order_by('-time')[:10]

    # Otherwise, load all because we're on the index not logged in page
    else:
        latest_comments = Comment.objects.order_by('-time')[:10]
        # Also save a variable that will let base.html know that we are on index without logged in
        context_dict['is_index'] = True

    for comment in latest_comments:
        comment_excerpt = comment.text[:200]
        latest_comments_results.append([comment, comment_excerpt])

    context_dict['latest_laws'] = latest_laws_results
    context_dict['latest_comments'] = latest_comments_results
    context_dict['user_form'] = UserForm()
    context_dict['profile_form'] = UserProfileForm()

    # you need request.user to access the django user stuff
    if logged_in:
        this_user = UserProfile.objects.get(user=user)
        user_msps = get_msps(this_user.postcode)
        user_msps_match = []
        context_dict['user_badge'] = computeUserBadge(user)
        for msp in user_msps:
            match = computeMatch(user, msp)
            user_msps_match.append([msp, match])
    else:
        user_msps_match = {}
    context_dict['user_msps_match'] = user_msps_match

    return context_dict


# Code reused from https://github.com/MostlyScottishPolitics/MostlyScottishP
def is_valid(postcode):
    """
    check if parameter provided could be a postcode
    :param postcode:
    :return:True or False
    """
    postcode = postcode.upper()
    postcode = re.sub('\s+', '', postcode)
    inward = 'ABDEFGHJLNPQRSTUWXYZ'
    fst = 'ABCDEFGHIJKLMNOPRSTUWYZ'
    sec = 'ABCDEFGHJKLMNOPQRSTUVWXY'
    thd = 'ABCDEFGHJKSTUW'
    fth = 'ABEHMNPRVWXY'

    return None != (re.match('[%s][1-9]\d[%s][%s]$' % (fst, inward, inward), postcode) or
                    re.match('[%s][1-9]\d\d[%s][%s]$' % (fst, inward, inward), postcode) or
                    re.match('[%s][%s]\d\d[%s][%s]$' % (fst, sec, inward, inward), postcode) or
                    re.match('[%s][%s][1-9]\d\d[%s][%s]$' % (fst, sec, inward, inward), postcode) or
                    re.match('[%s][1-9][%s]\d[%s][%s]$' % (fst, thd, inward, inward), postcode) or
                    re.match('[%s][%s][1-9][%s]\d[%s][%s]$' % (fst, sec, fth, inward, inward), postcode))


# Code reused from https://github.com/MostlyScottishPolitics/MostlyScottishP
def get_constituencies(postcode):
    """
    request regions mapit.mysociety.org for the given postcode
    :param postcode:
    :return:dictionary
    """
    if not is_valid(postcode):
        return {'ERROR': "Invalid postcode."}

    r = requests.get("http://mapit.mysociety.org/postcode/" + postcode)
    if r.status_code != 200:
        return {'ERROR': "There was an error looking up that postcode."}

    data = json.loads(r.content)
    areas = data['areas']
    regions = {}
    for item in areas:
        if areas[item]['type_name'].startswith("Scottish Parliament constituency"):
            regions['constituency'] = [str(areas[item]['name'])]
        if areas[item]['type_name'].startswith("Scottish Parliament region"):
            regions['region'] = [str(areas[item]['name'])]

    return regions


# Code reused from https://github.com/MostlyScottishPolitics/MostlyScottishP
def get_msps(postcode):
    """
    search the database for msps for each constituency received from get_constituencies
    :param postcode:
    :return:list of msps
    """
    regions = get_constituencies(postcode)
    if regions.has_key('ERROR'):
        return regions

    print regions
    msps = []
    for item in regions:
        const = Constituency.objects.filter(name=regions[item][0])
        for c in const:
            msps_const = MSP.objects.filter(constituency=c.id)
            for msp in msps_const:
                msps.append(msp)
    return msps
