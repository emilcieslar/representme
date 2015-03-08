from datetime import datetime, date
from django.shortcuts import render
import json
import re

import requests
from representME.models import Law, Comment, UserVote, Constituency, MSP, UserProfile, MSPVote
from representME.forms import UserForm, UserProfileForm, LawCommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def computeMatch(user, msp):
    return 0


# this is bulshit, someone write this
def computeUserBadge(user):
    number_of_comments = Comment.objects.filter(user=user).count()
    if number_of_comments < 5:
        return 'Noob'
    elif number_of_comments < 10:
        return 'Newbie'
    else:
        return 'Master'


def get_index_page(user, logged_in):
    context_dict = {}
    # have an empty dictionary that will contain tuples
    latest_laws_results = []
    # get latest 10 laws, here you change the number of laws needed on index page
    latest_laws = Law.objects.order_by('-date')[:10]
    # for each of those laws get the excerpt and add the pair to the dictionary to be returned
    # here you can control the length of the excerpt
    for law in latest_laws:
        law_excerpt = law.text[:200]
        latest_laws_results.append([law, law_excerpt])

    # same for comments
    latest_comments_results = []
    latest_comments = Comment.objects.order_by('-time')[:10]
    for comment in latest_comments:
        comment_excerpt = comment.text[:200]
        latest_comments_results.append([comment, comment_excerpt])


    context_dict['latest_laws'] = latest_laws_results
    context_dict['latest_comments'] = latest_comments_results
    context_dict['user_form'] = UserForm()
    context_dict['profile_form'] = UserProfileForm()

    # you need request.user to access the django user stuff
    if logged_in:
        # you use this to get the Userprofile data associated with this user
        this_user = UserProfile.objects.get(user=user)
        user_msps = get_msps(this_user.postcode)
        user_msps_match = []
        for msp in user_msps:
            match = computeMatch(user, msp)
            user_msps_match.append([msp, match])
    else:
        user_msps_match = {}
    context_dict['user_msps_match'] = user_msps_match
    context_dict['user_badge'] = computeUserBadge(user)
    print user_msps_match
    return context_dict


def index(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/representME/user/'+request.user.username+'/')

    context_dict = get_index_page(request.user, False)

    return render(request,'representME/index.html', context_dict)

def law(request, law_name):
    context_dict = {}

    try:

        law = Law.objects.get(name=law_name)
        comments = Comment.objects.order_by('-time').filter(law=law)
        votes = UserVote.objects.filter(law=law, voted=True)
        # this is how you get the date today:
        today = date.today()
        context_dict['votes_for'] = votes.filter(vote_for=True).count()
        context_dict['votes_against'] = votes.filter(vote_for=False).count()
        context_dict['law'] = law
        context_dict['upcoming'] = "Past" if law.date < today else "Upcoming"
        # this should be taken care of in the template, the information is already in the law, just send the law
        # also, you cannot compare strings in the template, bad bad practice for the future
        # context_dict['law_result'] =  law_result(law)
        context_dict['commentForm'] = LawCommentForm()
        context_dict['comments'] = comments
        context_dict['comments_number'] = comments.count()

        # you need request.user to access the django user stuff
        if request.user.is_authenticated():
            # you use this to get the Userprofile data associated with this user
            this_user = UserProfile.objects.get(user=request.user)
            user_msps = get_msps(this_user.postcode)
        else:
            user_msps = {}

        # have an empty dictionary that will contain tuples
        user_msps_results = []
        # for each of those user_msps get the vote for this law and add the pair to the dictionary to be returned
        for msp in user_msps:
            try:
                msp_vote = MSPVote.objects.get(msp=msp, law=law)
            except MSPVote.DoesNotExist:
                msp_vote = ''
            user_msps_results.append([msp, msp_vote])

        # might get error in templates if db is not complete and an MSP vote is ''
        # delete this and the print once it is tested
        print user_msps_results

        context_dict['user_msps'] = user_msps_results

        context_dict['user_vote'] = ''
        try:
            context_dict['user_vote'] = UserVote.objects.get(user=this_user, law=law)
        except UserVote.DoesNotExist:
            context_dict['user_vote'] = ''
    except Law.DoesNotExist:
        pass

    return render(request, 'representME/law.html', context_dict)

#From Cristina's previous project
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

#From Cristina's previous project
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

#From Cristina's previous project
def get_msps(postcode):
    """
    search the database for msps for each constituency received from get_constituencies
    :param postcode:
    :return:dictionary
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

def laws(request):
    context_dict = {}

    try:
        laws = Law.objects.order_by('-date')
        context_dict['laws'] = laws

    except:
        pass

    return render(request, 'representME/laws.html', context_dict)

def msps(request):
    context_dict = {}

    try:
        msps = MSP.objects.order_by('-lastname')
        context_dict['msps'] = msps;

    except:
        pass

    return render(request, 'representME/msps.html', context_dict)

@login_required
def userview(request, username):
    context_dict = get_index_page(request.user, True)

    try:
        userObj = User.objects.get(username=username)
        context_dict['user'] = userObj
    except User.DoesNotExist:
        pass

    return render(request, 'representME/index-logged.html', context_dict)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    userFormErrors = False
    userProfileFormErrors = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

            return HttpResponseRedirect('/representME/user/'+user.username+'/')

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            userFormErrors = user_form.errors
            userProfileFormErrors = profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        return HttpResponseRedirect('/representME/')

    # Render the template depending on the context.
    return render(request,
            'representME/index.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered, 'userFormErrors': userFormErrors, 'userProfileFormErrors': userProfileFormErrors} )