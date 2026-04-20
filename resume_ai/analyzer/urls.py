from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('resumes/', views.resume_list, name='resume_list'),
    path('resume/<int:pk>/', views.resume_detail, name='resume_detail'),
    path('resume/<int:pk>/edit/', views.edit_extracted_data, name='edit_extracted_data'),
    path('resume/<int:pk>/generate-matches/', views.generate_matches, name='generate_matches'),
    path('resume/<int:pk>/matches/', views.match_results, name='match_results'),
    path('resume/<int:pk>/recommendations/', views.job_recommendations, name='job_recommendations'),
    path('jobs/', views.job_list, name='job_list'),
]
