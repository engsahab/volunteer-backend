from rest_framework import serializers
from .models import Opportunity,Application,Skill,VolunteerProfile,User

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff']


class VolunteerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = VolunteerProfile
        fields = ['id', 'user', 'skills', 'city', 'specialization']

class ApplicationSerializer(serializers.ModelSerializer):
    profile = VolunteerProfileSerializer(read_only=True) 
    opportunity = serializers.StringRelatedField() 

    class Meta:
       model = Application
       fields = ['id', 'opportunity', 'status', 'applied_at', 'profile']
       read_only_fields = ['opportunity', 'profile']

class OpportunitySerializer(serializers.ModelSerializer):
    applications = ApplicationSerializer(many=True, read_only=True) 

    class Meta:
        model = Opportunity
        fields = ['id', 'title', 'description', 'date', 'location','skills_list', 'applications', 'specialization']


