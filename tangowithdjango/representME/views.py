from django.shortcuts import render
from representME.models import Law,User

# Create your views here.
def index(request):
    context_dict = {'bold_message': "I am bold message"}

    return render(request,'representME/index.html', context_dict)

def law(request, law_name):
    context_dict = {}
    print law_name
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


def user(request, username):
    context_dict = {}

    try:
        #userObj = User.objects.get(username=username)

        context_dict['user'] = "";
    except User.DoesNotExist:
        pass

    return render(request, 'representME/index-logged.html', context_dict)