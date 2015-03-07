from django.shortcuts import render
from representME.models import Law
from representME.forms import UserForm, UserProfileForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context_dict = {}

    context_dict['user_form'] = UserForm()
    context_dict['profile_form'] = UserProfileForm()

    return render(request,'representME/index.html', context_dict)

def law(request, law_name):
    context_dict = {}

    try:

        law = Law.objects.get(name=law_name)

        context_dict['law'] = law;
        context_dict['law_result'] = law_result(law)

    except Law.DoesNotExist:
        pass

    return render(request, 'representME/law.html', context_dict)

def law_result(law):
    if law.result == "1":
        return "Carried"
    elif law.result == "0":
        return "Refused"
    else:
        return "None"

def laws_result(laws):
    for law in laws:
        if law.result == "1":
            law.result = "Carried"
        elif law.result == "0":
            law.result = "Refused"
        else:
            law.result = "None"
    return laws

def laws(request):
    context_dict = {}

    try:
        laws = Law.objects.order_by('-date')
        context_dict['laws'] = laws_result(laws)

    except:
        pass

    return render(request, 'representME/laws.html', context_dict)

@login_required
def user(request, username):
    context_dict = {}

    try:
        #userObj = User.objects.get(username=username)

        context_dict['user'] = "";
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