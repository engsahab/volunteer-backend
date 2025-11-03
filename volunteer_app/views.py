from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from .models import Opportunity,Application,VolunteerProfile
from .serializers import OpportunitySerializer,ApplicationSerializer,VolunteerProfileSerializer
# Create your views here.


User = get_user_model()

class Home(APIView):

    permission_classes = [AllowAny] 
    
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
   permission_classes = [IsAuthenticatedOrReadOnly]
   def get(self, request):
        queryset = Opportunity.objects.all()
        serializer = OpportunitySerializer(queryset, many=True)
        return Response(serializer.data)

   def post(self, request):

        if not request.user.is_staff: 
            return Response({"error": "Only admins can create opportunities."}, status=status.HTTP_403_FORBIDDEN)
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

    permission_classes = [IsAuthenticatedOrReadOnly]
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

        if not request.user.is_staff:
            return Response({"error": "Only admins can edit opportunities."}, status=status.HTTP_403_FORBIDDEN)
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
       
        if not request.user.is_staff:
            return Response({"error": "Only admins can delete opportunities."}, status=status.HTTP_403_FORBIDDEN)
        try:
            queryset = get_object_or_404(Opportunity, id=opportunity_id)
            queryset.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Exception as error:
            return Response(
                {"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        


class OpportunityApplicationList(APIView):

       permission_classes = [IsAuthenticatedOrReadOnly]

       def  get(self, request, opportunity_id):
            queryset = Application.objects.filter(opportunity_id=opportunity_id)
            serializer = ApplicationSerializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)  
       
       def post(self, request, opportunity_id):

            try:

                profile = request.user.profile 
                if Application.objects.filter(profile=profile, opportunity_id=opportunity_id).exists():

                    return Response(
                        {"error": "You have already applied for this opportunity."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                serializer = ApplicationSerializer(data=request.data)
                
                if serializer.is_valid():

                    serializer.save(profile=profile, opportunity_id=opportunity_id) 
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except Exception as error:
                return Response(
                    {"error": "An error occurred submitting the application."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            


class ApplicationDetail(APIView):
   
    permission_classes = [IsAuthenticated]
    def get(self, request, app_id):
        
        application = get_object_or_404(Application, id=app_id)
        
       
        if not (request.user.profile == application.profile or request.user.is_staff):
            return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
            
        serializer = ApplicationSerializer(application)
        return Response(serializer.data)


    def put(self, request, app_id):
         
        if not request.user.is_staff:
            return Response({"error": "Only admins can change status."}, status=status.HTTP_403_FORBIDDEN)
            
        application = get_object_or_404(Application, id=app_id)
        
       
        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, app_id):
       
        application = get_object_or_404(Application, id=app_id)
        
        
        if not request.user.profile == application.profile:
             return Response({"error": "You can only delete your own applications."}, status=status.HTTP_403_FORBIDDEN)
        
        application.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class AdminApplicationList(APIView):
    
    permission_classes = [IsAdminUser] 

    def get(self, request):
       
        applications = Application.objects.all().order_by('-applied_at')
        
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
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


class GetUserProfileView(APIView):

    permission_classes = [IsAuthenticated] 

    def get(self, request):

        user = request.user
        try:
            profile = VolunteerProfile.objects.get(user=user)
        except VolunteerProfile.DoesNotExist:
            profile = VolunteerProfile.objects.create(user=user)
       
        serializer = VolunteerProfileSerializer(profile)

        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def put(self, request):
       
        try:
            profile = get_object_or_404(VolunteerProfile, user=request.user)
            serializer = VolunteerProfileSerializer(profile, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as error:
             return Response({"error": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
   
class AdminProfileDetail(APIView):
    
    permission_classes = [IsAdminUser] 

    def get(self, request, profile_id):

        try:

            profile = get_object_or_404(VolunteerProfile, id=profile_id)
            

            serializer = VolunteerProfileSerializer(profile)

            return Response(serializer.data, status=status.HTTP_200_OK)
            
        except Exception as error:
             return Response(
                {"error": "Profile not found or access denied."}, 
                status=status.HTTP_404_NOT_FOUND
            )