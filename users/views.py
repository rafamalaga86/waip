from .forms import RegistrationForm, ProfileForm, PasswordForm
from django.contrib import messages
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from games.utils import get_menus_data


def register(request):
    # POST ----------------------------------------------
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        if registration_form.is_valid():
            user = registration_form.save()
            login(request, user)
            return redirect('home')

    # GET -----------------------------------------------
    else:
        registration_form = RegistrationForm()

    # GET & POST not valid ------------------------------
    return render(request, 'registration.html', {
        'page': 'page-register',
        'menu_data_hide': True,
        'registration_form': registration_form,
    })


@login_required
def modify_logged_user(request):
    profile_form = None
    password_form = None
    # POST ----------------------------------------------
    if request.method == 'POST':
        if request.POST.get('user_info_change') == 'change_profile':
            # Change profile
            user_form = ProfileForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Your user information was successfully updated')
                return HttpResponseRedirect('/')

        if request.POST.get('user_info_change') == 'change_password':
            # Change the password
            password_form = PasswordForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect('/')

    # GET -----------------------------------------------
    else:
        profile_form = ProfileForm(initial=model_to_dict(request.user))
        password_form = PasswordForm(request.user)

    # SHARED --------------------------------------------
    return render(request, 'profile.html', {
        'page': 'page-modify-logged-user',
        'menu_data': get_menus_data(request.user.id),
        'profile_form': profile_form if profile_form is not None else ProfileForm(initial=model_to_dict(request.user)),
        'password_form': password_form if password_form is not None else PasswordForm(request.user),
    })
