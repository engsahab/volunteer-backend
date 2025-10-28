from rest_framework import serializers
from .models import Opportunity,Application,Skill



class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class OpportunitySerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Opportunity
        fields = ['id', 'title', 'description', 'date', 'location', 'skills']
        
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'