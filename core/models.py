from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        ordering = ['completed', '-created_at']

    def __str__(self):
        return self.title
