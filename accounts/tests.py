from django.test import TestCase
from django.contrib.auth.forms import UserCreationForm
from .forms import UserProfileForm

from django.urls import reverse,resolve
from .views import signup,setup_profile
from django.contrib.auth.models import User

from .models import UserProfile
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile



class SignUpTests(TestCase):
    def setUp(self):
        url=reverse('signup')
        self.response=self.client.get(url)

    def test_signUp_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_signup_url_resolves_signup_view(self):
        view=resolve('/signup/')
        self.assertEquals(view.func, signup)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_contains_form(self):
        form=self.response.context.get('form')
        self.assertIsInstance(form,UserCreationForm)

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'john',
            'email':'john@gmail.com',
            'password1': 'abcdef123456',
            'password2': 'abcdef123456'
        }
        self.response = self.client.post(url, data)
        self.profile_setup_url = reverse('setup_profile')

    def test_redirection(self):
        self.assertRedirects(self.response,self.profile_setup_url)

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_user_authentication(self):
        response=self.client.get(self.profile_setup_url)
        user=response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {}
        self.response = self.client.post(url, data)

    def test_signup_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)    

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='PNG'):
    """
    Generate a test image, returning the filename that it was saved as.

    If ``storage`` is ``None``, the BytesIO containing the image data
    will be passed instead.
    """
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

class ProfileSetUpTests(TestCase):
    def setUp(self):
        user=User.objects.create(username='john',email='john@gmail.com',)
        user.set_password('abcdef123456')
        user.save()
        profile=UserProfile(profile_user=user)
        profile.profile_pic=None

        profile.save()

        self.client.login(username='john',password='abcdef123456')
        self.response =self.client.get(reverse('setup_profile'))

    def test_setup_profile_status_code(self):
        self.assertEquals(self.response.status_code,200)

    def test_setup_profile_url_resolves_setup_profile_url_view(self):
        view=resolve('/setup_profile/')
        self.assertEquals(view.func, setup_profile)

    def test_csrf(self):
        self.assertContains(self.response,'csrfmiddlewaretoken')

    def test_contains_form(self):
        form=self.response.context.get('form')
        self.assertIsInstance(form,UserProfileForm)

    def test_form_inputs(self):
        '''
        The view must contain five inputs: csrf, username, email,
        password1, password2
        '''
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="file"', 1)

class SuccesfulProfileSetUpTests(TestCase):
    def setUp(self):
        user=User.objects.create(username='john',email='john@gmail.com')
        user.set_password('abcdef123456')
        user.save()
        self.client.login(username='john',password='abcdef123456')
        profile_pic = SimpleUploadedFile("file.jpg", b"file_content", content_type="image")
        self.response=self.client.post(reverse('setup_profile'), {'profile_pic': profile_pic})
        
    def test_redirection(self):
        self.feed_url=reverse('feed')
        self.assertRedirects(self.response,self.feed_url)

