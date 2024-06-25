from django.test import TestCase
from django.contrib.auth import get_user_model
from growth_forge.models import Profile
from projects.models import Project

User = get_user_model()

class ProfileTests(TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a user for testing
        cls.user = User.objects.create_user(
            # username='testuser2', 
            password='testpassword2', 
            email='test@test.com'
        )
        cls.user2 = User.objects.create_user(email='testuser2@example.com', password='testpassword')

    @classmethod
    def tearDownClass(cls):
        # Create a user for testing
        cls.user.delete() 

        cls.user2.delete() 

    def test_create_profile(self):
        # The Profile should be created automatically due to the post_save signal
        profile = Profile.objects.get(user=self.user)
        self.assertIsNotNone(
            profile
        )
        self.assertEqual(
            profile.user.email, 
            'test@test.com'
        )

    def test_retrieve_profile(self):
        profile = Profile.objects.get(user=self.user)
        retrieved_profile = Profile.objects.get(id=profile.id)
        self.assertEqual(retrieved_profile.user.email, 'test@test.com')

    def test_update_profile(self):
        profile, _ = Profile.objects.get_or_create(user=self.user)
        # Create a Project instance and add it to the profile's projects
        project = Project.objects.create(name='Test Project')
        profile.projects.add(project)
        # Verify the profile has the project added
        self.assertIn(project, profile.projects.all())
       

    def test_delete_profile(self):
        profile = Profile.objects.get(user=self.user)
        profile_id = profile.id
        profile.delete()
        with self.assertRaises(Profile.DoesNotExist):
            Profile.objects.get(id=profile_id)