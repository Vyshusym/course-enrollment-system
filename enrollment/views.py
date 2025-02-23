from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .models import Profile, Student, Course
from .forms import ProfileForm, EnrollmentForm

# --- Home and Login Views ---

class HomePageView(TemplateView):
    template_name = "enrollment/home.html"

class CustomLoginView(LoginView):
    template_name = "enrollment/login.html"

# --- Profile Views ---
class CustomLogoutView(LogoutView):
    http_method_names = ['get', 'post']  

    
@login_required
def profile_view(request):
    # If no profile exists, redirect to profile creation.
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect('profile_create')
    
    # If the user has enrolled, get the Student record.
    student = request.user.student if hasattr(request.user, 'student') else None
    return render(request, "enrollment/profile.html", {'profile': profile, 'student': student})

@login_required
def profile_create_view(request):
    # If profile already exists, go to profile page.
    if hasattr(request.user, 'profile'):
        return redirect('profile')
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, "enrollment/profile_form.html", {'form': form})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = "enrollment/profile_update.html"
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

# --- Enrollment Views ---

class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = EnrollmentForm
    template_name = "enrollment/enroll.html"
    success_url = reverse_lazy('enrollment_success')

    def dispatch(self, request, *args, **kwargs):
        # Require that the user has created a profile first.
        if not hasattr(request.user, 'profile'):
            return redirect('profile_create')
        # If already enrolled, redirect to profile.
        if hasattr(request.user, 'student'):
            return redirect('profile')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EnrollmentSuccessView(TemplateView):
    template_name = "enrollment/success.html"

# --- Courses List View ---

class CourseListView(ListView):
    model = Course
    template_name = "enrollment/courses.html"
    context_object_name = "courses"
