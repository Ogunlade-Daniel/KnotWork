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
from django.conf import settings
from django.conf.urls.static import static
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
    path('student/courses/<str:course_id>/enrol', views.student_enrol_course, name='student_enrol_course'),
    path('student/courses/<str:course_id>/save', views.student_toggle_saved_course, name='student_toggle_saved_course'),
    path('student/skill-matches', views.student_skill_matches, name='student_skill_matches'),
    path('student/browse', views.student_browse, name='student_browse'),
    path('student/browse/<int:user_id>/action', views.student_browse_action, name='student_browse_action'),
    path('student/requests/<int:request_id>/action', views.student_people_request_action, name='student_people_request_action'),
    path('student/my-connections', views.student_my_connections, name='student_my_connections'),
    path('student/requests', views.student_requests, name='student_requests'),
    path('student/messages', views.student_messages, name='student_messages'),
    path('student/sessions', views.student_sessions, name='student_sessions'),
    path('student/sessions/<int:session_id>/action', views.student_session_action, name='student_session_action'),
    path('live/<str:room_id>', views.live_classroom, name='live_classroom'),
    path('student/community', views.student_community, name='student_community'),
    path('student/community/<int:post_id>/action', views.student_community_action, name='student_community_post_action'),
    path('student/community/action', views.student_community_action, name='student_community_action'),
    path('student/progress', views.student_progress, name='student_progress'),
    path('student/achievements', views.student_achievements, name='student_achievements'),
    path('student/credits-and-status', views.student_credits_and_billing, name='student_credits_and_billing'),
    path('student/settings', views.student_settings, name='student_settings'),
    path('student/settings/username-availability', views.student_username_available, name='student_username_available'),
    path('student/help', views.student_help, name='student_help'),
    path('student/help/action', views.student_help_action, name='student_help_action'),
    path('student/profile', views.student_profile, name='student_profile'),
    path('student/logout', views.student_logout, name='student_logout'),
    


    # Student Urls
    path('teacher/dashboard', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/atelier', views.teacher_atelier, name='teacher_atelier'),
    path('teacher/atelier/<str:course_id>/edit', views.teacher_atelier, name='teacher_edit_course'),
    path('teacher/cohort', views.teacher_cohort, name='teacher_cohort'),
    path('teacher/studio', views.teacher_studio, name='teacher_studio'),
    path('teacher/studio/start', views.teacher_start_session, name='teacher_start_session'),
    path('teacher/studio/schedule', views.teacher_schedule_session, name='teacher_schedule_session'),
    path('teacher/studio/recordings/action', views.teacher_recording_action, name='teacher_recording_action'),
    path('teacher/studio/sessions/<int:session_id>/action', views.teacher_session_action, name='teacher_session_action'),
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

    path('teacher/logout', views.teacher_logout, name='teacher_logout'),


    # Mentor Urls
    path('mentor/dashboard', views.mentor_dashboard, name='mentor_dashboard'),
    path('mentor/mentees', views.mentor_mentees, name='mentor_mentees'),
    path('mentor/requests', views.mentor_requests, name='mentor_requests'),
    path('mentor/sessions', views.mentor_sessions, name='mentor_sessions'),
    path('mentor/mentoring-plans', views.mentor_mentoring_plans, name='mentor_mentoring_plans'),
    path('mentor/messages', views.mentor_messages, name='mentor_messages'),
    path('mentor/forum', views.mentor_forum, name='mentor_forum'),
    path('mentor/network', views.mentor_network, name='mentor_network'),
    path('mentor/resources', views.mentor_resources, name='mentor_resources'),
    path('mentor/reviews', views.mentor_reviews, name='mentor_reviews'),
    path('mentor/analytics', views.mentor_analytics, name='mentor_analytics'),
    path('mentor/honours', views.mentor_honours, name='mentor_honours'),
    path('mentor/earnings', views.mentor_earnings, name='mentor_earnings'),
    path('mentor/settings', views.mentor_settings, name='mentor_settings'),
    path('mentor/help', views.mentor_help, name='mentor_help'),
    path('mentor/dossier', views.mentor_dossier, name='mentor_dossier'),
    path('mentor/sign_out', views.mentor_sign_out, name='mentor_sign_out'),





    # Admin Urls
    path('admin/sign_up', views.admin_sign_up, name='admin_sign_up'),
    path('admin/login', views.admin_login, name='admin_login'),
    
    path('admin/dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('admin/live_pulse', views.admin_live_pulse, name='admin_live_pulse'),
    path('admin/analytics', views.admin_analytics, name='admin_analytics'),
    path('admin/members', views.admin_members, name='admin_members'),
    path('admin/verifications', views.admin_verifications, name='admin_verifications'),
    path('admin/roles_and_permissions', views.admin_roles_and_permissions, name='admin_roles_and_permissions'),
    path('admin/invitations', views.admin_invitations, name='admin_invitations'),
    path('admin/courses', views.admin_courses, name='admin_courses'),
    path('admin/moderation', views.admin_moderation, name='admin_moderation'),
    path('admin/reports', views.admin_reports, name='admin_reports'),
    path('admin/finance_and_payouts', views.admin_finance_and_payouts, name='admin_finance_and_payouts'),
    path('admin/announcements', views.admin_announcements, name='admin_announcements'),
    path('admin/support_tickets', views.admin_support_tickets, name='admin_support_tickets'),
    path('admin/audit', views.admin_audit, name='admin_audit'),
    path('admin/integrations', views.admin_integrations, name='admin_integrations'),
    path('admin/signal_tower', views.admin_signal_tower, name='admin_signal_tower'),
    path('admin/settings', views.admin_settings, name='admin_settings'),
    path('admin/profile', views.admin_profile, name='admin_profile'),
    path('admin/billing', views.admin_billing, name='admin_billing'),
    path('admin/status', views.admin_status, name='admin_status'),
    path('admin/help', views.admin_help, name='admin_help'),
    
    path('admin/sign_out', views.admin_sign_out, name='admin_sign_out'),


    # path('admin/', admin.site.urls),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
