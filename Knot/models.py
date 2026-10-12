from django.db import models
from django.contrib.auth.models import User


import uuid



class OnboardingProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('mentor', 'Mentor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='onboarding_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, db_index=True) # index for speed

    # Shared registration fields.
    first_name = models.CharField(max_length=80, blank=True)
    surname = models.CharField(max_length=80, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    timezone = models.CharField(max_length=100, blank=True)
    hear_about_us = models.CharField(max_length=100, blank=True)
    terms_accepted = models.BooleanField(default=False)
    email_marketing = models.BooleanField(default=False)

    # Shared registration data only. Role-specific data lives in private tables.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} ({self.get_role_display()})'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    skill_level = models.CharField(max_length=30, blank=True, null=True)
    primary_subject = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'student_profile'

    def __str__(self):
        return f'{self.user.email} (student)'

    @property
    def initials(self):
        first = self.user.first_name[0] if self.user.first_name else ""
        last = self.user.last_name[0] if self.user.last_name else ""

        if not first and not last:
            return self.user.email[0].upper() if self.user.email else "S"
        return f"{first}{last}".upper()


class StudentPrivate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_private')
    learning_goal = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    timezone = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'student_private'


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    years_experience = models.PositiveSmallIntegerField(null=True, blank=True)
    current_job_title = models.CharField(max_length=150, blank=True, default='')
    teaching_style = models.CharField(max_length=150, blank=True, default='')
    languages_spoken = models.CharField(max_length=255, blank=True, default='')
    portfolio_url = models.URLField(blank=True, default='')
    linkedin_url = models.URLField(blank=True, default='')
    github_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'teacher_profile'

    def __str__(self):
        return f'{self.user.email} (teacher)'

    @property
    def initials(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        return self.user.email[:2].upper()

class Course(models.Model):
    CATEGORY_CHOICES = [
        # --- Software Development - Phase 1 ---
        ('Frontend', 'Frontend Development'),
        ('Backend', 'Backend Development'),
        ('Fullstack', 'Fullstack Development'),
        ('Mobile', 'Mobile App Development'),
        ('Flutter', 'Flutter & Dart'),
        ('React Native', 'React Native'),

        # --- Design & Product - Phase 2 ---
        ('UI/UX', 'UI/UX Design'),
        ('Product Design', 'Product Design'),
        ('Product Management', 'Product Management'),
        ('No-Code', 'No-Code / Low-Code'),

        # --- Data & AI - Phase 3 ---
        ('Data Analysis', 'Data Analysis'),
        ('Data Science', 'Data Science'),
        ('Machine Learning', 'Machine Learning & AI'),
        ('Prompt Engineering', 'Prompt Engineering / GenAI'),

        # --- Cloud & DevOps - Phase 4 ---
        ('DevOps', 'DevOps & Cloud'),
        ('Cybersecurity', 'Cybersecurity'),
        ('Blockchain', 'Blockchain & Web3'),

        # --- Other Tech - Phase 5 ---
        ('Game Dev', 'Game Development'),
        ('Embedded', 'Embedded Systems / IoT'),
        ('QA Testing', 'QA & Software Testing'),
        ('Digital Marketing', 'Tech Marketing & Growth'),
    ]
        
    LEVEL_CHOICES = [
        ('All Levels', 'All Levels'),
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Expert', 'Expert / Professional'),
    ]

    CATEGORY_ICONS = {
        'Frontend': 'bi-code-slash', 'Backend': 'bi-hdd-stack',
        'Fullstack': 'bi-layers', 'Mobile': 'bi-phone',
        'Flutter': 'bi-phone-landscape', 'React Native': 'bi-phone-vibrate',
        'UI/UX': 'bi-palette', 'Product Design': 'bi-brush',
        'Product Management': 'bi-kanban', 'No-Code': 'bi-magic',
        'Data Analysis': 'bi-bar-chart-line', 'Data Science': 'bi-graph-up',
        'Machine Learning': 'bi-cpu', 'Prompt Engineering': 'bi-robot',
        'DevOps': 'bi-cloud-check', 'Cybersecurity': 'bi-shield-lock',
        'Blockchain': 'bi-link-45deg', 'Game Dev': 'bi-controller',
        'Embedded': 'bi-motherboard', 'QA Testing': 'bi-bug',
        'Digital Marketing': 'bi-megaphone',
    }

    LEVEL_ICONS = {
        'All Levels': 'bi-stars', 'Beginner': 'bi-mortarboard',
        'Intermediate': 'bi-bar-chart-steps', 'Advanced': 'bi-rocket-takeoff',
        'Expert': 'bi-trophy',
    }

    course_id = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True) # primary_key=True for make the customized ID the main ID

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES) # FIRST
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Beginner') # SECOND
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0) # 0 = free
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.course_id:
            # Format: KNT-FRO-A1B2C3
            prefix = self.category[:3].upper() if self.category else 'KNT'
            code = uuid.uuid4().hex[:6].upper()
            new_id = f'KNT-{prefix}-{code}'
            while Course.objects.filter(course_id=new_id).exists():
                code = uuid.uuid4().hex[:6].upper()
                new_id = f'KNT-{prefix}-{code}'
            self.course_id = new_id
        super().save(*args, **kwargs)

    def get_category_icon(self):
        return self.CATEGORY_ICONS.get(self.category, 'bi-book')

    def get_level_icon(self):
        return self.LEVEL_ICONS.get(self.level, 'bi-signal')
    
    def __str__(self):
        return f'{self.course_id} - {self.title}'

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    progress_percent = models.PositiveSmallIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_accessed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'course') # no double enroll

    @property
    def is_completed(self):
        return self.completed_at is not None or self.progress_percent >= 100


class SavedCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='saved_courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('student', 'course'), name='unique_saved_course'),
        ]
        ordering = ('-saved_at',)


class Certificate(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificates')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='certificates')
    certificate_id = models.CharField(max_length=24, unique=True)
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('student', 'course'), name='unique_student_certificate'),
        ]
        ordering = ('-issued_at',)


class LearningDeadline(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='deadlines')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='deadlines', null=True, blank=True)
    title = models.CharField(max_length=200)
    due_at = models.DateTimeField()
    action_label = models.CharField(max_length=40, default='Open')
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ('due_at',)


class WeeklyGoal(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='weekly_goals')
    week_start = models.DateField()
    target_sessions = models.PositiveSmallIntegerField(default=5)
    completed_sessions = models.PositiveSmallIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('student', 'week_start'), name='unique_student_weekly_goal'),
        ]


class LearningSession(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('live', 'Live'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    TYPE_CHOICES = [
        ('one_to_one', '1-on-1 Video call'),
        ('group', 'Group call'),
        ('cohort', 'Cohort class'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='learning_sessions')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='learning_sessions')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='learning_sessions', null=True, blank=True)
    title = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    duration_minutes = models.PositiveSmallIntegerField(default=45)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    session_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='one_to_one')
    description = models.TextField(blank=True, default='')
    room_id = models.CharField(max_length=64, unique=True, null=True, blank=True)
    meeting_url = models.URLField(blank=True, default='')
    notes = models.TextField(blank=True, default='')
    is_group = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('starts_at',)


class SessionParticipant(models.Model):
    ROLE_CHOICES = [
        ('host', 'Host'),
        ('co_host', 'Co-host'),
        ('student', 'Student'),
        ('observer', 'Observer'),
    ]
    ATTENDANCE_CHOICES = [
        ('invited', 'Invited'),
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ]

    session = models.ForeignKey(LearningSession, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_participation')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    attendance = models.CharField(max_length=12, choices=ATTENDANCE_CHOICES, default='invited')
    joined_at = models.DateTimeField(null=True, blank=True)
    left_at = models.DateTimeField(null=True, blank=True)
    hand_raised = models.BooleanField(default=False)
    hand_raised_at = models.DateTimeField(null=True, blank=True)
    is_muted = models.BooleanField(default=True)
    is_cam_off = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('session', 'user'), name='unique_session_participant'),
        ]


class SessionHand(models.Model):
    session = models.ForeignKey(LearningSession, on_delete=models.CASCADE, related_name='raised_hands')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='raised_hands')
    asked_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('session', 'student'),
                name='unique_active_session_hand',
            ),
        ]


class StudioRecording(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='studio_recordings')
    session = models.ForeignKey(LearningSession, on_delete=models.SET_NULL, related_name='recordings', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='studio_recordings', null=True, blank=True)
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    mode = models.CharField(max_length=20, default='camera')
    duration_seconds = models.PositiveIntegerField(default=0)
    size_mb = models.DecimalField(max_digits=9, decimal_places=1, default=0)
    media_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)


class SessionAttendance(models.Model):
    STATUS_CHOICES = [('present', 'Present'), ('absent', 'Absent')]
    session = models.ForeignKey(LearningSession, on_delete=models.CASCADE, related_name='attendance')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='session_attendance')
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='absent')
    join_time = models.DateTimeField(null=True, blank=True)
    leave_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('session', 'student'), name='unique_session_attendance'),
        ]


class SessionNote(models.Model):
    session = models.ForeignKey(LearningSession, on_delete=models.CASCADE, related_name='session_notes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='session_notes')
    content = models.TextField(blank=True, default='')
    is_private = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('session', 'user'), name='unique_session_note_author'),
        ]

class TeacherPrivate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_private')
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    payment_method = models.CharField(max_length=80, blank=True, default='')
    availability = models.CharField(max_length=150, blank=True, default='')
    id_certificate = models.FileField(upload_to='private/teacher/id/', blank=True, null=True)
    background_check_consent = models.BooleanField(default=False)
    teacher_terms_accepted = models.BooleanField(default=False)

    class Meta:
        db_table = 'teacher_private'


class Mentor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_profile')
    mentorship_areas = models.CharField(max_length=255, blank=True, default='')
    industry_skills = models.CharField(max_length=255, blank=True, default='')
    current_role_company = models.CharField(max_length=180, blank=True, default='')
    mentor_bio = models.TextField(blank=True, default='')
    mentor_links = models.CharField(max_length=500, blank=True, default='')
    mentorship_type = models.CharField(max_length=100, blank=True, default='')
    languages_spoken = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = True
        db_table = 'mentor_profile'

    def __str__(self):
        return f'{self.user.email} (mentor)'

    @property
    def initials(self):
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name[0]}{self.user.last_name[0]}".upper()
        return self.user.email[:2].upper()


class MentorPrivate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='mentor_private')
    phone_number = models.CharField(max_length=25, null=True, blank=True)
    session_rate = models.CharField(max_length=80, blank=True, default='')
    max_students_per_month = models.PositiveSmallIntegerField(null=True, blank=True)
    mentor_id = models.FileField(upload_to='private/mentor/id/', blank=True, null=True)
    references = models.TextField(blank=True, default='')
    availability = models.CharField(max_length=150, blank=True, default='')
    mentor_terms_accepted = models.BooleanField(default=False)

    class Meta:
        db_table = 'mentor_private'


class PeopleRequest(models.Model):
    REQUEST_TYPES = [
        ('connection', 'Connection'),
        ('mentorship', 'Mentorship'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('withdrawn', 'Withdrawn'),
        ('passed', 'Passed'),
    ]

    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_people_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_people_requests')
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [
            models.UniqueConstraint(fields=('from_user', 'to_user', 'request_type'), name='unique_people_request'),
            models.CheckConstraint(check=~models.Q(from_user=models.F('to_user')), name='people_request_not_self'),
        ]


class CommunityPost(models.Model):
    CATEGORY_CHOICES = [
        ('discussion', 'Discussion'),
        ('question', 'Question'),
        ('showcase', 'Showcase'),
        ('feedback', 'Feedback'),
        ('jobs', 'Opportunities'),
        ('announce', 'Announcement'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_posts')
    title = models.CharField(max_length=180)
    body = models.TextField()
    image = models.FileField(upload_to='community/images/%Y/%m/', blank=True, null=True)
    tags = models.CharField(max_length=300, blank=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='discussion', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)


class CommunityPollOption(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='poll_options')
    text = models.CharField(max_length=100)

    class Meta:
        ordering = ('id',)


class CommunityPollVote(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='poll_votes')
    option = models.ForeignKey(CommunityPollOption, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_poll_votes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=('post', 'user'), name='unique_community_poll_vote')]


class CommunityReply(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_replies')
    body = models.TextField(max_length=3000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)


class CommunityReaction(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='reactions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_reactions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=('post', 'user'), name='unique_community_reaction')]


class CommunityBookmark(models.Model):
    post = models.ForeignKey(CommunityPost, on_delete=models.CASCADE, related_name='bookmarks')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='community_bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)
        constraints = [models.UniqueConstraint(fields=('post', 'user'), name='unique_community_bookmark')]


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    category = models.CharField(max_length=40, default='general')
    subject = models.CharField(max_length=180)
    message = models.TextField(max_length=5000)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated_at',)


class HelpfulnessFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='helpfulness_feedback')
    topic = models.CharField(max_length=80, default='help-centre')
    was_helpful = models.BooleanField()
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=('user', 'topic'), name='unique_helpfulness_feedback')]
