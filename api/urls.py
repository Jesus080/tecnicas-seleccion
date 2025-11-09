from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para ViewSets
router = DefaultRouter()
router.register(r'analyses', views.MalwareAnalysisViewSet)
router.register(r'features', views.FeatureImportanceViewSet)
router.register(r'metrics', views.ModelMetricsViewSet)

urlpatterns = [
    # API endpoints
    path('', include(router.urls)),
    path('predict/', views.PredictMalwareView.as_view(), name='predict'),
    path('feature-importances/', views.get_feature_importances, name='feature-importances'),
    path('train/', views.train_model_view, name='train-model'),
    path('stats/', views.get_model_stats, name='model-stats'),
    
    # Frontend views
    path('home/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
