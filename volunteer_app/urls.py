from django.urls import path
from . import views 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
   
    path('home/', views.Home.as_view(), name='home'),

    path('opportunities/', views.OpportunityList.as_view(), name='opportunity_list'),
    path('opportunities/<int:opportunity_id>/', views.OpportunityDetail.as_view(), name='opportunity_detail'),
    path('opportunities/<int:opportunity_id>/applications/', views.OpportunityApplicationList.as_view(), name='opportunity_applications'),

    path('applications/<int:app_id>/', views.ApplicationDetail.as_view(), name='application-detail'),

    path('admin/applications/', views.AdminApplicationList.as_view(), name='admin-app-list'),
 
    path('profile/', views.GetUserProfileView.as_view(), name='get_profile'),
    path('admin/profile/<int:profile_id>/', views.AdminProfileDetail.as_view(), name='admin-profile-detail'),
    path('signup/', views.SignupUserView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
