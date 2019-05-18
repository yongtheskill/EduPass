from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, logout
from django.urls import reverse_lazy
from django.views import generic


from django.shortcuts import render

import random
import string


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
            if user is not None:
                logout(request)
                twoFactorKey = randomString()
                print(twoFactorKey)
                context = {
                    'twoFactorKey': twoFactorKey,
                    'username': username,
                    'password': password,
                }
                return render(request, 'twoFactor.html', context)

    return render(request, 'login.html')