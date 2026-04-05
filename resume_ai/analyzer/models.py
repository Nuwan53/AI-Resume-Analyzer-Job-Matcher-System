from django.db import models

# Create your models here.
class Resume(models.Model):
    file = models.FileField(upload_to = 'resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class ExtarctedData(models.Model):
    resume = models.OneToOneField(Resume, on_delete=models.CASCADE)
    skills = models.TextField()
    experience = models.TextField()
    education = models.TextField()

class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    required_skills = models.TextField()

class MatchResult(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    score = models.FloatField()
    