from django.urls import path
from . import views 

urlpatterns = [
   
    path('home/', views.Home.as_view(), name='home'),

    path('opportunities/', views.OpportunityList.as_view(), name='opportunity_list'),
    path('opportunities/<int:opportunity_id>/', views.OpportunityDetail.as_view(), name='opportunity_detail'),
]