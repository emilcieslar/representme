from datetime import datetime, date
from django.shortcuts import render,render_to_response
import json
import re

import requests
from representME.models import Law, Comment, UserVote, Constituency, MSP, UserProfile, MSPVote, Position
from representME.forms import UserForm, UserProfileForm, LawCommentForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from representME.bing_search import run_query
# For the reverse() functionality
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
#from representME.search import generic_search
from itertools import chain


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
    # If user is logged in, load only the user's comments
    if logged_in:
        latest_comments = Comment.objects.filter(user=user).order_by('-time')[:10]
    # Otherwise, load all because we're on the index not logged in page
    else:
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
        context_dict['user_badge'] = computeUserBadge(user)
        for msp in user_msps:
            match = computeMatch(user, msp)
            user_msps_match.append([msp, match])
    else:
        user_msps_match = {}
    context_dict['user_msps_match'] = user_msps_match

    print user_msps_match
    return context_dict


def index(request):

    #if request.user.is_authenticated():
        #return HttpResponseRedirect('/representME/user/'+request.user.username+'/')

    if request.user.is_authenticated():
        return render(request,'representme/index-logged.html',get_index_page(request.user, True))

    return render(request,'representme/index.html', get_index_page(request.user, False))

'''
MSP page
'''
def msp(request, msp_name):
    #assume MSP name is entered as 'firstname_surname'
    names = msp_name.split('-')

    print names[0] + " " + names[1]

    context_dict = {}

    try:
        #try to retrieve MSP with matching first and last name
        msp = MSP.objects.get(firstname__iexact=names[0], lastname__iexact=names[1])

        context_dict['msp'] = msp

        user_msps = []

        #get user's MSPs and store in user_msps
        # you need request.user to access the django user stuff
        if request.user.is_authenticated():

            this_user = UserProfile.objects.get(user=request.user)

            user_msps = get_msps(this_user.postcode)

        else:
            user_msps = []

        #whether it is the user's msp or not
        for user_msp in user_msps:
            if user_msp == msp:
                context_dict['is_my_msp'] = True
                break
            else:
                context_dict['is_my_msp'] = False

        # get laws msp has voted on + excerpts
        laws = []
        #try to get msp votes
        try:
            MSP_votes = MSPVote.objects.filter(msp=msp).exclude(vote=MSPVote.ABSENT)
            for vote in MSP_votes:
                law_excerpt = vote.law.text[:200]
                laws.append([vote, law_excerpt])
        except MSPVote.DoesNotExist:
            pass
        context_dict['msp_laws'] = laws

        positions = []
        try:
            positions = Position.objects.filter(msp=msp)
        except Position.DoesNotExist:
            pass

        print positions
        context_dict['msp_positions'] = positions

    except MSP.DoesNotExist:
        pass

    #not sure what to do if this happens!
    except MSP.MultipleObjectsReturned:
        pass

    print context_dict

    return render(request,'representme/msp.html', context_dict)

def law(request, law_name):
    context_dict = {}

    try:

        law = Law.objects.get(name=law_name)
        comments = Comment.objects.order_by('-time').filter(law=law)
        votes = UserVote.objects.filter(law=law)
        # this is how you get the date today:
        today = date.today()
        context_dict['votes_for'] = votes.filter(vote=True).count()
        context_dict['votes_against'] = votes.filter(vote=False).count()
        context_dict['law'] = law
        context_dict['upcoming'] = "Past" if law.date < today else "Upcoming"
        # this should be taken care of in the template, the information is already in the law, just send the law
        # also, you cannot compare strings in the template, bad bad practice for the future
        # context_dict['law_result'] =  law_result(law)
        context_dict['commentForm'] = LawCommentForm()
        context_dict['comments'] = comments
        context_dict['comments_number'] = comments.count()

        user_msps = {}

        # you need request.user to access the django user stuff
        if request.user.is_authenticated():
            # you use this to get the Userprofile data associated with this user
            this_user = UserProfile.objects.get(user=request.user)
            # -------------------------------------------------------------------------
            # EDIT THIS WHEN CONNECTED TO INTERNET AGAIN
            # -------------------------------------------------------------------------
            # THIS DOES NOT WORK WITHOUT INTERNET CONNECTION
            user_msps = get_msps(this_user.postcode)
        else:
            this_user = -1

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
            pass
    except Law.DoesNotExist:
        pass

    return render(request, 'representme/law.html', context_dict)

"""
Returns the relevant law objects based on the user's search query provided in input "search"
"""
def search(request):
    context_dict = {}

    if request.method == 'POST':

        query_string = request.POST.get('search')

        #split query terms on ' '
        query_terms = query_string.split()

        #create an empty list to store search results for laws
        search_results_laws = list()

        #create an empty list to store search results for MSPs
        search_results_MSPs = list()

        #retrieve results for each query term
        for term in query_terms:

            search_results_laws.extend(list(chain(Law.objects.filter(topic__contains=term),Law.objects.filter(text__contains=term))))
            search_results_MSPs.extend(list(chain(MSP.objects.filter(firstname__contains=term),MSP.objects.filter(lastname__contains=term))))

        context_dict = {'search_results_laws': search_results_laws, 'search_results_MSPs': search_results_MSPs,'query_string': query_string}

        return render(request, 'representme/search.html', context_dict)

    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'representme/search.html', {})


	
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

    return render(request, 'representme/laws.html', context_dict)

def msps(request):
    context_dict = {}

    try:
        msps = MSP.objects.order_by('-lastname')
        context_dict['msps'] = msps;

    except:
        pass

    return render(request, 'representme/msps.html', context_dict)


# DEPRECATED
'''''
@login_required
def userview(request, username):
    context_dict = get_index_page(request.user, True)

    # If user tries to access another users profile, go back to his/her profile
    if username != request.user.username:
        return HttpResponseRedirect('/representME/user/'+request.user.username+'/')

    return render(request, 'representme/index-logged.html', context_dict)
'''''

def user_login(request):
    # Context dict containing errors
    context_dict = {}
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
        # because the request.POST.get('<variable>') returns None, if the value does not exist,
        # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponseRedirect(reverse('index') + '#login-disabled')
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponseRedirect(reverse('index') + '#login-invalid')

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, '/representme/#login', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('index'))

def register(request):

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

            # Set variable that will hold the password that is not encrypted
            # If we use user.password var after set password, it shows only encrypted one
            password = user.password

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

            new_user = authenticate(username=user.username, password=password)

            login(request, new_user)

            # Go to the login page
            return HttpResponseRedirect(reverse('index'))

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            userFormErrors = user_form.errors
            userProfileFormErrors = profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        return HttpResponseRedirect(reverse('index'))

    # Render the template depending on the context.
    return render(request,
            'representme/index.html',
            {'user_form': user_form, 'profile_form': profile_form, 'userFormErrors': userFormErrors, 'userProfileFormErrors': userProfileFormErrors} )


'''
User Vote CLICK
'''
@login_required
def user_vote(request):

    law_id = None
    vote = None

    # If the request method is get, set law_id and vote
    if request.method == 'GET':
        law_id = request.GET['law_id']
        vote = request.GET['vote']

    # Convert vote to proper boolean
    if vote == 'true':
        vote = True
    else:
        vote = False

    # Get law object from database
    law = Law.objects.get(id=int(law_id))

    # If something goes bad, we don't wanna update the HTML
    success = False

    # If law_id was set up correctly
    if law_id:
        # Get the user vote if exists
        user_law_vote = UserVote.objects.filter(user=request.user, law=law)
        # If it exists
        if user_law_vote:
            # Set vote for whatever user voted
            user_law_vote.voted_for = vote
            # Save the model
            user_law_vote.save()
            # We were successful this time!
            success = True
        # Otherwise create a new vote
        else:
            try:
                query = UserVote(user=request.user, law=law, voted=True, vote_for=vote)
                query.save()
                # Again success!
                success = True
            except:
                pass

    # Return whether we were successful or not
    return HttpResponse(success)


'''''
Add comment
'''''
@login_required
def add_comment(request):

    law_id = None
    text = None

    # If the request method is get, set law_id and vote
    if request.method == 'GET':
        law_id = request.GET['law_id']
        text = request.GET['text']

    # Get law object from database
    law = Law.objects.get(id=int(law_id))

    # If something goes bad, we don't wanna update the HTML
    output = False

    # If law_id was set up correctly then we can suppose
    # that text was set up correct as well
    if law_id:
        # Get the user vote if exists
        #user_law_vote = UserVote.objects.filter(user=request.user, law=law)
        # If it exists
        #if user_law_vote:
        #    # Set vote for whatever user voted
        #    user_law_vote.voted_for = vote
        #    # Save the model
        #    user_law_vote.save()
        #    # We were successful this time!
        #    success = True
        # Otherwise create a new vote
        #else:
        try:
            # Save the comment to the database
            query = Comment(user=request.user, law=law, text=text)
            query.save()

            # Save a dictionary of data into output
            # Here we have date, id of the comment and username
            output = json.dumps({"date": query.time.strftime("%d/%m/%Y %H.%M"),
                                 "id": query.id,
                                 "username": request.user.username})
        except:
            pass

        # Return whether we were successful or not
        if output != False:
            # In case of success, return json
            return HttpResponse(output, content_type='application/json; charset=utf8')
        else:
            return HttpResponse(output)

