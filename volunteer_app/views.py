from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import Opportunity,Application,Skill
from .serializers import OpportunitySerializer,ApplicationSerializer,SkillSerializer
# Create your views here.

class Home(APIView):
    def get(self, request):
        content = {'message': 'Welcome to the Volunteer Management API!'}
        return Response(content)

    def post(self, request):
        print("POST data received:", request.data) 
        
        content = {
            'message': 'POST request successful!',
            'data_received': request.data 
        }
        return Response(content)
    


class OpportunityList(APIView):
    def get(self, request):
        queryset = Opportunity.objects.all()
        serializer = OpportunitySerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            serializer = OpportunitySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class OpportunityDetail(APIView):
    def get(self, request, opportunity_id):
        try:
            queryset = get_object_or_404(Opportunity, id=opportunity_id)
            serializer = OpportunitySerializer(queryset)
            return Response(serializer.data)

        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def put(self, request, opportunity_id):
        try:
            queryset = get_object_or_404(Opportunity, id=opportunity_id)
            serializer = OpportunitySerializer(queryset, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def delete(self, request, opportunity_id):
        try:
            queryset = get_object_or_404(Opportunity, id=opportunity_id)
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

class OpportunityApplicationList(APIView):
       def  get(self, request, opportunity_id):
       
            queryset = Application.objects.filter(opportunity_id=opportunity_id)
            serializer = ApplicationSerializer(queryset, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)  
       

      
class SkillList(APIView):
       def post(self, request):
        serializer = SkillSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AssociateSkillToOpp(APIView):
       def patch(self, request, opportunity_id, skill_id):
        opportunity = get_object_or_404(Opportunity, id=opportunity_id)
        skill = get_object_or_404(Skill, id=skill_id)
        opportunity.skills.add(skill)
        return Response({"message": f"Skill {skill.name} added to {opportunity.title}"}, status=status.HTTP_200_OK)


class DesociateSkillFromOpp(APIView):
    def post(self, request, opportunity_id, skill_id): 
        opportunity = get_object_or_404(Opportunity, id=opportunity_id)
        skill = get_object_or_404(Skill, id=skill_id)
        opportunity.skills.remove(skill)
        return Response({"message": f"Skill {skill.name} removed from {opportunity.title}"}, status=status.HTTP_200_OK)