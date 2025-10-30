from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import Opportunity,Application,Skill,VolunteerProfile
from .serializers import OpportunitySerializer,ApplicationSerializer,SkillSerializer,VolunteerProfileSerializer
# Create your views here.


User = get_user_model()

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
            skills_opportunity_has = queryset.skills.all() 
            skills_opportunity_does_not_have = Skill.objects.exclude(
                id__in=skills_opportunity_has.values_list('id')
            )
            data = serializer.data
            data['skills_opportunity_has'] = SkillSerializer(skills_opportunity_has, many=True).data
            data['skills_opportunity_does_not_have'] = SkillSerializer(skills_opportunity_does_not_have, many=True).data
            return Response(data)

        
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
   
class SignupUserView(APIView):
    permission_classes = [AllowAny] 

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password or not email:
            return Response(
                {"error": "Please provide a username, password, and email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': "User Already Exisits"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username, email=email, password=password
        )

    
        VolunteerProfile.objects.create(user=user)
       
        return Response(
            {"id": user.id, "username": user.username, "email": user.email},
            status=status.HTTP_201_CREATED,
        )