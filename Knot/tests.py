from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from tempfile import TemporaryDirectory

from Knot.models import (
    CommunityBookmark,
    CommunityPost,
    CommunityPollOption,
    CommunityPollVote,
    CommunityReaction,
    CommunityReply,
    Course,
    HelpfulnessFeedback,
    Mentor,
    OnboardingProfile,
    PeopleRequest,
    Student,
    StudentPrivate,
    SupportTicket,
    Teacher,
)


class RoleBasedRegistrationTests(TestCase):
    def test_student_registration_creates_private_student_profile(self):
        user = User.objects.create_user(username='student@example.com', email='student@example.com', password='secret123')
        OnboardingProfile.objects.create(user=user, role='student')
        Student.objects.create(user=user, skill_level='Beginner', primary_subject='Python')
        StudentPrivate.objects.create(user=user, learning_goal='Build Python skills')

        self.assertTrue(Student.objects.filter(user=user).exists())
        self.assertEqual(user.onboarding_profile.role, 'student')

    def test_teacher_registration_creates_private_teacher_profile(self):
        user = User.objects.create_user(username='teacher@example.com', email='teacher@example.com', password='secret123')
        OnboardingProfile.objects.create(user=user, role='teacher')
        Teacher.objects.create(user=user, years_experience=5, current_job_title='Senior Engineer', teaching_style='Project-based')

        self.assertTrue(Teacher.objects.filter(user=user).exists())
        self.assertEqual(user.onboarding_profile.role, 'teacher')

    def test_mentor_registration_creates_private_mentor_profile(self):
        user = User.objects.create_user(username='mentor@example.com', email='mentor@example.com', password='secret123')
        OnboardingProfile.objects.create(user=user, role='mentor')
        Mentor.objects.create(user=user, mentorship_areas='Product Design', current_role_company='Knotwork', mentorship_type='1:1')

        self.assertTrue(Mentor.objects.filter(user=user).exists())
        self.assertEqual(user.onboarding_profile.role, 'mentor')


class StudentBrowseTests(TestCase):
    def setUp(self):
        self.student_user = User.objects.create_user(
            username='browse-student@example.com',
            email='browse-student@example.com',
            password='secret123',
            first_name='Browse',
            last_name='Student',
        )
        OnboardingProfile.objects.create(user=self.student_user, role='student')
        self.student = Student.objects.create(user=self.student_user, primary_subject='Python')
        self.client.force_login(self.student_user)

    def make_student(self, index):
        user = User.objects.create_user(
            username=f'learner{index}@example.com',
            email=f'learner{index}@example.com',
            first_name=f'Learner{index}',
        )
        OnboardingProfile.objects.create(user=user, role='student', bio=f'Learning Python {index}')
        return Student.objects.create(user=user, primary_subject='Python', skill_level='Beginner')

    def test_browse_lists_real_members_and_applies_search(self):
        member = self.make_student(1)

        response = self.client.get('/student/browse', {'q': 'Learner1'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Learner1')
        self.assertNotContains(response, 'Amara Okoye')
        self.assertEqual(response.context['result_count'], 1)
        self.assertEqual(response.context['people'][0]['user'], member.user)

    def test_browse_pagination_has_working_previous_and_next_links(self):
        for index in range(10):
            self.make_student(index)

        response = self.client.get('/student/browse', {'page': 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['people']), 1)
        self.assertContains(response, 'page=1')
        self.assertContains(response, 'Previous page')
        self.assertContains(response, 'Next page')

    def test_connect_action_persists_once(self):
        member = self.make_student(2)
        action_url = f'/student/browse/{member.user_id}/action'

        first_response = self.client.post(action_url, {'action': 'connection', 'next': '/student/browse?role=student'})
        second_response = self.client.post(action_url, {'action': 'connection', 'next': '/student/browse?role=student'})

        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(second_response.status_code, 302)
        self.assertEqual(PeopleRequest.objects.filter(from_user=self.student_user, to_user=member.user).count(), 1)

    def test_teacher_course_action_filters_find_courses(self):
        teacher_user = User.objects.create_user(
            username='browse-teacher@example.com',
            email='browse-teacher@example.com',
            first_name='Course',
            last_name='Teacher',
        )
        OnboardingProfile.objects.create(user=teacher_user, role='teacher')
        teacher = Teacher.objects.create(user=teacher_user, current_job_title='Python coach')
        course = Course.objects.create(
            teacher=teacher,
            title='Python foundations',
            category='Backend',
            description='Learn Python fundamentals.',
            price=0,
        )

        browse_response = self.client.get('/student/browse', {'role': 'teacher'})
        courses_response = self.client.get('/student/courses', {'teacher_id': teacher_user.id})

        self.assertContains(browse_response, 'Course Teacher')
        self.assertContains(browse_response, f'teacher_id={teacher_user.id}')
        self.assertEqual(courses_response.status_code, 200)
        self.assertEqual(list(courses_response.context['courses']), [course])

    def test_incoming_request_can_be_accepted_from_browse_and_appears_in_connections(self):
        sender = self.make_student(20)
        request_record = PeopleRequest.objects.create(
            from_user=sender.user,
            to_user=self.student_user,
            request_type='connection',
        )

        browse_response = self.client.get('/student/browse')
        self.assertContains(browse_response, 'Accept')
        accept_response = self.client.post(
            f'/student/browse/{sender.user_id}/action',
            {'action': 'accept', 'next': '/student/browse'},
        )

        self.assertEqual(accept_response.status_code, 302)
        request_record.refresh_from_db()
        self.assertEqual(request_record.status, 'accepted')
        connections_response = self.client.get('/student/my-connections')
        self.assertContains(connections_response, sender.user.first_name)
        self.assertEqual(connections_response.context['connection_count'], 1)

    def test_requests_page_accept_and_decline_persist(self):
        first_sender = self.make_student(21)
        second_sender = self.make_student(22)
        accepted = PeopleRequest.objects.create(from_user=first_sender.user, to_user=self.student_user, request_type='connection')
        declined = PeopleRequest.objects.create(from_user=second_sender.user, to_user=self.student_user, request_type='connection')

        response = self.client.get('/student/requests')
        self.assertContains(response, first_sender.user.first_name)
        self.client.post(f'/student/requests/{accepted.id}/action', {'action': 'accept', 'next': '/student/requests'})
        self.client.post(f'/student/requests/{declined.id}/action', {'action': 'decline', 'next': '/student/requests'})

        accepted.refresh_from_db()
        declined.refresh_from_db()
        self.assertEqual(accepted.status, 'accepted')
        self.assertEqual(declined.status, 'declined')

    def test_skill_match_connect_and_pass_update_requests(self):
        StudentPrivate.objects.create(user=self.student_user, learning_goal='Learn Python programming')
        teacher_user = User.objects.create_user(
            username='match-teacher@example.com',
            email='match-teacher@example.com',
            first_name='Python',
            last_name='Teacher',
        )
        OnboardingProfile.objects.create(user=teacher_user, role='teacher')
        teacher = Teacher.objects.create(user=teacher_user, current_job_title='Python instructor')
        Course.objects.create(
            teacher=teacher,
            title='Python programming',
            category='Backend',
            description='Python foundations.',
            price=0,
        )

        matches_response = self.client.get('/student/skill-matches')
        self.assertContains(matches_response, 'Python Teacher')
        self.assertEqual(matches_response.context['match_count'], 1)
        action_url = f'/student/browse/{teacher_user.id}/action'
        self.client.post(action_url, {'action': 'connection', 'next': '/student/skill-matches'})
        outgoing = PeopleRequest.objects.get(from_user=self.student_user, to_user=teacher_user, request_type='connection')
        self.assertEqual(outgoing.status, 'pending')

        self.client.post(action_url, {'action': 'pass', 'next': '/student/skill-matches'})
        outgoing.refresh_from_db()
        self.assertEqual(outgoing.status, 'passed')

    def test_withdraw_from_requests_page_updates_connections_sent_list(self):
        recipient = self.make_student(23)
        outgoing = PeopleRequest.objects.create(from_user=self.student_user, to_user=recipient.user, request_type='connection')

        response = self.client.get('/student/requests', {'tab': 'sent'})
        self.assertContains(response, recipient.user.first_name)
        self.client.post(f'/student/requests/{outgoing.id}/action', {'action': 'withdraw', 'next': '/student/requests?tab=sent'})

        outgoing.refresh_from_db()
        self.assertEqual(outgoing.status, 'withdrawn')
        connections_response = self.client.get('/student/my-connections')
        self.assertEqual(connections_response.context['sent_count'], 0)


class StudentCommunityAchievementsHelpTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='community-student@example.com',
            email='community-student@example.com',
            password='secret123',
            first_name='Community',
            last_name='Student',
        )
        OnboardingProfile.objects.create(user=self.user, role='student')
        self.student = Student.objects.create(user=self.user, primary_subject='Python')
        self.client.force_login(self.user)

    def test_community_post_reply_reaction_and_bookmark_persist(self):
        response = self.client.post('/student/community/action', {
            'action': 'create',
            'title': 'How should I practice Python?',
            'body': 'I want a small daily exercise plan.',
            'category': 'question',
        })
        post = CommunityPost.objects.get(author=self.user)
        self.assertEqual(response.status_code, 302)
        self.client.post(f'/student/community/{post.id}/action', {'action': 'reply', 'body': 'Start with a short script.'})
        self.client.post(f'/student/community/{post.id}/action', {'action': 'upvote'})
        self.client.post(f'/student/community/{post.id}/action', {'action': 'bookmark'})
        self.assertEqual(CommunityReply.objects.filter(post=post, author=self.user).count(), 1)
        self.assertTrue(CommunityReaction.objects.filter(post=post, user=self.user).exists())
        self.assertTrue(CommunityBookmark.objects.filter(post=post, user=self.user).exists())
        feed = self.client.get('/student/community', {'category': 'question'})
        self.assertContains(feed, 'How should I practice Python?')
        self.assertEqual(feed.context['post_count'], 1)

    def test_community_text_only_composer_derives_post_title(self):
        response = self.client.post('/student/community/action', {
            'action': 'create',
            'body': 'A text-only post from the community composer.\nMore detail follows.',
            'category': 'showcase',
        })

        post = CommunityPost.objects.get(author=self.user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(post.title, 'A text-only post from the community composer.')
        self.assertEqual(post.body, 'A text-only post from the community composer.\nMore detail follows.')
        self.assertEqual(post.category, 'showcase')

    def test_community_composer_saves_image_tags_poll_and_vote(self):
        png_data = (
            b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01'
            b'\x00\x00\x00\x01\x08\x04\x00\x00\x00\xb5\x1c\x0c\x02'
            b'\x00\x00\x00\x0bIDATx\xdac\xf8\x0f\x00\x01\x01\x01\x00'
            b'\x18\xdd\x8d\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
        )
        with TemporaryDirectory() as media_dir, override_settings(MEDIA_ROOT=media_dir):
            response = self.client.post('/student/community/action', {
                'action': 'create',
                'body': 'Which approach should we use?',
                'category': 'question',
                'tags': 'python, #django',
                'poll_option': ['Option A', 'Option B'],
                'image': SimpleUploadedFile('diagram.png', png_data, content_type='image/png'),
            })

            post = CommunityPost.objects.get(author=self.user)
            options = list(CommunityPollOption.objects.filter(post=post).order_by('id'))
            self.assertEqual(response.status_code, 302)
            self.assertEqual(post.tags, 'python, django')
            self.assertTrue(post.image.storage.exists(post.image.name))
            self.assertEqual([option.text for option in options], ['Option A', 'Option B'])

            self.client.post(f'/student/community/{post.id}/action', {
                'action': 'poll_vote',
                'option_id': options[0].id,
            })
            self.client.post(f'/student/community/{post.id}/action', {
                'action': 'poll_vote',
                'option_id': options[1].id,
            })

            vote = CommunityPollVote.objects.get(post=post, user=self.user)
            self.assertEqual(vote.option_id, options[1].id)

    def test_community_delete_is_limited_to_post_owner(self):
        author = User.objects.create_user(username='other-member@example.com')
        post = CommunityPost.objects.create(author=author, title='Member post', body='Keep this post.')

        self.client.post(f'/student/community/{post.id}/action', {'action': 'delete'})

        self.assertTrue(CommunityPost.objects.filter(pk=post.pk).exists())

    def test_achievements_derive_counts_from_student_records(self):
        response = self.client.get('/student/achievements')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['badge_count'], 11)
        self.assertEqual(response.context['unlocked_count'], 0)
        self.assertEqual(response.context['filter_name'], 'all')

    def test_help_ticket_feedback_and_close_are_persisted(self):
        response = self.client.post('/student/help/action', {
            'action': 'ticket',
            'category': 'community',
            'subject': 'Question about posting',
            'message': 'How do I format code in a community post?',
        })
        ticket = SupportTicket.objects.get(user=self.user)
        self.assertEqual(response.status_code, 302)
        self.client.post('/student/help/action', {'action': 'feedback', 'helpful': 'yes'})
        self.client.post('/student/help/action', {'action': 'close_ticket', 'ticket_id': ticket.id})
        ticket.refresh_from_db()
        self.assertEqual(ticket.status, 'closed')
        self.assertTrue(HelpfulnessFeedback.objects.get(user=self.user).was_helpful)
        self.assertContains(self.client.get('/student/help'), 'Question about posting')
