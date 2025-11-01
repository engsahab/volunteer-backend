from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.



class Skill(models.Model):
    name = models.CharField(max_length=100)


class VolunteerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    skills = models.ManyToManyField(Skill, blank=True) 
    city = models.CharField(max_length=100, blank=True, null=True)
    specialization = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username


class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=200)
    skills = models.ManyToManyField(Skill, blank=True)

    def __str__(self):
        return self.title

      

class Application(models.Model):
   
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    profile = models.ForeignKey(VolunteerProfile, on_delete=models.CASCADE, related_name='applications', null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True) 

   
    def __str__(self):
        
        if self.profile and self.profile.user:
            return f"Application by {self.profile.user.username} for {self.opportunity.title}"
        else:
            return f"Application (No Profile) for {self.opportunity.title}"
        
    class Meta:
            
        ordering = ['-applied_at']