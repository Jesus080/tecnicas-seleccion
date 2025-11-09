from rest_framework import serializers
from .models import MalwareAnalysis, FeatureImportance, ModelMetrics


class MalwareAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = MalwareAnalysis
        fields = ['id', 'created_at', 'malware_type', 'confidence', 'f1_score']
        read_only_fields = ['id', 'created_at']


class FeatureImportanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeatureImportance
        fields = ['id', 'feature_name', 'importance_score', 'rank']
        read_only_fields = ['id']


class ModelMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelMetrics
        fields = ['id', 'model_type', 'metric_name', 'metric_value', 'with_scaler', 'created_at']
        read_only_fields = ['id', 'created_at']


class PredictionInputSerializer(serializers.Serializer):
    """
    Serializer para recibir datos de entrada para predicción
    """
    features = serializers.DictField(
        child=serializers.FloatField(),
        help_text="Diccionario con las características de la aplicación"
    )


class PredictionOutputSerializer(serializers.Serializer):
    """
    Serializer para devolver resultados de predicción
    """
    prediction = serializers.CharField(help_text="Tipo de malware predicho")
    confidence = serializers.FloatField(help_text="Confianza de la predicción")
    probabilities = serializers.DictField(help_text="Probabilidades para cada clase")
    timestamp = serializers.DateTimeField(help_text="Timestamp de la predicción")
