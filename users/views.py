from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import RegistrationForm


def register(request):
    # POST ----------------------------------------------
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            username = registration_form.cleaned_data.get('username')
            raw_password = registration_form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')

    # GET -----------------------------------------------
    else:
        registration_form = RegistrationForm()

    # GET & POST not valid ------------------------------
    return render(request, 'registration.html', {
        'page': 'page-register',
        'form': registration_form,
    })


@login_required
def modify_logged_user(request):
    # POST ----------------------------------------------
    if request.method == 'POST':
        # Check if the user has permission over the game
        user_form = UserForm(request.POST)
        if not user_form.is_valid():
            return HttpResponse(status=400)
        user = user_form.save(commit=False)
        user.save()
        return HttpResponseRedirect('/')

    # GET -----------------------------------------------
    else:
        game_form = GameForm()

    # SHARED --------------------------------------------
    context = {
        'page': 'page-modify-logged-user',
        'gameForm': game_form,
    }
    return render(request, 'new-game.html', context)