from django.urls import path
from . import views 

urlpatterns = [
   
    path('home/', views.Home.as_view(), name='home'),

    path('opportunities/', views.OpportunityList.as_view(), name='opportunity_list'),
    path('opportunities/<int:opportunity_id>/', views.OpportunityDetail.as_view(), name='opportunity_detail'),
    path('opportunities/<int:opportunity_id>/applications/', views.OpportunityApplicationList.as_view(), name='opportunity_applications'),


    path('skills/', views.SkillList.as_view(), name='skill-list'),
    path('opportunities/<int:opportunity_id>/associate-skill/<int:skill_id>/', views.AssociateSkillToOpp.as_view(), name='associate-skill'),
    path('opportunities/<int:opportunity_id>/desociate-skill/<int:skill_id>/', views.DesociateSkillFromOpp.as_view(), name='desociate-skill'),
]
