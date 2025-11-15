from reactpy import component
from frontend.components.counter import Counter
from frontend.components.profile_form import ProfileForm

@component
def App():
    return ProfileForm()