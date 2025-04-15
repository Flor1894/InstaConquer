from .models import Post, Comment
from django import forms


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
          'image',
          'caption'
        ]


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
          'text',
        ]
    
    def save(self):
        user = super().save(commit=True)
        user.set_password(self.cleaned_data["password"])
        user.save()
        
        from profiles.models import UserProfile
        UserProfile.objects.create(user=user)
        
        return user
    
class LoginForm(forms.Form):
    username = forms.CharField(label="Email")
    password = forms.CharField(
        label="Password", widget=forms.PasswordInput())