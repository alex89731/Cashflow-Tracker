from django.urls import path
from . import views

urlpatterns = [
    path('', views.cashflow_list, name='cashflow_list'),
    path('new/', views.cashflow_create, name='cashflow_create'),
    path('<int:pk>/edit/', views.cashflow_update, name='cashflow_update'),
    path('<int:pk>/delete/', views.cashflow_delete, name='cashflow_delete'),
    
    # API endpoints
    path('api/categories/', views.CategoryAPIView.as_view(), name='category-api'),
    path('api/subcategories/', views.SubcategoryAPIView.as_view(), name='subcategory-api'),
]
