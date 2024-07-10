from django.urls import path
from .views import (
    StatusView,
    KeywordView,
    PresentationView,
    CoAuthorView,
    AbstractView,
    AbstractDetailsView,
    AbstractStatusView,
    AbstractReviewerView,
    AbstractReviewView,
    ClinicalCaseView,
    ProgrammaticEvaluationView,
    ClinicalCaseDetailsView,
    ProgrammaticEvaluationDetailsView,
    ClinicalCaseStatusView,
    ClinicalCaseReviewView,
    ProgrammaticEvaluationStatusView,
    ProgrammaticEvaluationReviewView,
    AbstractReviewerRelocateView
)


urlpatterns = [
    path('', AbstractView.as_view()),
    path('clinical/', ClinicalCaseView.as_view()),
    path('programmatic/', ProgrammaticEvaluationView.as_view()),
    path('<int:pk>/', AbstractDetailsView.as_view()),
    path('clinical/<int:pk>/', ClinicalCaseDetailsView.as_view()),
    path('programmatic/<int:pk>/', ProgrammaticEvaluationDetailsView.as_view()),
    path('<int:pk>/status/', AbstractStatusView.as_view()),
    path('clinical/<int:pk>/status/', ClinicalCaseStatusView.as_view()),
    path('programmatic/<int:pk>/status/', ProgrammaticEvaluationStatusView.as_view()),
    path('<int:pk>/review/', AbstractReviewerView.as_view()),
    path('<int:pk>/review/realocate/', AbstractReviewerRelocateView.as_view()),
    path('clinical/<int:pk>/review/', ClinicalCaseReviewView.as_view()),
    path('programmatic/<int:pk>/review/', ProgrammaticEvaluationReviewView.as_view()),
    path('review/', AbstractReviewView.as_view()),
    path('status/', StatusView.as_view()),
    path('keyword/', KeywordView.as_view()),
    path('presentation/', PresentationView.as_view()),
    path('coauthor/', CoAuthorView.as_view()),
    # path('resume/', views.ResumeView.as_view()),
]
