from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name='Usuario')
    image=models.ImageField(upload_to='posts/_images', verbose_name='Imagen')
    caption = models.TextField(max_length=500, blank=True, verbose_name='Descripción')                                                                                                                                                                    
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    likes = models.ManyToManyField(User, related_name='liked_posts', verbose_name='N me gusta', blank=True)
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
    
    
class Comment(models.Model):
    post =models.ForeignKey(Post,on_delete=models.CASCADE, related_name='coments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coments')
    text = models.TimeField(max_length=300)
    created_at =models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Comentario'
        verbose_name_plural = 'Comentarios'
        
    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"