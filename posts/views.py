from django.views.generic.edit import CreateView
from django import forms
from posts.models import Post
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
# Create your views here.
from .forms import PostCreateForm
from django.http import HttpResponseRedirect
from django.urls import reverse

@method_decorator(login_required, name='dispatch')
class PostCreateView(CreateView):
    template_name = 'posts/post_create.html'
    model = Post
    form_class = PostCreateForm
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user 
        messages.add_message(self.request, messages.SUCCESS, "Post creado correctamente")
        return super(PostCreateView, self).form_valid(form)

@method_decorator(login_required, name='dispatch')
class PostDetailView(DetailView):
    template_name = "posts/post_detail.html"
    model = Post
    context_object_name = 'post'
    
@login_required
def like_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.user in post.likes.all():
        messages.add_message(request, messages.INFO, "Ya no me gusta esta publicacion.")
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        messages.add_message(request, messages.INFO, "Me gusta esta publicacion.")

    return HttpResponseRedirect(reverse('post_detail', args=[pk]))
