"""
URL configuration for Knotwork project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Knot import views

urlpatterns = [
    # Public Website
    path('', views.home, name='home'),
    path('explore', views.explore, name='explore'),
    path('skill-exchange', views.skill_exchange, name='skill_exchange'),
    path('how-it-works', views.how_it_works, name='how_it_works'),
    path('mentors', views.mentors, name='mentors'),
    path('communities', views.communities, name='communities'),
    path('pricing', views.pricing, name='pricing'),
    path('about', views.about, name='about'),
    path('blog', views.blog, name='blog'),
    path('help', views.help, name='help'),


    # Authentications
    path('get-started', views.get_started, name='get_started'),
    path('login', views.login, name='login'),

    # Student Urls
    path('student/dashboard', views.student_dashboard, name='student_dashboard'),
    path('student/my-learning', views.student_my_learning, name='student_my_learning'),
    path('student/courses', views.student_find_courses, name='student_find_courses'),
    path('student/skill-matches', views.student_skill_matches, name='student_skill_matches'),
    path('student/browse', views.student_browse, name='student_browse'),
    path('student/my-connections', views.student_my_connections, name='student_my_connections'),
    path('student/requests', views.student_requests, name='student_requests'),
    path('student/messages', views.student_messages, name='student_messages'),
    path('student/sessions', views.student_sessions, name='student_sessions'),
    path('student/community', views.student_community, name='student_community'),
    path('student/progress', views.student_progress, name='student_progress'),
    path('student/achievements', views.student_achievements, name='student_achievements'),
    path('student/credits-and-billing', views.student_credits_and_billing, name='student_credits_and_billing'),
    path('student/settings', views.student_settings, name='student_settings'),
    path('student/help', views.student_help, name='student_help'),
    path('student/profile', views.student_profile, name='student_profile'),
    path('student/logout', views.student_logout, name='student_logout'),
    


    # Student Urls
    path('teacher/dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/logout', views.teacher_logout, name='teacher_logout'),
    path('teacher/atelier', views.teacher_atelier, name='teacher_atelier'),
    path('teacher/cohort', views.teacher_cohort, name='teacher_cohort'),
    path('teacher/studio', views.teacher_studio, name='teacher_studio'),
    path('teacher/grading', views.teacher_grading, name='teacher_grading'),
    path('teacher/assignments', views.teacher_assignments, name='teacher_assignments'),
    path('teacher/seminar', views.teacher_seminar, name='teacher_seminar'),
    path('teacher/messages', views.teacher_messages, name='teacher_messages'),
    path('teacher/enrolments', views.teacher_enrolments, name='teacher_enrolments'),
    path('teacher/network', views.teacher_network, name='teacher_network'),
    path('teacher/reviews', views.teacher_reviews, name='teacher_reviews'),
    path('teacher/analytics', views.teacher_analytics, name='teacher_analytics'),
    path('teacher/honours', views.teacher_honours, name='teacher_honours'),
    path('teacher/earnings', views.teacher_earnings, name='teacher_earnings'),
    path('teacher/settings', views.teacher_settings, name='teacher_settings'),
    path('teacher/help', views.teacher_help, name='teacher_help'),

    path('teacher/my-dossier', views.teacher_dossier, name='teacher_dossier'),


    # Mentor Urls
    path('mentor/dashboard', views.mentor_dashboard, name='mentor_dashboard'),






    # Admin Urls
    path('admin/dashboard', views.admin_dashboard, name='admin_dashboard'),



    # path('admin/', admin.site.urls),

]
