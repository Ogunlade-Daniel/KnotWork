from django.contrib import messages
from django.shortcuts import redirect, render



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
    return render(request, 'Knot_Base/pricing.html')

def about(request):
    return render(request, 'Knot_Base/about.html')

def blog(request):
    return render(request, 'Knot_Base/blog.html')

def help(request):
    return render(request, 'Knot_Base/help.html')





def get_started(request):
    return render(request, 'Auth/get_started.html')

def login(request):
    return render(request, 'Auth/login.html')


