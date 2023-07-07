from django.db import models

# Create your models here.
class TodoList(models.Model):
  title = models.CharField(max_length=35)
  is_done = models.BooleanField(default=False)
  creted_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return str(self.title)
