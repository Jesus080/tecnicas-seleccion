from django.contrib import admin
from .models import MalwareAnalysis, FeatureImportance, ModelMetrics


@admin.register(MalwareAnalysis)
class MalwareAnalysisAdmin(admin.ModelAdmin):
    list_display = ['malware_type', 'confidence', 'f1_score', 'created_at']
    list_filter = ['malware_type', 'created_at']
    search_fields = ['malware_type']
    date_hierarchy = 'created_at'


@admin.register(FeatureImportance)
class FeatureImportanceAdmin(admin.ModelAdmin):
    list_display = ['rank', 'feature_name', 'importance_score']
    ordering = ['rank']
    search_fields = ['feature_name']


@admin.register(ModelMetrics)
class ModelMetricsAdmin(admin.ModelAdmin):
    list_display = ['model_type', 'metric_name', 'metric_value', 'with_scaler', 'created_at']
    list_filter = ['model_type', 'with_scaler', 'created_at']
    search_fields = ['metric_name']
