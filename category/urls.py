from django.urls import path
from .views import CategoryView, SubCategoryView, CategoryDetailView, SubCategorySpecView, SubCategoryDetailView


urlpatterns = [
    path('', CategoryView.as_view()),
    path('<int:pk>/', CategoryDetailView.as_view()),
    path('<int:pk>/subcategory/', SubCategorySpecView.as_view()),
    path('subcategory/', SubCategoryView.as_view()),
    path('subcategory/<int:pk>/', SubCategoryDetailView.as_view())
]