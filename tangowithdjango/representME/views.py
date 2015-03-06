from django.shortcuts import render
from representME.models import Law,User

# Create your views here.
def index(request):
    context_dict = {'bold_message': "I am bold message"}

    return render(request,'representME/index.html', context_dict)

def law(request, law_name_slug):
    context_dict = {}

    try:
        # instead of name it should be slug, but our db doesn't have a slug yet
        law = Law.objects.get(name=law_name_slug)

        context_dict['law'] = law;
    except Law.DoesNotExist:
        pass

    return render(request, 'representME/law.html', context_dict)

def user(request, username):
    context_dict = {}

    try:
        #userObj = User.objects.get(username=username)

        context_dict['user'] = "";
    except User.DoesNotExist:
        pass

    return render(request, 'representME/index-logged.html', context_dict)