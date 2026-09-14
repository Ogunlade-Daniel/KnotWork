from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required


from django.contrib import messages, auth
from django.contrib.auth import login as auth_login
from .forms import LoginForm, OnboardingForm
from .models import OnboardingProfile, Student




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
    role = request.POST.get('role', 'student')
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
            profile_data = {
                field_name: data.get(field_name)
                for field_name in OnboardingForm.PROFILE_FIELDS
                if data.get(field_name) is not None
            }
            OnboardingProfile.objects.create(
                user=user,
                role=data['role'],
                **profile_data,
            )
            if data['role'] == 'student':
                Student.objects.create(user=user)
        messages.success(request, 'Your account is ready. You can log in now.')
        return redirect('login')

    return render(request, 'Auth/get_started.html', {'form': form, 'selected_role': role})

def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        auth_login(request, form.cleaned_data['user'])
        messages.success(request, "You have logged successfully in!")
        return redirect('student_dashboard')
    return render(request, 'Auth/login.html', {'form': form})



# STUDENT VIEWS SECTIONS
@login_required(login_url='login')
def student_dashboard(request):
    profile = getattr(request.user, 'onboarding_profile', None)
    mentor = {
        'initials': 'TF',
        'name': 'Tolu Fashina',
        'role': 'Senior Fullstack Mentor',
    }
    if profile and profile.current_role_company:
        mentor['role'] = profile.current_role_company

    return render(request, 'Knot_Student/student_dashboard.html', {'mentor': mentor})


def student_my_learning(request):
    return render(request, 'Knot_Student/my_learning.html')

def student_find_courses(request):
    return render(request, 'Knot_Student/find_courses.html')

def student_skill_matches(request):
    return render(request, 'Knot_Student/skill_matches.html')

def student_browse(request):
    return render(request, 'Knot_Student/browse.html')

def student_my_connections(request):
    return render(request, 'Knot_Student/my_connections.html')

def student_requests(request):
    return render(request, 'Knot_Student/requests.html')

def student_messages(request):
    return render(request, 'Knot_Student/messages.html')

def student_sessions(request):
    return render(request, 'Knot_Student/sessions.html')

def student_community(request):
    return render(request, 'Knot_Student/community.html')

def student_progress(request):
    return render(request, 'Knot_Student/progress.html')

def student_achievements(request):
    return render(request, 'Knot_Student/achievements.html')

def student_credits_and_billing(request):
    return render(request, 'Knot_Student/credits_and_billing.html')

def student_settings(request):
    return render(request, 'Knot_Student/settings.html')

def student_help(request):
    return render(request, 'Knot_Student/help_centre.html')

def student_profile(request):
    return render(request, 'Knot_Student/profile.html')


def student_logout(request):
    auth.logout(request)
    messages.success(request, "You have successfully logged out!")
    return redirect('/login')


# TEACHER VIEWS SECTIONS
def teacher_dashboard(request):
    return render(request, 'Knot_Teacher/teacher_dashboard.html')

def teacher_atelier(request):
    return render(request, 'Knot_Teacher/atelier.html')

def teacher_cohort(request):
    return render(request, 'Knot_Teacher/cohort.html')

def teacher_studio(request):
    return render(request, 'Knot_Teacher/studio.html')

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

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')

def teacher_dossier(request):
    return render(request, 'Knot_Teacher/dossier.html')





# MENTOR VIEWS SECTIONS

def admin_dashboard(request):
    return render(request, 'Knot_Teacher/admin_dashboard.html')







