from django.contrib import admin

from profiles.models  import UserProfile, Follow


@admin.register(UserProfile)
class FollowAdmin(admin.ModelAdmin):
    list_display =['user', 'birth_date']
    
@admin.register(Follow)
class UserProfileAdmin(admin.ModelAdmin):
    list_display =['follower', 'following', 'created_at']