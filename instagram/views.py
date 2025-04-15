from django.shortcuts import render

from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic.edit import FormView
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistationForm, LoginForm
from django.views.generic import DetailView
from django.views.generic import ListView
from django.utils.decorators import method_decorator
from profiles.models import Follow

from profiles.forms import FollowForm

from profiles.models import UserProfile
from django.views.generic.edit import UpdateView
from posts.models import Post
from .forms import ProfileFollow



from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class HomeView(TemplateView):
    template_name = "general/home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #si el usuario esta logueado
        if self.request.user.is_authenticated:
            #obtenemos los posts de los usuarios que seguimos
            seguidos = Follow.objects.filter(follower=self.request.user.profile).values_list('following', flat=True)
            #Nos traemos los post de los usuarios que seguimos
            last_post = Post.objects.filter(user__profile__user__in=seguidos)
            
        else:
            last_post = Post.objects.all().order_by('-created_at')[:5]
        context['last_posts'] = last_post

        return context
    
class LoginView(FormView):
    template_name = "general/login.html"
    form_class = LoginForm

    def form_valid(self, form):
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=password)

        if user is not None:
            login(self.request, user)
            messages.add_message(self.request, messages.SUCCESS, f'Bienvenido de nuevo {user.username}')
            return HttpResponseRedirect(reverse('home'))

        else:
            messages.add_message(
                self.request, messages.ERROR, 'Usuario no válido o contraseña no válida')
            return super(LoginView, self).form_invalid(form)

    
class RegisterView(CreateView):
    template_name = "general/register.html"
    model = User
    success_url = reverse_lazy('login')
    form_class = RegistationForm
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Usuario creado correctamente")
        return super(RegisterView, self).form_valid(form)


class LegalView(TemplateView):
    template_name = "general/legal.html"
    

class ContactView(TemplateView):
    template_name = "general/contact.html"

@method_decorator(login_required, name='dispatch')
class ProfileDetailView(DetailView, FormView):
    template_name = "general/profile_detail.html"   
    model = UserProfile
    context_object_name= "profile"
    form_class = FollowForm
    
    def get_initial(self):
        self.initial['profile_pk'] = self.get_object().pk
        return super().get_initial()
    
    def form_valid(self, form):
        profile_pk = form.cleaned_data.get('profile_pk')
        action = form.cleaned_data.get('action')
        following = UserProfile.objects.get(pk=profile_pk)

        
        if action == 'follow':
            Follow.objects.get_or_create(
                follower=self.request.user.profile, 
                following=following
            )
            messages.add_message(self.request, messages.SUCCESS, f'Has seguido a este usuario')
        elif action == 'unfollow':
            Follow.objects.filter(
                follower=self.request.user.profile, 
                following=following
            ).delete()
            messages.add_message(self.request, messages.SUCCESS, f'Has dejado de seguir a este usuario {following.user.username}')
            
        return super(ProfileDetailView, self).form_valid(form)
        
    def get_success_url(self):
        return reverse('profile_detail', args=[self.request.user.profile.pk])
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
       
        
        following= Follow.objects.filter(follower=self.request.user.profile, following=self.get_object()).exists()
        context['following'] = following
        return context
    
@method_decorator(login_required, name='dispatch')
class ProfileListView(ListView):
    template_name = "general/profile_list.html"   
    model = UserProfile
    context_object_name= "profiles"
    
    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user) 
    
@method_decorator(login_required, name='dispatch') 
class ProfileUpdateView(UpdateView):
    template_name = "general/profile_update.html"   
    model = UserProfile
    context_object_name= "profile"
    fields = [
        "bio",
        "profile_picture",  
        "birth_date",
    ]
    
    
    def dispatch(self, request, *args, **kwargs):
        user_profile = self.get_object()
        if user_profile.user != request.user:
            return HttpResponseRedirect(reverse('home'))
        return super(ProfileUpdateView, self).dispatch(request, *args, **kwargs)
    
    
    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, "Perfil actualizado correctamente")
        return super(ProfileUpdateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('profile_detail', kwargs={'pk': self.object.pk})
    
@method_decorator(login_required, name='dispatch')   
def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, "Se ha cerrado sesión correctamente.")
    return HttpResponseRedirect(reverse('home'))


