from rest_framework import serializers
from .models import Opportunity,Application,Skill,VolunteerProfile



class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class VolunteerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerProfile
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    profile = VolunteerProfileSerializer(read_only=True)
    class Meta:
       model = Application
       fields = ['id', 'opportunity', 'status', 'applied_at', 'profile']
       

class OpportunitySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    applications = ApplicationSerializer(many=True, read_only=True)


    class Meta:
        model = Opportunity
        fields = ['id', 'title', 'description', 'date', 'location', 'skills', 'applications']

