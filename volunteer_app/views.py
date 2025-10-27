from rest_framework.views import APIView
from rest_framework.response import Response

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