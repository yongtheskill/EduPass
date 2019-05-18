from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, logout
from django.urls import reverse_lazy
from django.views import generic


from django.shortcuts import render

import random
import string

import phonenumbers
import boto3


class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def LogIn(request):
    success_url = "/"
    template_name = 'login.html'
    
    def randomString(stringLength=5):
        """Generate a random string of fixed length """
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(stringLength))

    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            phoneNumber = user.student.phoneNumber
            numberList = list(str(phoneNumber))
            numberList[:4] = "****"
            displayNumber = "".join(numberList)
            if user is not None:
                logout(request)
                twoFactorKey = randomString()

                print ("beforeFormat: " + str(phoneNumber))
                print ("afterFormat: " + phonenumbers.format_number(phonenumbers.parse(str(phoneNumber), "SG"), phonenumbers.PhoneNumberFormat.E164))

                
                authMessage = "EduPass Login Two-Factor authentication code for " + username + ": \n" + twoFactorKey

                client = boto3.client(
                    "sns",
                    aws_access_key_id="AKIAQF4IUI6ABXEKSZEE",
                    aws_secret_access_key="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",
                    region_name="us-east-1"
                )

                client.publish(
                    PhoneNumber= phonenumbers.format_number(phonenumbers.parse(str(phoneNumber), "SG"), phonenumbers.PhoneNumberFormat.E164),
                    Message=authMessage,
                    Subject="EduPass Authentication"
                )



                print("2fK: " + twoFactorKey)
                context = {
                    'twoFactorKey': twoFactorKey,
                    'displayNumber': displayNumber,
                    'phoneNumber': phoneNumber,
                    'username': username,
                    'password': password,
                }
                return render(request, 'twoFactor.html', context)

    return render(request, 'login.html')