from django import forms
from .models import Profile, Student, Course

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'current_year_of_study',
            'linkedin',
            'github',
            'phone_number',
            'address',
            'guardian_phone_number'
        ]

class EnrollmentForm(forms.ModelForm):
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        help_text="Select the courses you want to enroll in."
    )
    
    class Meta:
        model = Student
        fields = ['name', 'email', 'courses']
