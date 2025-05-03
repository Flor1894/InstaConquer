from django.test import TestCase

from profiles.models import UserProfile, Follow, User
from django.contrib.auth.models import User

class UserProfileModelTest(TestCase):
    
    def setUp(self):
        
        self.user1 = User.objects.create_user(
            username="john",
            email="john@lennon.com",
            password="johnpassword"
        )
        
        self.user2 = User.objects.create_user(
            username="poul",
            email="poul@lennon.com",
            password="poulpassword"
        )
        
        self.profile1 = UserProfile.objects.create(
            user=self.user1,
            bio="Bio de John",
            birth_date="1990-01-01"
        )
        
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            bio="Bio de Paul",
            birth_date="1990-01-18"
        )
        
    def test_user_profile_creation(self):
           self.assertEqual(self.profile1.bio, "Bio de John")
           self.assertEqual(self.user1.username, "john")
           
    def test_follow_user(self):
        created = self.profile1.follow(self.profile2)
        self.assertTrue(created)
        self.assertTrue(Follow.objects.filter(follower=self.profile1, following=self.profile2).exists())
        created = self.profile1.follow(self.profile2)
        self.assertFalse(created)  # No se puede seguir a alguien que ya se sigue
        self.assertTrue(Follow.objects.filter(follower=self.profile1, following=self.profile2).exists())
        
    def test_unfollow_user(self):
        self.profile1.follow(self.profile2)
        self.assertTrue(Follow.objects.filter(follower=self.profile1, following=self.profile2).exists())
        self.profile1.unfollow(self.profile2)
        self.assertFalse(Follow.objects.filter(follower=self.profile1, following=self.profile2).exists())
        
    def test_str_userprofile(self):
        self.assertEqual(str(self.profile1), self.profile1.user.username)
        
class FollowModelTest(TestCase):
    def setUp(self):
        
        self.user1 = User.objects.create_user(
            username="john",
            email="john@lennon.com",
            password="johnpassword"
        )
        
        self.user2 = User.objects.create_user(
            username="poul",
            email="poul@lennon.com",
            password="poulpassword"
        )
        
        self.profile1 = UserProfile.objects.create(
            user=self.user1,
            bio="Bio de John",
            birth_date="1990-01-01"
        )
        
        self.profile2 = UserProfile.objects.create(
            user=self.user2,
            bio="Bio de Paul",
            birth_date="1990-01-18"
        )
        
        def test_unique_follow_once_time(self):
            Follow.objects.get_or_create(follower=self.profile1, following=self.profile2)
            self.assertEqual(Follow.objects.filter(follower=self.profile1, following=self.profile2).count(), 1)
            Follow.objects.get_or_create(follower=self.profile1, following=self.profile2)
            self.assertEqual(Follow.objects.filter(follower=self.profile1, following=self.profile2).count(), 1)