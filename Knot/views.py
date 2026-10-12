from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Count, Prefetch, Q, Sum
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib import messages, auth
from django.contrib.auth import login as auth_login
from .forms import CourseForm, LoginForm, OnboardingForm
from .models import (
    Mentor,
    MentorPrivate,
    OnboardingProfile,
    Enrollment,
    Course,
    Student,
    StudentPrivate,
    Teacher,
    TeacherPrivate,
    SavedCourse,
    Certificate,
    LearningDeadline,
    WeeklyGoal,
    LearningSession,
    SessionHand,
    StudioRecording,
    SessionAttendance,
    SessionNote,
    SessionParticipant,
    PeopleRequest,
    CommunityPost,
    CommunityPollOption,
    CommunityPollVote,
    CommunityReply,
    CommunityReaction,
    CommunityBookmark,
    SupportTicket,
    HelpfulnessFeedback,
)


ROLE_DASHBOARD_MAP = {
    'student': 'student_dashboard',
    'teacher': 'teacher_dashboard',
    'mentor': 'mentor_dashboard',
}


def redirect_user_by_role(user):
    profile = getattr(user, 'onboarding_profile', None)
    role = getattr(profile, 'role', 'student')
    dashboard = ROLE_DASHBOARD_MAP.get(role, 'student_dashboard')
    return redirect(dashboard)




def home(request):
    return render(request, 'Knot_Base/index.html')

def explore(request):
    context = {
        'topics': [
            {'name': 'Design & UX', 'icon': 'bi bi-bezier2', 'description': 'Shape clearer products, interfaces, and experiences.', 'count': '48'},
            {'name': 'Technology', 'icon': 'bi bi-code-slash', 'description': 'Build with Python, web tools, data, and AI.', 'count': '72'},
            {'name': 'Business', 'icon': 'bi bi-graph-up-arrow', 'description': 'Turn ideas into durable, useful ventures.', 'count': '36'},
            {'name': 'Languages', 'icon': 'bi bi-translate', 'description': 'Practice conversation with people who get it.', 'count': '29'},
            {'name': 'Creative Arts', 'icon': 'bi bi-palette', 'description': 'Make room for writing, music, and visual work.', 'count': '54'},
            {'name': 'Wellbeing', 'icon': 'bi bi-heart-pulse', 'description': 'Build habits that support a fuller life.', 'count': '31'},
        ],
        'mentors': [
            {'initials': 'AM', 'name': 'Amina Mensah', 'title': 'Product Designer', 'focus': 'Design systems', 'rating': '4.9', 'sessions': '86'},
            {'initials': 'JR', 'name': 'Jonah Reed', 'title': 'Software Engineer', 'focus': 'Python & APIs', 'rating': '4.8', 'sessions': '64'},
            {'initials': 'LK', 'name': 'Lena Kim', 'title': 'Brand Strategist', 'focus': 'Story & strategy', 'rating': '5.0', 'sessions': '51'},
        ],
        'communities': [
            {'icon': 'bi bi-brush', 'name': 'Creative Practice', 'description': 'A generous studio for sharing work, process, and feedback.', 'members': '1.8k'},
            {'icon': 'bi bi-terminal', 'name': 'Builders Lab', 'description': 'Ship small projects and learn from the people making them.', 'members': '2.4k'},
            {'icon': 'bi bi-globe2', 'name': 'Language Exchange', 'description': 'Keep conversations flowing across cultures and time zones.', 'members': '3.1k'},
        ],
    }
    return render(request, 'Knot_Base/explore.html', context)

def skill_exchange(request):
    context = {
        'exchange_topics': [
            'Python', 'UI/UX Design', 'Spanish', 'Public Speaking',
            'Photography', 'Data Analysis', 'Writing', 'Marketing',
        ],
        'match': {
            'score': '94%',
            'partner_initials': 'SR',
            'partner_name': 'Sarah Robinson',
            'partner_role': 'Product Designer',
            'partner_teaches': 'UI/UX Design',
            'partner_wants': 'Python',
        },
    }
    return render(request, 'Knot_Base/skill_exchange.html', context)

def how_it_works(request):
    return render(request, 'Knot_Base/how_it_works.html')

def mentors(request):
    context = {
        'mentors': [
            {'initials': 'AR', 'name': 'Aria Reyes', 'title': 'UX Designer', 'bio': 'Makes complex products feel clear and human.', 'skills': ['UX', 'Figma', 'Research'], 'rating': '4.9', 'reviews': '87', 'sessions': '14', 'tone': 'lime'},
            {'initials': 'MC', 'name': 'Marcus Chen', 'title': 'Data Scientist', 'bio': 'Turns messy questions into useful models and stories.', 'skills': ['Python', 'ML', 'SQL'], 'rating': '4.8', 'reviews': '124', 'sessions': '22', 'tone': 'sky'},
            {'initials': 'SP', 'name': 'Sofia Patel', 'title': 'Writer & Language Coach', 'bio': 'Helps ideas find their voice in English and Spanish.', 'skills': ['Writing', 'Spanish', 'Storytelling'], 'rating': '4.7', 'reviews': '56', 'sessions': '9', 'tone': 'sun'},
            {'initials': 'TK', 'name': 'Tom Kim', 'title': 'Web Developer', 'bio': 'Builds practical web skills one friendly session at a time.', 'skills': ['React', 'Node', 'TypeScript'], 'rating': '4.9', 'reviews': '103', 'sessions': '18', 'tone': 'blue'},
            {'initials': 'NB', 'name': 'Nia Brooks', 'title': 'Brand Strategist', 'bio': 'Finds the sharpest story inside an ambitious idea.', 'skills': ['Branding', 'Strategy', 'Research'], 'rating': '5.0', 'reviews': '41', 'sessions': '12', 'tone': 'lime'},
            {'initials': 'DA', 'name': 'Diego Alvarez', 'title': 'Photography Mentor', 'bio': 'Teaches you to notice light, composition, and the moment.', 'skills': ['Photo', 'Light', 'Editing'], 'rating': '4.9', 'reviews': '68', 'sessions': '16', 'tone': 'sky'},
        ],
    }
    return render(request, 'Knot_Base/mentors.html', context)

def communities(request):
    context = {
        'communities': [
            {'icon': 'bi bi-code-square', 'name': 'Dev Collective', 'description': 'Share code, review projects, and learn new frameworks with developers at every level.', 'members': '1,284', 'topic': 'Technology', 'activity': '28 conversations today', 'tone': 'sky'},
            {'icon': 'bi bi-palette', 'name': 'Design Guild', 'description': 'Get thoughtful critiques, trade workflows, and learn the systems behind great products.', 'members': '856', 'topic': 'Design', 'activity': '14 conversations today', 'tone': 'lime'},
            {'icon': 'bi bi-brain', 'name': 'Mindful Makers', 'description': 'A gentle space for meditation, journaling, creative practice, and balanced routines.', 'members': '642', 'topic': 'Wellbeing', 'activity': '9 conversations today', 'tone': 'sun'},
            {'icon': 'bi bi-translate', 'name': 'Language Exchange', 'description': 'Keep conversations flowing across cultures with friendly practice partners.', 'members': '3,108', 'topic': 'Languages', 'activity': '36 conversations today', 'tone': 'sky'},
            {'icon': 'bi bi-camera', 'name': 'Lens & Light', 'description': 'Talk composition, editing, and the small choices that make an image feel alive.', 'members': '734', 'topic': 'Creative Arts', 'activity': '11 conversations today', 'tone': 'lime'},
            {'icon': 'bi bi-briefcase', 'name': 'Builders Network', 'description': 'Turn early ideas into useful projects with accountability, feedback, and shared momentum.', 'members': '1,972', 'topic': 'Business', 'activity': '22 conversations today', 'tone': 'sun'},
        ],
    }
    return render(request, 'Knot_Base/communities.html', context)

def pricing(request):
    context = {
        'plans': [
            {'name': 'Starter', 'price': '$0', 'description': 'Begin your exchange with the essentials.', 'features': ['Skill exchange', 'Basic matching', 'Join 3 communities', 'Messaging and chat']},
            {'name': 'Pro', 'price': '$12', 'description': 'For serious learners and teachers.', 'features': ['Everything in Starter', 'Advanced matching', 'Unlimited communities', 'AI tutor and roadmaps', 'Video and live classes'], 'popular': True},
            {'name': 'Mentor', 'price': '$29', 'description': 'For dedicated mentors and professionals.', 'features': ['Everything in Pro', 'Paid session tools', 'Advanced analytics', 'Portfolio builder', 'Priority support']},
        ],
    }
    return render(request, 'Knot_Base/pricing.html', context)

def about(request):
    return render(request, 'Knot_Base/about.html', {'team_count': '12k+', 'topic_count': '340+', 'country_count': '116+'})

def blog(request):
    context = {
        'posts': [
            {'category': 'Learning', 'title': 'Why teaching is one of the fastest ways to learn', 'excerpt': 'The strongest knowledge sticks when you have to make it useful for another person.', 'date': 'Sep 04, 2026', 'read_time': '5 min read', 'icon': 'bi bi-lightbulb'},
            {'category': 'Community', 'title': 'How to find your people in a new learning community', 'excerpt': 'A few small habits can turn a quiet room into a place where your questions belong.', 'date': 'Aug 28, 2026', 'read_time': '4 min read', 'icon': 'bi bi-people'},
            {'category': 'Practice', 'title': 'The small-session method for making steady progress', 'excerpt': 'You do not need a perfect schedule. You need a rhythm you can return to.', 'date': 'Aug 19, 2026', 'read_time': '6 min read', 'icon': 'bi bi-arrow-repeat'},
            {'category': 'Stories', 'title': 'From UX research to Python: Aria and Marcus exchange notes', 'excerpt': 'Two KnotWorkers share what changed when learning became reciprocal.', 'date': 'Aug 11, 2026', 'read_time': '7 min read', 'icon': 'bi bi-chat-heart'},
        ],
    }
    return render(request, 'Knot_Base/blog.html', context)

def help(request):
    context = {
        'faqs': [
            {'question': 'What is KnotWork?', 'answer': 'KnotWork is a mutual learning network where people teach what they know and learn from others.'},
            {'question': 'Is it free to join?', 'answer': 'Yes. You can create a free account, explore communities, and start skill exchanges without a paid plan.'},
            {'question': 'Can I be both a student and a teacher?', 'answer': 'That is the heart of KnotWork. Your profile can include skills you want to learn and skills you are ready to share.'},
            {'question': 'How are matches made?', 'answer': 'Matches consider your skills, learning goals, preferred format, and availability.'},
        ],
    }
    return render(request, 'Knot_Base/help.html', context)




# The Authentication Parts

def get_started(request):
    role = request.POST.get('role', request.GET.get('role', 'student'))
    form = OnboardingForm(
        request.POST or None,
        request.FILES or None,
        initial={'role': role},
    )

    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        with transaction.atomic():
            user = User.objects.create_user(
                username=data['email'],
                email=data['email'],
                password=data['password'],
                first_name=data['first_name'],
                last_name=data['surname'],
            )

            role = data['role']
            profile_data = {
                'first_name': data['first_name'],
                'surname': data['surname'],
                'email': data['email'],
                'bio': data.get('short_bio') or data.get('mentor_bio') or '',
                'timezone': data.get('timezone') or '',
                'hear_about_us': data.get('hear_about_us') or '',
                'terms_accepted': data.get('terms_accepted', False),
                'email_marketing': data.get('email_marketing', False),
            }

            OnboardingProfile.objects.create(
                user=user,
                role=role,
                **profile_data,
            )

            if role == 'student':
                Student.objects.create(
                    user=user,
                    skill_level=data.get('skill_level') or '',
                    primary_subject=data.get('primary_subject') or '',
                )
                StudentPrivate.objects.create(
                    user=user,
                    learning_goal=data.get('learning_goal') or '',
                    phone_number=data.get('phone_number') or '',
                    timezone=data.get('timezone') or '',
                )
            elif role == 'teacher':
                Teacher.objects.create(
                    user=user,
                    years_experience=data.get('years_experience'),
                    current_job_title=data.get('current_job_title') or '',
                    teaching_style=data.get('teaching_style') or '',
                    languages_spoken=data.get('languages_spoken') or '',
                    portfolio_url=data.get('portfolio_url') or '',
                    linkedin_url=data.get('linkedin_url') or '',
                    github_url=data.get('github_url') or '',
                )
                TeacherPrivate.objects.create(
                    user=user,
                    phone_number=data.get('phone_number') or '',
                    payment_method=data.get('payment_method') or '',
                    availability=data.get('availability') or '',
                    id_certificate=data.get('id_certificate'),
                    background_check_consent=data.get('background_check_consent', False),
                    teacher_terms_accepted=data.get('teacher_terms_accepted', False),
                )
            elif role == 'mentor':
                Mentor.objects.create(
                    user=user,
                    mentorship_areas=data.get('mentorship_areas') or '',
                    industry_skills=data.get('industry_skills') or '',
                    current_role_company=data.get('current_role_company') or '',
                    mentor_bio=data.get('mentor_bio') or '',
                    mentor_links=data.get('mentor_links') or '',
                    mentorship_type=data.get('mentorship_type') or '',
                    languages_spoken=data.get('languages_spoken') or '',
                )
                MentorPrivate.objects.create(
                    user=user,
                    phone_number=data.get('phone_number') or '',
                    session_rate=data.get('session_rate') or '',
                    max_students_per_month=data.get('max_students_per_month'),
                    mentor_id=data.get('mentor_id'),
                    references=data.get('references') or '',
                    availability=data.get('availability') or '',
                    mentor_terms_accepted=data.get('mentor_terms_accepted', False),
                )

        messages.success(request, 'Your account is ready. You can log in to your account!')
        return redirect('login')

    return render(request, 'Auth/get_started.html', {'form': form, 'selected_role': role})


def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.cleaned_data['user']
        auth_login(request, user)
        messages.success(request, 'You have logged in successfully!')
        return redirect_user_by_role(user)
    return render(request, 'Auth/login.html', {'form': form})



# STUDENT VIEWS SECTIONS
@login_required(login_url='login')
def student_dashboard(request):
    # 1. Get public + private - but NEVER send private to template
    student_profile = getattr(request.user, 'student_profile', None)
    student_private = getattr(request.user, 'student_private', None)

    # 2. if no student profile yet, redirect to onboarding/get_started
    if not student_profile:
        return redirect('get-started')
    
    return render(request, 'Knot_Student/student_dashboard.html', {
        'student': student_profile,
        'learning_goal': student_private.learning_goal if student_private else "",
    })


@login_required(login_url='login')
def student_find_courses(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')

    courses = Course.objects.filter(is_published=True).select_related('teacher__user')
    q = request.GET.get('q', '').strip()
    
    category = request.GET.getlist('category')
    level = request.GET.getlist('level')
    max_price = request.GET.get('max_price', '').strip()
    teacher_id = request.GET.get('teacher_id', '').strip()
    if q:
        courses = courses.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(category__icontains=q) |
            Q(teacher__user__first_name__icontains=q) |
            Q(teacher__user__last_name__icontains=q)
        )

    if category:
        courses = courses.filter(category__in=category)

    if level:
        courses = courses.filter(level__in=level)

    if teacher_id.isdigit():
        courses = courses.filter(teacher__user_id=int(teacher_id))

    if max_price:
        try:
            courses = courses.filter(price__lte=Decimal(max_price))
        except (InvalidOperation, TypeError, ValueError):
            max_price = ''

    enrolled_course_ids = set(Enrollment.objects.filter(
        student=student,
        course__in=courses,
    ).values_list('course_id', flat=True))
    saved_course_ids = set(SavedCourse.objects.filter(
        student=student,
        course__in=courses,
    ).values_list('course_id', flat=True))

    return render(request, 'Knot_Student/find_courses.html', {
        'courses': courses,
        'enrolled_course_ids': enrolled_course_ids,
        'saved_course_ids': saved_course_ids,
        'course_count': courses.count(),
        'search_query': q,
        'selected_category': category,
        'selected_level': level,
        'max_price': max_price or '240',
        'categories': Course.CATEGORY_CHOICES, # from the models 
        'levels': Course.LEVEL_CHOICES, # from the models
        'category_icons': Course.CATEGORY_ICONS,
        'level_icons': Course.LEVEL_ICONS,
        'category_options': [
            {'value': value, 'label': label, 'icon': Course.CATEGORY_ICONS.get(value, 'bi-book')}
            for value, label in Course.CATEGORY_CHOICES
        ],
        'level_options': [
            {'value': value, 'label': label, 'icon': Course.LEVEL_ICONS.get(value, 'bi-signal')}
            for value, label in Course.LEVEL_CHOICES
        ],
    })


@login_required(login_url='login')
def student_my_learning(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')

    enrollments = Enrollment.objects.filter(
        student=student,
    ).select_related('course', 'course__teacher__user').order_by('-enrolled_at')
    completed_enrollments = enrollments.filter(completed_at__isnull=False) | enrollments.filter(progress_percent=100)
    active_enrollments = enrollments.exclude(pk__in=completed_enrollments.values('pk'))
    saved_courses = Course.objects.filter(
        saved_by__student=student,
        is_published=True,
    ).select_related('teacher__user').distinct()
    certificates = Certificate.objects.filter(student=student).select_related('course').order_by('-issued_at')
    for enrollment in completed_enrollments.select_related('course'):
        Certificate.objects.get_or_create(
            student=student,
            course=enrollment.course,
            defaults={'certificate_id': f'KNT-CERT-{enrollment.course.course_id}'[:24]},
        )
    certificates = Certificate.objects.filter(student=student).select_related('course').order_by('-issued_at')
    upcoming_deadlines = LearningDeadline.objects.filter(
        student=student,
        is_completed=False,
        due_at__gte=timezone.now(),
    ).select_related('course')[:5]
    week_start = timezone.localdate() - timedelta(days=timezone.localdate().weekday())
    weekly_goal, _ = WeeklyGoal.objects.get_or_create(student=student, week_start=week_start)
    total_learning_minutes = LearningSession.objects.filter(
        student=student,
        status='completed',
    ).aggregate(total=Sum('duration_minutes')).get('total') or 0
    completed_count = completed_enrollments.count()
    active_count = active_enrollments.count()
    progress_total = sum(item.progress_percent for item in active_enrollments)
    progress_percent = round(progress_total / active_count) if active_count else 0

    return render(request, 'Knot_Student/my_learning.html', {
        'enrollments': active_enrollments,
        'completed_enrollments': completed_enrollments,
        'saved_courses': saved_courses,
        'active_count': active_count,
        'completed_count': completed_count,
        'saved_count': saved_courses.count(),
        'progress_percent': progress_percent,
        'total_learning_hours': round(total_learning_minutes / 60, 1),
        'certificates': certificates,
        'certificate_count': certificates.count(),
        'upcoming_deadlines': upcoming_deadlines,
        'weekly_goal': weekly_goal,
    })


@login_required(login_url='login')
def student_toggle_saved_course(request, course_id):
    if request.method != 'POST':
        return redirect('student_find_courses')
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')
    course = Course.objects.filter(course_id=course_id, is_published=True).first()
    if not course:
        messages.error(request, 'That course is no longer available.')
        return redirect('student_find_courses')
    saved, created = SavedCourse.objects.get_or_create(student=student, course=course)
    if not created:
        saved.delete()
    return redirect(request.POST.get('next') or 'student_find_courses')


@login_required(login_url='login')
def student_enrol_course(request, course_id):
    if request.method != 'POST':
        return redirect('student_find_courses')

    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')

    course = Course.objects.filter(course_id=course_id, is_published=True).first()
    if not course:
        messages.error(request, 'That course is no longer available.')
        return redirect('student_find_courses')

    _, created = Enrollment.objects.get_or_create(student=student, course=course)
    if created:
        messages.success(request, f'You are now enrolled in {course.title}.')
    else:
        messages.info(request, f'You are already enrolled in {course.title}.')
    return redirect('student_my_learning')

def student_skill_matches(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')

    private = getattr(request.user, 'student_private', None)
    wanted_text = ' '.join(filter(None, (student.primary_subject, private.learning_goal if private else ''))).casefold()
    wanted_terms = {term for term in wanted_text.replace('/', ' ').replace(',', ' ').split() if len(term) > 2}
    excluded_ids = set(PeopleRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user),
    ).filter(request_type='connection', status__in=('pending', 'accepted', 'passed')).values_list('from_user_id', 'to_user_id'))
    excluded_ids = {user_id for pair in excluded_ids for user_id in pair if user_id != request.user.id}

    candidates = []
    teachers = Teacher.objects.select_related('user', 'user__onboarding_profile').prefetch_related('courses').exclude(user=request.user)
    for teacher in teachers:
        course_skills = list(teacher.courses.filter(is_published=True).values_list('category', flat=True))
        offerings = list(teacher.courses.filter(is_published=True).values_list('title', flat=True)) + course_skills
        if teacher.current_job_title:
            offerings.append(teacher.current_job_title)
        matched = [term for term in wanted_terms if any(term in offering.casefold() for offering in offerings)]
        if matched and teacher.user_id not in excluded_ids:
            candidates.append({
                'user': teacher.user,
                'name': teacher.user.get_full_name().strip() or teacher.user.username,
                'initials': teacher.initials,
                'role': teacher.current_job_title or 'Teacher',
                'bio': getattr(getattr(teacher.user, 'onboarding_profile', None), 'bio', '') or 'This teacher has not added a bio yet.',
                'offerings': list(dict.fromkeys(offerings)),
                'matched_skills': matched,
                'match_score': round(len(matched) * 100 / max(len(wanted_terms), 1)),
                'action': 'connection',
            })
    mentors = Mentor.objects.select_related('user').exclude(user=request.user)
    for mentor in mentors:
        offerings = [term.strip() for value in (mentor.mentorship_areas, mentor.industry_skills) for term in value.split(',') if term.strip()]
        matched = [term for term in wanted_terms if any(term in offering.casefold() for offering in offerings)]
        if matched and mentor.user_id not in excluded_ids:
            candidates.append({
                'user': mentor.user,
                'name': mentor.user.get_full_name().strip() or mentor.user.username,
                'initials': mentor.initials,
                'role': mentor.current_role_company or 'Mentor',
                'bio': mentor.mentor_bio or 'This mentor has not added a bio yet.',
                'offerings': offerings,
                'matched_skills': matched,
                'match_score': round(len(matched) * 100 / max(len(wanted_terms), 1)),
                'action': 'mentorship',
            })

    candidates.sort(key=lambda item: (-len(item['matched_skills']), item['name'].casefold()))
    connected_ids = PeopleRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user), request_type='connection', status='accepted',
    ).count()
    recent_connections = PeopleRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user), request_type='connection', status='accepted',
    ).select_related('from_user', 'to_user').order_by('-responded_at', '-created_at')[:4]
    recent_rows = []
    for item in recent_connections:
        person = item.to_user if item.from_user_id == request.user.id else item.from_user
        recent_rows.append({'person': person, 'initials': _user_initials(person)})
    return render(request, 'Knot_Student/skill_matches.html', {
        'matches': candidates,
        'match_count': len(candidates),
        'connected_count': connected_ids,
        'wanted_skills': sorted(wanted_terms),
        'recent_connections': recent_rows,
    })

def student_browse(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')

    role = request.GET.get('role', 'student')
    if role not in {'student', 'teacher', 'mentor'}:
        role = 'student'
    query = request.GET.get('q', '').strip()
    selected_skill = request.GET.get('skill', '').strip()

    if role == 'student':
        profiles = Student.objects.select_related('user', 'user__onboarding_profile').exclude(user=request.user)
        if query:
            profiles = profiles.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(primary_subject__icontains=query) |
                Q(user__onboarding_profile__bio__icontains=query)
            )
        raw_profiles = list(profiles.order_by('user__first_name', 'user__last_name'))
        people = []
        for profile in raw_profiles:
            skills = [profile.primary_subject] if profile.primary_subject else []
            onboarding = getattr(profile.user, 'onboarding_profile', None)
            people.append({
                'user': profile.user,
                'name': profile.user.get_full_name().strip() or profile.user.username,
                'initials': profile.initials,
                'role_label': f'{profile.primary_subject or "Student"} learner',
                'role_name': 'Student',
                'role_icon': 'bi-mortarboard',
                'role_class': '',
                'bio': (onboarding.bio if onboarding else '') or 'This learner has not added a bio yet.',
                'skills': skills,
                'meta_label': 'Learning level',
                'meta_value': profile.skill_level or 'Not specified',
                'action': 'connection',
            })
    elif role == 'teacher':
        profiles = Teacher.objects.select_related('user', 'user__onboarding_profile').annotate(
            published_course_count=Count('courses', filter=Q(courses__is_published=True), distinct=True),
            learner_count=Count('courses__enrollments__student', filter=Q(courses__is_published=True), distinct=True),
        )
        if query:
            profiles = profiles.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(current_job_title__icontains=query) |
                Q(courses__title__icontains=query) |
                Q(courses__category__icontains=query) |
                Q(user__onboarding_profile__bio__icontains=query)
            ).distinct()
        raw_profiles = list(profiles.order_by('user__first_name', 'user__last_name'))
        people = []
        for profile in raw_profiles:
            skills = list(Course.objects.filter(teacher=profile, is_published=True).values_list('category', flat=True).distinct())
            onboarding = getattr(profile.user, 'onboarding_profile', None)
            people.append({
                'user': profile.user,
                'name': profile.user.get_full_name().strip() or profile.user.username,
                'initials': profile.initials,
                'role_label': profile.current_job_title or 'Teacher',
                'role_name': 'Teacher',
                'role_icon': 'bi-person-video3',
                'role_class': 'sky',
                'bio': (onboarding.bio if onboarding else '') or 'This teacher has not added a bio yet.',
                'skills': skills,
                'meta_label': 'Published courses',
                'meta_value': profile.published_course_count,
                'secondary_label': 'Learners',
                'secondary_value': profile.learner_count,
                'action': 'courses',
            })
    else:
        profiles = Mentor.objects.select_related('user', 'user__onboarding_profile')
        if query:
            profiles = profiles.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(mentorship_areas__icontains=query) |
                Q(industry_skills__icontains=query) |
                Q(current_role_company__icontains=query) |
                Q(mentor_bio__icontains=query)
            )
        raw_profiles = list(profiles.order_by('user__first_name', 'user__last_name'))
        people = []
        for profile in raw_profiles:
            skills = [skill.strip() for skill in f'{profile.mentorship_areas},{profile.industry_skills}'.split(',') if skill.strip()]
            people.append({
                'user': profile.user,
                'name': profile.user.get_full_name().strip() or profile.user.username,
                'initials': profile.initials,
                'role_label': profile.current_role_company or 'Mentor',
                'role_name': 'Mentor',
                'role_icon': 'bi-person-badge',
                'role_class': 'violet',
                'bio': profile.mentor_bio or 'This mentor has not added a bio yet.',
                'skills': skills,
                'meta_label': 'Mentorship areas',
                'meta_value': ', '.join(skills[:2]) or 'Not specified',
                'action': 'mentorship',
            })

    if selected_skill:
        people = [person for person in people if any(selected_skill.casefold() in skill.casefold() for skill in person['skills'])]

    skills = set()
    for subject in Student.objects.exclude(primary_subject__isnull=True).exclude(primary_subject='').values_list('primary_subject', flat=True):
        skills.add(subject.strip())
    skills.update(Course.objects.filter(is_published=True).values_list('category', flat=True).distinct())
    for mentorship_areas, industry_skills in Mentor.objects.values_list('mentorship_areas', 'industry_skills'):
        skills.update(skill.strip() for value in (mentorship_areas, industry_skills) for skill in value.split(',') if skill.strip())

    role_counts = {
        'student': max(Student.objects.count() - int(Student.objects.filter(pk=student.pk).exists()), 0),
        'teacher': Teacher.objects.count(),
        'mentor': Mentor.objects.count(),
    }
    candidate_ids = [person['user'].id for person in people]
    person_request_types = {
        person['user'].id: ('mentorship' if person['action'] == 'mentorship' else 'connection')
        for person in people
    }
    sent_by_user = {}
    received_by_user = {}
    related_requests = PeopleRequest.objects.filter(
        Q(from_user=request.user, to_user_id__in=candidate_ids) |
        Q(to_user=request.user, from_user_id__in=candidate_ids),
    )
    for item in related_requests:
        other_user_id = item.to_user_id if item.from_user_id == request.user.id else item.from_user_id
        if item.request_type != person_request_types.get(other_user_id):
            continue
        if item.from_user_id == request.user.id:
            sent_by_user[other_user_id] = item.status
        else:
            received_by_user[other_user_id] = item.status
    for person in people:
        target_id = person['user'].id
        if received_by_user.get(target_id) == 'pending':
            person['request_status'] = 'incoming'
        elif sent_by_user.get(target_id) == 'pending':
            person['request_status'] = 'sent'
        elif 'accepted' in (sent_by_user.get(target_id), received_by_user.get(target_id)):
            person['request_status'] = 'connected' if person['action'] == 'connection' else 'accepted'
        else:
            person['request_status'] = ''

    paginator = Paginator(people, 9)
    try:
        page_obj = paginator.page(request.GET.get('page', 1))
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1 if request.GET.get('page', '1').isdigit() is False else paginator.num_pages or 1)

    return render(request, 'Knot_Student/browse.html', {
        'people': page_obj.object_list,
        'page_obj': page_obj,
        'page_range': paginator.get_elided_page_range(page_obj.number),
        'role': role,
        'role_counts': role_counts,
        'result_count': paginator.count,
        'search_query': query,
        'selected_skill': selected_skill,
        'skill_options': sorted(skills, key=str.casefold),
    })


@login_required(login_url='login')
def student_browse_action(request, user_id):
    if request.method != 'POST':
        return redirect('student_browse')
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')

    target = User.objects.filter(pk=user_id, is_active=True).exclude(pk=request.user.pk).first()
    if not target:
        messages.error(request, 'That member is no longer available.')
        return redirect('student_browse')

    action = request.POST.get('action')
    if action == 'pass' and (Student.objects.filter(user=target).exists() or Teacher.objects.filter(user=target).exists() or Mentor.objects.filter(user=target).exists()):
        request_type = 'connection'
    elif action == 'accept' and Mentor.objects.filter(user=target).exists():
        request_type = 'mentorship'
    elif action in {'connection', 'accept'} and (Student.objects.filter(user=target).exists() or Teacher.objects.filter(user=target).exists()):
        request_type = 'connection'
    elif action == 'mentorship' and Mentor.objects.filter(user=target).exists():
        request_type = 'mentorship'
    else:
        messages.error(request, 'That action is not available for this member.')
        return redirect('student_browse')

    if action == 'accept':
        incoming = PeopleRequest.objects.filter(from_user=target, to_user=request.user, request_type=request_type, status='pending').first()
        if incoming:
            incoming.status = 'accepted'
            incoming.responded_at = timezone.now()
            incoming.save(update_fields=('status', 'responded_at'))
            PeopleRequest.objects.filter(
                from_user=request.user,
                to_user=target,
                request_type=request_type,
                status='pending',
            ).update(status='withdrawn', responded_at=timezone.now())
            if request_type == 'connection':
                messages.success(request, f'You are now connected with {target.get_full_name() or target.username}.')
            else:
                messages.success(request, f'You accepted the mentorship request from {target.get_full_name() or target.username}.')
        else:
            messages.info(request, 'There is no pending request from this member.')
    elif action == 'pass':
        PeopleRequest.objects.update_or_create(
            from_user=request.user,
            to_user=target,
            request_type='connection',
            defaults={'status': 'passed', 'responded_at': timezone.now()},
        )
        messages.info(request, 'Profile passed.')
    else:
        existing = PeopleRequest.objects.filter(from_user=request.user, to_user=target, request_type=request_type).first()
        if existing and existing.status in {'pending', 'accepted'}:
            messages.info(request, 'You already have an active request or connection with this member.')
        else:
            PeopleRequest.objects.update_or_create(
                from_user=request.user,
                to_user=target,
                request_type=request_type,
                defaults={'status': 'pending', 'responded_at': None},
            )
            messages.success(request, 'Your request has been sent.')
    next_url = request.POST.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('student_browse')

def student_my_connections(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')
    connections = PeopleRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user), request_type='connection', status='accepted',
    ).select_related('from_user', 'to_user').order_by('-responded_at', '-created_at')
    outgoing = PeopleRequest.objects.filter(from_user=request.user, request_type='connection', status='pending').select_related('to_user')
    incoming = PeopleRequest.objects.filter(to_user=request.user, request_type='connection', status='pending').select_related('from_user')
    connection_rows = []
    for item in connections:
        person = item.to_user if item.from_user_id == request.user.id else item.from_user
        connection_rows.append({'request': item, 'person': person, 'initials': _user_initials(person)})
    sent_rows = [{'request': item, 'person': item.to_user, 'initials': _user_initials(item.to_user)} for item in outgoing]
    incoming_rows = [{'request': item, 'person': item.from_user, 'initials': _user_initials(item.from_user)} for item in incoming]
    return render(request, 'Knot_Student/my_connections.html', {
        'connections': connection_rows,
        'sent_requests': sent_rows,
        'incoming_requests': incoming_rows,
        'connection_count': len(connection_rows),
        'sent_count': len(sent_rows),
        'incoming_count': len(incoming_rows),
    })

def student_requests(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')
    tab = request.GET.get('tab', 'incoming')
    if tab not in {'incoming', 'sent', 'history'}:
        tab = 'incoming'
    base = PeopleRequest.objects.filter(request_type__in=('connection', 'mentorship')).select_related('from_user', 'to_user')
    incoming = base.filter(to_user=request.user, status='pending').order_by('-created_at')
    sent = base.filter(from_user=request.user, status='pending').order_by('-created_at')
    history = base.filter(Q(from_user=request.user) | Q(to_user=request.user)).exclude(status='pending').order_by('-responded_at', '-created_at')
    selected = {'incoming': incoming, 'sent': sent, 'history': history}[tab]
    rows = []
    for item in selected:
        person = item.from_user if item.to_user_id == request.user.id else item.to_user
        rows.append({'request': item, 'person': person, 'initials': _user_initials(person), 'direction': 'incoming' if item.to_user_id == request.user.id else 'sent'})
    return render(request, 'Knot_Student/requests.html', {
        'request_rows': rows,
        'active_tab': tab,
        'incoming_count': incoming.count(),
        'sent_count': sent.count(),
        'history_count': history.count(),
        'accepted_count': base.filter(Q(from_user=request.user) | Q(to_user=request.user), status='accepted').count(),
        'connection_count': incoming.filter(request_type='connection').count(),
        'mentorship_count': incoming.filter(request_type='mentorship').count(),
    })


def _user_initials(user):
    name = user.get_full_name().strip()
    if name:
        return ''.join(part[0] for part in name.split()[:2]).upper()
    return user.username[:2].upper()


@login_required(login_url='login')
def student_people_request_action(request, request_id):
    if request.method != 'POST':
        return redirect('student_requests')
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')
    action = request.POST.get('action')
    people_request = PeopleRequest.objects.filter(pk=request_id).first()
    if not people_request:
        messages.error(request, 'That request is no longer available.')
        return redirect('student_requests')
    if action in {'accept', 'decline'} and people_request.to_user_id == request.user.id and people_request.status == 'pending':
        people_request.status = 'accepted' if action == 'accept' else 'declined'
        if action == 'accept':
            PeopleRequest.objects.filter(
                from_user=request.user,
                to_user=people_request.from_user,
                request_type=people_request.request_type,
                status='pending',
            ).update(status='withdrawn', responded_at=timezone.now())
    elif action == 'withdraw' and people_request.from_user_id == request.user.id and people_request.status == 'pending':
        people_request.status = 'withdrawn'
    elif action == 'remove' and request.user.id in (people_request.from_user_id, people_request.to_user_id) and people_request.status == 'accepted':
        people_request.status = 'withdrawn'
    else:
        messages.error(request, 'That action is not available for this request.')
        return redirect('student_requests')
    people_request.responded_at = timezone.now()
    people_request.save(update_fields=('status', 'responded_at'))
    messages.success(request, 'Request updated.')
    next_url = request.POST.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('student_requests')

def student_messages(request):
    return render(request, 'Knot_Student/messages.html')

def student_sessions(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')
    sessions = LearningSession.objects.filter(student=student).select_related('teacher__user', 'course')
    return render(request, 'Knot_Student/sessions.html', {
        'upcoming_sessions': sessions.filter(status='live') | sessions.filter(status='scheduled', starts_at__gte=timezone.now()),
        'past_sessions': sessions.filter(status='completed'),
        'cancelled_sessions': sessions.filter(status='cancelled'),
    })


@login_required(login_url='login')
def student_session_action(request, session_id):
    if request.method != 'POST':
        return redirect('student_sessions')
    student = getattr(request.user, 'student_profile', None)
    session = LearningSession.objects.filter(id=session_id, student=student).first()
    if not session:
        messages.error(request, 'That session is not available to you.')
        return redirect('student_sessions')
    action = request.POST.get('action')
    if action == 'cancel' and session.status == 'scheduled':
        session.status = 'cancelled'
        session.save(update_fields=('status',))
        messages.success(request, 'Session cancelled successfully.')
    elif action == 'raise_hand' and session.status == 'scheduled':
        hand, created = SessionHand.objects.get_or_create(session=session, student=student)
        if not created and hand.resolved_at is not None:
            hand.resolved_at = None
            hand.save(update_fields=('resolved_at',))
        messages.success(request, 'Your hand is raised for this session.')
    elif action == 'lower_hand':
        SessionHand.objects.filter(session=session, student=student, resolved_at__isnull=True).update(resolved_at=timezone.now())
        messages.info(request, 'Your hand has been lowered.')
    elif action == 'rebook' and session.status in ('completed', 'cancelled'):
        LearningSession.objects.create(
            student=student,
            teacher=session.teacher,
            course=session.course,
            title=session.title,
            starts_at=timezone.now() + timedelta(days=7),
            duration_minutes=session.duration_minutes,
            is_group=session.is_group,
        )
        messages.success(request, 'A follow-up session was scheduled for next week.')
    elif action == 'join' and session.status in ('scheduled', 'live'):
        SessionParticipant.objects.update_or_create(
            session=session,
            user=request.user,
            defaults={'role': 'student', 'attendance': 'present', 'joined_at': timezone.now()},
        )
        SessionAttendance.objects.update_or_create(
            session=session,
            student=student,
            defaults={'status': 'present', 'join_time': timezone.now()},
        )
        messages.success(request, 'You joined the session room.')
        if session.meeting_url:
            return redirect(session.meeting_url)
        if session.room_id:
            return redirect('live_classroom', room_id=session.room_id)
    elif action == 'leave':
        SessionAttendance.objects.filter(session=session, student=student).update(leave_time=timezone.now())
        SessionParticipant.objects.filter(session=session, user=request.user).update(left_at=timezone.now())
        messages.info(request, 'You left the session room.')
    elif action == 'save_note':
        SessionNote.objects.update_or_create(
            session=session,
            user=request.user,
            defaults={'content': request.POST.get('content', '')},
        )
    return redirect('student_sessions')

@login_required(login_url='login')
def student_community(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')

    category = request.GET.get('category', 'all')
    valid_categories = {value for value, _label in CommunityPost.CATEGORY_CHOICES}
    if category != 'all' and category not in valid_categories:
        category = 'all'
    query = request.GET.get('q', '').strip()
    sort = request.GET.get('sort', 'newest')
    posts = CommunityPost.objects.select_related('author', 'author__onboarding_profile').annotate(
        reaction_count=Count('reactions', distinct=True),
        reply_count=Count('replies', distinct=True),
    ).prefetch_related(Prefetch(
        'poll_options',
        queryset=CommunityPollOption.objects.annotate(vote_count=Count('votes')).order_by('id'),
    ))
    if category != 'all':
        posts = posts.filter(category=category)
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query) | Q(tags__icontains=query) | Q(author__first_name__icontains=query) | Q(author__last_name__icontains=query))
    if sort == 'popular':
        posts = posts.order_by('-reaction_count', '-created_at')
    elif sort == 'unanswered':
        posts = posts.filter(reply_count=0).order_by('-created_at')
    else:
        sort = 'newest'
        posts = posts.order_by('-created_at')
    saved_only = request.GET.get('saved') == '1'
    if saved_only:
        posts = posts.filter(bookmarks__user=request.user)

    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))
    post_ids = list(page_obj.object_list.values_list('id', flat=True))
    liked_ids = set(CommunityReaction.objects.filter(user=request.user, post_id__in=post_ids).values_list('post_id', flat=True))
    bookmarked_ids = set(CommunityBookmark.objects.filter(user=request.user, post_id__in=post_ids).values_list('post_id', flat=True))
    poll_votes = dict(CommunityPollVote.objects.filter(user=request.user, post_id__in=post_ids).values_list('post_id', 'option_id'))
    for post in page_obj.object_list:
        post.viewer_liked = post.id in liked_ids
        post.viewer_bookmarked = post.id in bookmarked_ids
        post.recent_replies = post.replies.select_related('author').order_by('-created_at')[:3]
        post.tag_list = [tag.strip() for tag in post.tags.split(',') if tag.strip()]
        post.poll_option_rows = list(post.poll_options.all())
        post.poll_vote_count = sum(option.vote_count for option in post.poll_option_rows)
        post.viewer_poll_option_id = poll_votes.get(post.id)
        for option in post.poll_option_rows:
            option.vote_percent = round(option.vote_count * 100 / post.poll_vote_count) if post.poll_vote_count else 0

    trending_topics = list(
        CommunityPost.objects.values('category').annotate(post_count=Count('id')).order_by('-post_count')[:5]
    )
    contributors = User.objects.annotate(
        post_count=Count('community_posts', distinct=True),
        reply_count=Count('community_replies', distinct=True),
    ).annotate(
        activity_count=Count('community_posts', distinct=True) + Count('community_replies', distinct=True),
    ).filter(Q(post_count__gt=0) | Q(reply_count__gt=0)).order_by('-activity_count')[:5]
    return render(request, 'Knot_Student/community.html', {
        'page_obj': page_obj,
        'posts': page_obj.object_list,
        'category': category,
        'category_options': CommunityPost.CATEGORY_CHOICES,
        'search_query': query,
        'sort': sort,
        'saved_only': saved_only,
        'member_count': OnboardingProfile.objects.count(),
        'post_count': CommunityPost.objects.count(),
        'reply_count': CommunityReply.objects.count(),
        'trending_topics': trending_topics,
        'contributors': contributors,
    })


@login_required(login_url='login')
def student_community_action(request, post_id=None):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')
    if request.method != 'POST':
        return redirect('student_community')

    action = request.POST.get('action')
    if action == 'create':
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()
        category = request.POST.get('category', 'discussion')
        valid_categories = {value for value, _label in CommunityPost.CATEGORY_CHOICES}
        image = request.FILES.get('image')
        raw_tags = request.POST.get('tags', '').strip()
        tags = list(dict.fromkeys(tag.strip().lstrip('#') for tag in raw_tags.split(',') if tag.strip()))
        poll_options = [option.strip() for option in request.POST.getlist('poll_option') if option.strip()]
        if not title and body:
            title = body.splitlines()[0].strip()[:180]
        image_valid = True
        if image:
            extension = image.name.rsplit('.', 1)[-1].lower() if '.' in image.name else ''
            header = image.read(12)
            image.seek(0)
            image_valid = image.size <= 5 * 1024 * 1024 and (
                (extension == 'png' and header.startswith(b'\x89PNG\r\n\x1a\n'))
                or (extension in ('jpg', 'jpeg') and header.startswith(b'\xff\xd8\xff'))
                or (extension == 'gif' and header[:6] in (b'GIF87a', b'GIF89a'))
                or (extension == 'webp' and header[:4] == b'RIFF' and header[8:12] == b'WEBP')
            )
        poll_valid = not poll_options or (
            2 <= len(poll_options) <= 5
            and all(len(option) <= 100 for option in poll_options)
            and len({option.casefold() for option in poll_options}) == len(poll_options)
        )
        if (not title or not body or len(title) > 180 or len(body) > 10000
                or category not in valid_categories or len(raw_tags) > 300
                or len(tags) > 8 or any(len(tag) > 32 for tag in tags)
                or not image_valid or not poll_valid):
            messages.error(request, 'Check the post text, image (PNG, JPEG, GIF or WebP up to 5 MB), tags, and poll choices.')
        else:
            with transaction.atomic():
                post = CommunityPost.objects.create(
                    author=request.user,
                    title=title,
                    body=body,
                    category=category,
                    image=image,
                    tags=', '.join(tags),
                )
                CommunityPollOption.objects.bulk_create(
                    CommunityPollOption(post=post, text=option) for option in poll_options
                )
            messages.success(request, 'Your post is now in the community feed.')
        return redirect('student_community')

    post = CommunityPost.objects.filter(pk=post_id).first()
    if not post:
        messages.error(request, 'That discussion is no longer available.')
        return redirect('student_community')
    if action == 'poll_vote':
        option = CommunityPollOption.objects.filter(post=post, pk=request.POST.get('option_id')).first()
        if option:
            CommunityPollVote.objects.update_or_create(
                post=post,
                user=request.user,
                defaults={'option': option},
            )
            messages.success(request, 'Your vote was recorded.')
        else:
            messages.error(request, 'Choose a valid option for this poll.')
    elif action == 'reply':
        body = request.POST.get('body', '').strip()
        if body and len(body) <= 3000:
            CommunityReply.objects.create(post=post, author=request.user, body=body)
            messages.success(request, 'Your reply was added.')
        else:
            messages.error(request, 'Write a reply of up to 3000 characters.')
    elif action == 'upvote':
        reaction, created = CommunityReaction.objects.get_or_create(post=post, user=request.user)
        if not created:
            reaction.delete()
    elif action == 'bookmark':
        bookmark, created = CommunityBookmark.objects.get_or_create(post=post, user=request.user)
        if not created:
            bookmark.delete()
    elif action == 'delete' and post.author_id == request.user.id:
        post.delete()
        messages.success(request, 'Your post was deleted.')
    else:
        messages.error(request, 'That action is not available.')
    next_url = request.POST.get('next', '')
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect('student_community')

def student_progress(request):
    return render(request, 'Knot_Student/progress.html')

@login_required(login_url='login')
def student_achievements(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')

    enrollments = Enrollment.objects.filter(student=student)
    completed_enrollments = enrollments.filter(Q(completed_at__isnull=False) | Q(progress_percent__gte=100)).count()
    sessions = LearningSession.objects.filter(student=student, status='completed')
    completed_sessions = sessions.count()
    completed_minutes = sessions.aggregate(total=Sum('duration_minutes'))['total'] or 0
    sent_connections = PeopleRequest.objects.filter(from_user=request.user, request_type='connection', status='pending').count()
    outgoing_connection_count = PeopleRequest.objects.filter(
        from_user=request.user,
        request_type='connection',
        status__in=('pending', 'accepted'),
    ).count()
    accepted_connections = PeopleRequest.objects.filter(
        Q(from_user=request.user) | Q(to_user=request.user), request_type='connection', status='accepted',
    ).count()
    posts_count = CommunityPost.objects.filter(author=request.user).count()
    replies_count = CommunityReply.objects.filter(author=request.user).count()
    week_start = timezone.localdate() - timedelta(days=timezone.localdate().weekday())
    weekly_goal = WeeklyGoal.objects.filter(student=student, week_start=week_start).first()
    goal_met = bool(weekly_goal and weekly_goal.completed_sessions >= weekly_goal.target_sessions)

    definitions = [
        {'key': 'course-one', 'title': 'First Course', 'description': 'Enroll in your first course.', 'category': 'learning', 'tier': 'bronze', 'icon': 'bi-mortarboard-fill', 'current': enrollments.count(), 'target': 1},
        {'key': 'course-finish', 'title': 'Course Finisher', 'description': 'Complete three enrolled courses.', 'category': 'learning', 'tier': 'silver', 'icon': 'bi-check2-circle', 'current': completed_enrollments, 'target': 3},
        {'key': 'session-one', 'title': 'First Session', 'description': 'Complete your first learning session.', 'category': 'learning', 'tier': 'bronze', 'icon': 'bi-camera-video-fill', 'current': completed_sessions, 'target': 1},
        {'key': 'session-ten', 'title': 'Session Regular', 'description': 'Complete ten learning sessions.', 'category': 'learning', 'tier': 'silver', 'icon': 'bi-calendar-check-fill', 'current': completed_sessions, 'target': 10},
        {'key': 'learning-hours', 'title': 'Deep Learner', 'description': 'Complete 20 hours of learning sessions.', 'category': 'learning', 'tier': 'gold', 'icon': 'bi-clock-history', 'current': completed_minutes // 60, 'target': 20},
        {'key': 'connection-one', 'title': 'First Connection', 'description': 'Accept or complete your first connection.', 'category': 'social', 'tier': 'bronze', 'icon': 'bi-people-fill', 'current': accepted_connections, 'target': 1},
        {'key': 'connection-five', 'title': 'Growing Network', 'description': 'Build five accepted connections.', 'category': 'social', 'tier': 'silver', 'icon': 'bi-diagram-3-fill', 'current': accepted_connections, 'target': 5},
        {'key': 'community-one', 'title': 'Community Voice', 'description': 'Publish your first community post.', 'category': 'social', 'tier': 'bronze', 'icon': 'bi-chat-left-text-fill', 'current': posts_count, 'target': 1},
        {'key': 'community-ten', 'title': 'Helpful Contributor', 'description': 'Write ten community posts or replies.', 'category': 'social', 'tier': 'gold', 'icon': 'bi-chat-square-heart-fill', 'current': posts_count + replies_count, 'target': 10},
        {'key': 'weekly-goal', 'title': 'Weekly Momentum', 'description': 'Meet your weekly learning session goal.', 'category': 'learning', 'tier': 'bronze', 'icon': 'bi-lightning-charge-fill', 'current': weekly_goal.completed_sessions if weekly_goal else 0, 'target': weekly_goal.target_sessions if weekly_goal else 1},
        {'key': 'connection-sender', 'title': 'Connector', 'description': 'Send your first connection request.', 'category': 'social', 'tier': 'bronze', 'icon': 'bi-person-plus-fill', 'current': outgoing_connection_count, 'target': 1},
    ]
    badges = []
    for item in definitions:
        item['unlocked'] = item['current'] >= item['target']
        item['progress'] = min(100, round(item['current'] * 100 / max(item['target'], 1)))
        item['progress_label'] = f"{min(item['current'], item['target'])} / {item['target']}"
        item['category_label'] = item['category']
        item['tier_label'] = item['tier'].title()
        badges.append(item)
    filter_name = request.GET.get('filter', 'all')
    if filter_name == 'unlocked':
        filtered_badges = [item for item in badges if item['unlocked']]
    elif filter_name == 'locked':
        filtered_badges = [item for item in badges if not item['unlocked']]
    elif filter_name in {'learning', 'social'}:
        filtered_badges = [item for item in badges if item['category'] == filter_name]
    elif filter_name == 'legendary':
        filtered_badges = [item for item in badges if item['tier'] == 'legendary']
    else:
        filter_name = 'all'
        filtered_badges = badges
    sort_name = request.GET.get('sort', 'progress')
    if sort_name == 'name':
        filtered_badges.sort(key=lambda item: item['title'].casefold())
    elif sort_name == 'unlocked':
        filtered_badges.sort(key=lambda item: (not item['unlocked'], item['title'].casefold()))
    else:
        sort_name = 'progress'
        filtered_badges.sort(key=lambda item: (item['unlocked'], -item['progress'], item['title'].casefold()))
    unlocked_badges = [item for item in badges if item['unlocked']]
    return render(request, 'Knot_Student/achievements.html', {
        'badges': filtered_badges,
        'badge_count': len(badges),
        'unlocked_count': len(unlocked_badges),
        'locked_count': len(badges) - len(unlocked_badges),
        'completion_percent': round(len(unlocked_badges) * 100 / len(badges)) if badges else 0,
        'learning_count': sum(item['category'] == 'learning' for item in badges),
        'social_count': sum(item['category'] == 'social' for item in badges),
        'legendary_count': sum(item['tier'] == 'legendary' for item in badges),
        'bronze_count': sum(item['tier'] == 'bronze' for item in badges),
        'silver_count': sum(item['tier'] == 'silver' for item in badges),
        'gold_count': sum(item['tier'] == 'gold' for item in badges),
        'filtered_count': len(filtered_badges),
        'sort_name': sort_name,
        'filter_name': filter_name,
        'recent_badges': unlocked_badges,
        'completed_sessions': completed_sessions,
        'completed_courses': completed_enrollments,
        'accepted_connections': accepted_connections,
    })

def student_credits_and_billing(request):
    return render(request, 'Knot_Student/credits_and_billing.html')

def student_settings(request):
    return render(request, 'Knot_Student/settings.html')

@login_required(login_url='login')
def student_help(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')
    tickets = SupportTicket.objects.filter(user=request.user)[:5]
    return render(request, 'Knot_Student/help_centre.html', {
        'tickets': tickets,
        'open_ticket_count': SupportTicket.objects.filter(user=request.user, status__in=('open', 'in_progress')).count(),
        'search_query': request.GET.get('q', '').strip(),
        'member_count': OnboardingProfile.objects.count(),
        'faq_count': 23,
    })


@login_required(login_url='login')
def student_help_action(request):
    student = getattr(request.user, 'student_profile', None)
    if not student:
        return redirect('get_started')
    if request.method != 'POST':
        return redirect('student_help')
    action = request.POST.get('action')
    if action == 'ticket':
        subject = request.POST.get('subject', '').strip()
        body = request.POST.get('message', '').strip()
        category = request.POST.get('category', 'general')
        valid_categories = {'general', 'sessions', 'credits', 'account', 'safety', 'community'}
        if subject and body and len(subject) <= 180 and len(body) <= 5000 and category in valid_categories:
            SupportTicket.objects.create(user=request.user, subject=subject, message=body, category=category)
            messages.success(request, 'Your support request has been submitted.')
        else:
            messages.error(request, 'Add a subject and message, and choose a valid help category.')
    elif action == 'feedback':
        was_helpful = request.POST.get('helpful') == 'yes'
        HelpfulnessFeedback.objects.update_or_create(
            user=request.user,
            topic='help-centre',
            defaults={'was_helpful': was_helpful},
        )
        messages.success(request, 'Thanks, your feedback has been recorded.')
    elif action == 'close_ticket':
        ticket = SupportTicket.objects.filter(pk=request.POST.get('ticket_id'), user=request.user).first()
        if ticket and ticket.status in {'open', 'in_progress'}:
            ticket.status = 'closed'
            ticket.save(update_fields=('status', 'updated_at'))
            messages.success(request, 'Your ticket has been closed.')
        else:
            messages.error(request, 'That support ticket cannot be closed.')
    else:
        messages.error(request, 'That help-centre action is not available.')
    return redirect('student_help')

def student_profile(request):
    return render(request, 'Knot_Student/profile.html')


def student_logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('/login')


# TEACHER VIEWS SECTIONS
@login_required(login_url='login')
def teacher_dashboard(request):
    return render(request, 'Knot_Teacher/teacher_dashboard.html')

@login_required(login_url='login')
def teacher_atelier(request, course_id=None):
    teacher = getattr(request.user, 'teacher_profile', None)
    if not teacher:
        messages.error(request, 'Only teachers accounts can access the Atelier.')
        return redirect_user_by_role(request.user)

    editing_course = None
    edit_id = course_id or request.GET.get('edit')
    if course_id and request.method != 'POST':
        return redirect(f'{reverse("teacher_atelier")}?tab=drafts')
    if edit_id:
        editing_course = Course.objects.filter(
            teacher=teacher,
            course_id=edit_id,
            is_published=False,
        ).first()
        if not editing_course:
            messages.error(request, 'That draft could not be found.')
            return redirect('teacher_atelier')

    if request.method == 'POST':
        if request.POST.get('action') == 'bulk_publish':
            course_ids = request.POST.getlist('course_ids')
            updated_count = Course.objects.filter(
                teacher=teacher,
                course_id__in=course_ids,
                is_published=False,
            ).update(is_published=True)
            if updated_count:
                messages.success(request, f'{updated_count} draft course(s) published successfully.')
            else:
                messages.info(request, 'Select at least one draft course to publish.')
            return redirect(f'{reverse("teacher_atelier")}?tab={"published" if updated_count else "drafts"}')

        posted_course_id = request.POST.get('course_id')
        if posted_course_id and (not editing_course or editing_course.course_id != posted_course_id):
            editing_course = Course.objects.filter(
                teacher=teacher,
                course_id=posted_course_id,
                is_published=False,
            ).first()
        form = CourseForm(request.POST, instance=editing_course)
        if form.is_valid():
            course = form.save(commit=False)
            course.teacher = teacher
            course.is_published = request.POST.get('action') == 'publish'
            course.save()
            if course.is_published:
                messages.success(request, f'Your course "{course.title}" is now published.')
            else:
                messages.success(request, f'Your course "{course.title}" has been saved as a draft.')
            tab = 'published' if course.is_published else 'drafts'
            return redirect(f'{reverse("teacher_atelier")}?tab={tab}')
    else:
        form = CourseForm(instance=editing_course)

    courses = Course.objects.filter(teacher=teacher).order_by('-created_at')
    published_courses = courses.filter(is_published=True)
    draft_courses = courses.filter(is_published=False)
    return render(request, 'Knot_Teacher/atelier.html', {
        'form': form,
        'published_courses': published_courses,
        'draft_courses': draft_courses,
        'published_count': published_courses.count(),
        'draft_count': draft_courses.count(),
        'editing_course': editing_course,
        'student_count': Enrollment.objects.filter(course__teacher=teacher).count(),
        'category_options': [
            {'value': value, 'label': label, 'icon': Course.CATEGORY_ICONS.get(value, 'bi-book')}
            for value, label in Course.CATEGORY_CHOICES
        ],
        'level_options': [
            {'value': value, 'label': label, 'icon': Course.LEVEL_ICONS.get(value, 'bi-signal')}
            for value, label in Course.LEVEL_CHOICES
        ],
    })

@login_required(login_url='login')
def teacher_cohort(request):
    teacher = getattr(request.user, 'teacher_profile', None)
    if not teacher:
        return redirect_user_by_role(request.user)
    query = request.GET.get('q', '').strip()
    segment = request.GET.get('segment', 'all')
    cohort_base = Enrollment.objects.filter(course__teacher=teacher).select_related(
        'student__user', 'course',
    ).order_by('-enrolled_at')
    all_enrollments = list(cohort_base)
    spotlight_enrollment = max(
        all_enrollments,
        key=lambda item: (item.progress_percent, item.last_accessed_at or item.enrolled_at),
        default=None,
    )
    today = timezone.localdate()
    month_ago = timezone.now() - timedelta(days=30)
    week_ago = timezone.now() - timedelta(days=7)
    student_ids = {item.student_id for item in all_enrollments}
    progress_values = [item.progress_percent for item in all_enrollments]
    metrics = {
        'total_students': len(student_ids),
        'active_learners': len({item.student_id for item in all_enrollments if item.last_accessed_at and item.last_accessed_at >= week_ago}),
        'new_students': len({item.student_id for item in all_enrollments if item.enrolled_at >= month_ago}),
        'needs_attention': len({item.student_id for item in all_enrollments if item.progress_percent < 35}),
        'graduating': len({item.student_id for item in all_enrollments if item.progress_percent >= 80}),
        'avg_progress': round(sum(progress_values) / len(progress_values)) if progress_values else 0,
        'avg_tenure_months': round(sum((timezone.now() - item.enrolled_at).days for item in all_enrollments) / max(len(all_enrollments), 1) / 30),
        'joined_label': min((item.enrolled_at for item in all_enrollments), default=None),
    }
    enrollments = cohort_base
    if query:
        enrollments = enrollments.filter(
            Q(student__user__first_name__icontains=query) |
            Q(student__user__last_name__icontains=query) |
            Q(course__title__icontains=query)
        )
    if segment == 'needs':
        enrollments = enrollments.filter(progress_percent__lt=35)
    elif segment == 'thriving':
        enrollments = enrollments.filter(progress_percent__gte=70)
    elif segment == 'new':
        enrollments = enrollments.filter(progress_percent=0)
    segment_counts = {
        'all': metrics['total_students'],
        'thriving': len({item.student_id for item in all_enrollments if item.progress_percent >= 70}),
        'steady': len({item.student_id for item in all_enrollments if 35 <= item.progress_percent < 70}),
        'new': metrics['new_students'],
        'needs': metrics['needs_attention'],
    }
    return render(request, 'Knot_Teacher/cohort.html', {
        'cohort_enrollments': enrollments,
        'cohort_count': enrollments.values('student_id').distinct().count(),
        'cohort_query': query,
        'cohort_segment': segment,
        'cohort_metrics': metrics,
        'cohort_segment_counts': segment_counts,
        'spotlight_enrollment': spotlight_enrollment,
    })

@login_required(login_url='login')
def teacher_studio(request):
    teacher = getattr(request.user, 'teacher_profile', None)
    if not teacher:
        return redirect_user_by_role(request.user)
    sessions = LearningSession.objects.filter(teacher=teacher).select_related(
        'student__user', 'course',
    )
    active_session = sessions.filter(status='live').first()
    next_session = sessions.filter(status='scheduled', starts_at__gte=timezone.now()).first()
    active_hands = SessionHand.objects.filter(
        session=active_session,
        resolved_at__isnull=True,
    ).select_related('student__user') if active_session else SessionHand.objects.none()
    return render(request, 'Knot_Teacher/studio.html', {
        'studio_sessions': sessions,
        'upcoming_sessions': sessions.filter(status='scheduled', starts_at__gte=timezone.now()),
        'completed_sessions': sessions.filter(status='completed'),
        'active_session': active_session,
        'next_session': next_session,
        'active_hands': active_hands,
        'recordings': StudioRecording.objects.filter(teacher=teacher).select_related('course', 'session'),
        'teacher_courses': Course.objects.filter(teacher=teacher, is_published=True).order_by('title'),
        'teacher_students': Student.objects.filter(enrollments__course__teacher=teacher).distinct().select_related('user').order_by('user__first_name', 'user__last_name'),
    })


@login_required(login_url='login')
def live_classroom(request, room_id):
    session = LearningSession.objects.filter(room_id=room_id).select_related('teacher__user', 'course').first()
    if not session:
        messages.error(request, 'That live classroom could not be found.')
        return redirect('student_sessions')
    teacher = getattr(request.user, 'teacher_profile', None)
    student = getattr(request.user, 'student_profile', None)
    is_teacher = bool(teacher and session.teacher_id == teacher.id)
    is_student = bool(student and session.student_id == student.id)
    is_participant = SessionParticipant.objects.filter(session=session, user=request.user).exists()
    if not (is_teacher or is_student or is_participant):
        messages.error(request, 'You are not enrolled in this classroom.')
        return redirect('student_sessions' if student else 'teacher_studio')
    participant, _ = SessionParticipant.objects.get_or_create(
        session=session,
        user=request.user,
        defaults={'role': 'host' if is_teacher else 'student'},
    )
    return render(request, 'Knot/learning_room.html', {
        'session': session,
        'participant': participant,
        'is_teacher': is_teacher,
        'participants': session.participants.select_related('user').order_by('role', 'user__first_name'),
        'hands': session.raised_hands.filter(resolved_at__isnull=True).select_related('student__user'),
        'notes': SessionNote.objects.filter(session=session, user=request.user).first(),
    })


@login_required(login_url='login')
def teacher_recording_action(request):
    if request.method != 'POST':
        return redirect('teacher_studio')
    teacher = getattr(request.user, 'teacher_profile', None)
    if not teacher:
        return redirect_user_by_role(request.user)
    action = request.POST.get('action')
    recording_id = request.POST.get('recording_id')
    recording = StudioRecording.objects.filter(id=recording_id, teacher=teacher).first() if recording_id else None
    if action == 'start':
        session = LearningSession.objects.filter(teacher=teacher, status='scheduled', started_at__isnull=False).first()
        recording = StudioRecording.objects.create(
            teacher=teacher,
            session=session,
            course=session.course if session else None,
            title=session.title if session else 'Studio recording',
            status='processing',
            mode=request.POST.get('mode', 'camera'),
        )
        return JsonResponse({'ok': True, 'recording_id': recording.id})
    if not recording:
        return JsonResponse({'ok': False, 'error': 'Recording not found.'}, status=404)
    if action == 'stop':
        recording.duration_seconds = max(0, int(request.POST.get('duration_seconds') or 0))
        recording.status = 'draft'
        recording.save(update_fields=('duration_seconds', 'status'))
    elif action == 'publish':
        recording.status = 'published'
        recording.save(update_fields=('status',))
    elif action == 'archive':
        recording.status = 'archived'
        recording.save(update_fields=('status',))
    elif action == 'restore':
        recording.status = 'draft'
        recording.save(update_fields=('status',))
    return JsonResponse({'ok': True, 'status': recording.status})


@login_required(login_url='login')
def teacher_start_session(request):
    if request.method != 'POST':
        return redirect('teacher_studio')
    teacher = getattr(request.user, 'teacher_profile', None)
    if not teacher:
        return redirect_user_by_role(request.user)
    title = request.POST.get('title', 'Live learning session').strip() or 'Live learning session'
    starts_at = request.POST.get('starts_at')
    try:
        parsed_start = datetime.fromisoformat(starts_at) if starts_at else timezone.now()
        if timezone.is_naive(parsed_start):
            parsed_start = timezone.make_aware(parsed_start)
    except (TypeError, ValueError):
        parsed_start = timezone.now()
    duration = int(request.POST.get('duration_minutes') or 45)
    session_type = request.POST.get('session_type', 'one_to_one')
    description = request.POST.get('description', '').strip()
    course = Course.objects.filter(course_id=request.POST.get('course_id'), teacher=teacher).first()
    student_ids = request.POST.getlist('student_ids')
    students = Student.objects.filter(id__in=student_ids) if student_ids else Student.objects.filter(
        enrollments__course__teacher=teacher,
    ).distinct()
    created = 0
    for student in students:
        session = LearningSession.objects.create(
            student=student,
            teacher=teacher,
            course=course,
            title=title,
            starts_at=parsed_start,
            duration_minutes=max(15, min(duration, 240)),
            is_group=len(students) > 1 or session_type in ('group', 'cohort'),
            session_type=session_type,
            description=description,
            room_id=uuid4().hex,
        )
        SessionParticipant.objects.get_or_create(session=session, user=teacher.user, defaults={'role': 'host'})
        SessionParticipant.objects.get_or_create(session=session, user=student.user, defaults={'role': 'student'})
        created += 1
    messages.success(request, f'Session created for {created} student(s).')
    return redirect('teacher_studio')


def teacher_schedule_session(request):
    if request.method != 'POST':
        return redirect('teacher_studio')
    request_data = request.POST.copy()
    request_data['starts_at'] = f"{request.POST.get('date')}T{request.POST.get('time')}"
    request_data['action'] = 'schedule'
    request._post = request_data
    return teacher_start_session(request)


@login_required(login_url='login')
def teacher_session_action(request, session_id):
    if request.method != 'POST':
        return redirect('teacher_studio')
    teacher = getattr(request.user, 'teacher_profile', None)
    session = LearningSession.objects.filter(id=session_id, teacher=teacher).first()
    if not session:
        messages.error(request, 'That session is not available to you.')
        return redirect('teacher_studio')
    action = request.POST.get('action')
    now = timezone.now()
    if action == 'start':
        session.status = 'live'
        session.started_at = now
        session.save(update_fields=('status', 'started_at'))
        messages.success(request, f'{session.title} is now live.')
    elif action == 'end':
        session.status = 'completed'
        session.ended_at = now
        session.save(update_fields=('status', 'ended_at'))
        messages.success(request, f'{session.title} has ended.')
    elif action == 'resolve_hand':
        hand_id = request.POST.get('hand_id')
        SessionHand.objects.filter(id=hand_id, session=session, resolved_at__isnull=True).update(resolved_at=now)
    elif action == 'save_note':
        SessionNote.objects.update_or_create(
            session=session,
            user=request.user,
            defaults={'content': request.POST.get('content', '')},
        )
    elif action == 'attendance':
        SessionAttendance.objects.update_or_create(
            session=session,
            student_id=request.POST.get('student_id'),
            defaults={'status': request.POST.get('status', 'present')},
        )
    return redirect('teacher_studio')

def teacher_grading(request):
    return render(request, 'Knot_Teacher/grading.html')

def teacher_assignments(request):
    return render(request, 'Knot_Teacher/assignments.html')

def teacher_seminar(request):
    return render(request, 'Knot_Teacher/seminar.html')

def teacher_messages(request):
    return render(request, 'Knot_Teacher/messages.html')

def teacher_enrolments(request):
    return render(request, 'Knot_Teacher/enrolments.html')

def teacher_network(request):
    return render(request, 'Knot_Teacher/network.html')

def teacher_reviews(request):
    return render(request, 'Knot_Teacher/reviews.html')

def teacher_analytics(request):
    return render(request, 'Knot_Teacher/analytics.html')

def teacher_honours(request):
    return render(request, 'Knot_Teacher/honours.html')

def teacher_earnings(request):
    return render(request, 'Knot_Teacher/earnings.html')

def teacher_settings(request):
    return render(request, 'Knot_Teacher/settings.html')

def teacher_help(request):
    return render(request, 'Knot_Teacher/help.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('login')


# MENTOR VIEWS SECTIONS

def mentor_dashboard(request):
    return render(request, 'Knot_Mentor/mentor_dashboard.html')

def mentor_mentees(request):
    return render(request, 'Knot_Mentor/mentees.html')

def mentor_requests(request):
    return render(request, 'Knot_Mentor/requests.html')

def mentor_sessions(request):
    return render(request, 'Knot_Mentor/sessions.html')

def mentor_mentoring_plans(request):
    return render(request, 'Knot_Mentor/mentoring_plans.html')

def mentor_messages(request):
    return render(request, 'Knot_Mentor/messages.html')

def mentor_forum(request):
    return render(request, 'Knot_Mentor/forum.html')

def mentor_network(request):
    return render(request, 'Knot_Mentor/network.html')

def mentor_resources(request):
    return render(request, 'Knot_Mentor/resources.html')

def mentor_reviews(request):
    return render(request, 'Knot_Mentor/reviews.html')

def mentor_analytics(request):
    return render(request, 'Knot_Mentor/analytics.html')

def mentor_honours(request):
    return render(request, 'Knot_Mentor/honours.html')

def mentor_earnings(request):
    return render(request, 'Knot_Mentor/earnings.html')

def mentor_settings(request):
    return render(request, 'Knot_Mentor/settings.html')

def mentor_help(request):
    return render(request, 'Knot_Mentor/help.html')

def mentor_dossier(request):
    return render(request, 'Knot_Mentor/dossier.html')


def mentor_sign_out(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('login')




# MENTOR VIEWS SECTIONS

def admin_dashboard(request):
    return render(request, 'Knot_Admin/admin_dashboard.html')

def admin_live_pulse(request):
    return render(request, 'Knot_Admin/live_pulse.html')

def admin_analytics(request):
    return render(request, 'Knot_Admin/analytics.html')

def admin_members(request):
    return render(request, 'Knot_Admin/members.html')

def admin_verifications(request):
    return render(request, 'Knot_Admin/verifications.html')

def admin_roles_and_permissions(request):
    return render(request, 'Knot_Admin/roles_and_permissions.html')

def admin_invitations(request):
    return render(request, 'Knot_Admin/invitations.html')

def admin_courses(request):
    return render(request, 'Knot_Admin/courses.html')

def admin_moderation(request):
    return render(request, 'Knot_Admin/moderation.html')

def admin_reports(request):
    return render(request, 'Knot_Admin/reports.html')

def admin_finance_and_payouts(request):
    return render(request, 'Knot_Admin/finance_and_payouts.html')

def admin_announcements(request):
    return render(request, 'Knot_Admin/announcements.html')

def admin_support_tickets(request):
    return render(request, 'Knot_Admin/support_tickets.html')

def admin_audit(request):
    return render(request, 'Knot_Admin/audit.html')

def admin_integrations(request):
    return render(request, 'Knot_Admin/integrations.html')

def admin_signal_tower(request):
    return render(request, 'Knot_Admin/signal_tower.html')

def admin_settings(request):
    return render(request, 'Knot_Admin/settings.html')

def admin_help(request):
    return render(request, 'Knot_Admin/help.html')

def admin_profile(request):
    return render(request, 'Knot_Admin/profile.html')

def admin_billing(request):
    return render(request, 'Knot_Admin/billing.html')

def admin_status(request):
    return render(request, 'Knot_Admin/status.html')

def admin_sign_up(request):
    return render(request, 'Auth/admin/sign_up.html')

def admin_login(request):
    return render(request, 'Auth/admin/login.html')



def admin_sign_out(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('login')

