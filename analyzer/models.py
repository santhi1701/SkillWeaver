
from django.db import models
from django.contrib.auth.models import User

# Model for uploaded resumes
class Resume(models.Model):
    ROLE_CHOICES = [
        ('Data Analyst', 'Data Analyst'),
        ('Data Scientist', 'Data Scientist'),
        ('Web Developer', 'Web Developer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resume_file = models.FileField(upload_to='resumes/')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    match_score = models.FloatField(default=0)  # Store AI match score
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"