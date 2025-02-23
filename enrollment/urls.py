from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    HomePageView, CustomLoginView, profile_create_view, profile_view,
    ProfileUpdateView, EnrollmentCreateView, EnrollmentSuccessView, CourseListView, CustomLogoutView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/create/', profile_create_view, name='profile_create'),
    path('profile/', profile_view, name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('enroll/', EnrollmentCreateView.as_view(), name='enroll'),
    path('enroll/success/', EnrollmentSuccessView.as_view(), name='enrollment_success'),
    path('courses/', CourseListView.as_view(), name='courses'),
]
