from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import MyUser, Event, Comment
from PIL import Image
import io

# Helper function to create a sample image file
def create_test_image():
    image = Image.new('RGB', (100, 100), color='white')
    byte_arr = io.BytesIO()
    image.save(byte_arr, format='JPEG')
    byte_arr.seek(0)
    return SimpleUploadedFile('test_image.jpg', byte_arr.read(), content_type='image/jpeg')

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_signup_view(self):
        # Simulate sending the verification code and set it in the session
        session = self.client.session
        session['verification_code'] = '123456'
        session['code_sent_at'] = timezone.now().timestamp()
        session.save()

        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpass123',
            'password_confirmation': 'testpass123',
            'verification_code': '123456',
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(MyUser.objects.filter(username='testuser').exists())

class EventTests(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(username='eventuser', password='testpass123')
        self.client.login(username='eventuser', password='testpass123')
        self.uploaded_image = create_test_image()

    def test_create_event(self):
        event_time = timezone.now().strftime('%Y-%m-%dT%H:%M')
        response = self.client.post(reverse('create_event'), {
            'title': 'Sample Event',
            'category': 'game',
            'event_time': event_time,
            'location': 'Sample Location',
            'description': 'This is a sample event.',
            'image': self.uploaded_image,
            'fee': 0,
            'max_participants': 10,
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(Event.objects.filter(title='Sample Event').exists())

class EventInteractionTests(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(username='interactuser', password='testpass123')
        self.client.login(username='interactuser', password='testpass123')
        self.event = Event.objects.create(
            title='Interact Event',
            category='music',
            event_time=timezone.now(),
            location='Interact Location',
            description='Sample description',
            image=create_test_image(),
            fee=0,
            max_participants=10,
            created_by=self.user,
        )

    def test_toggle_favorite(self):
        response = self.client.post(reverse('toggle_favorite', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.event.saved_by_users.filter(id=self.user.id).exists())

    def test_apply_event(self):
        response = self.client.post(reverse('apply_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.event.applied_by_users.filter(id=self.user.id).exists())

    def test_cancel_collection(self):
        self.event.saved_by_users.add(self.user)  # First, save the event
        response = self.client.post(reverse('cancel_collection', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.event.saved_by_users.filter(id=self.user.id).exists())

    def test_delete_event(self):
        response = self.client.post(reverse('delete_event', args=[self.event.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Event.objects.filter(id=self.event.id).exists())

    def test_post_comment(self):
        response = self.client.post(reverse('add_comment', args=[self.event.id]), {
            'content': 'This is a comment.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Comment.objects.filter(event=self.event, content='This is a comment.').exists())

class EventFilteringTests(TestCase):
    def setUp(self):
        self.user = MyUser.objects.create_user(username='filteruser', password='testpass123')
        self.client.login(username='filteruser', password='testpass123')
        self.event1 = Event.objects.create(
            title='Game Event',
            category='game',
            event_time=timezone.now(),
            location='Game Location',
            description='Game description',
            image=create_test_image(),
            fee=0,
            max_participants=10,
            created_by=self.user,
        )
        self.event2 = Event.objects.create(
            title='Music Event',
            category='music',
            event_time=timezone.now(),
            location='Music Location',
            description='Music description',
            image=create_test_image(),
            fee=0,
            max_participants=10,
            created_by=self.user,
        )

    def test_filtered_events_by_category(self):
        response = self.client.get(reverse('filtered_events', args=['game']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Game Event')
        self.assertNotContains(response, 'Music Event')

    def test_search_results(self):
        response = self.client.get(reverse('search_results'), {'search_query': 'Game'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Game Event')
        self.assertNotContains(response, 'Music Event')
