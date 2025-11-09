from django.db import models
from django.utils import timezone


class MalwareAnalysis(models.Model):
    """
    Modelo para almacenar resultados de análisis de malware
    """
    MALWARE_TYPES = [
        ('benign', 'Benigno'),
        ('adware', 'Adware'),
        ('malware', 'Malware General'),
    ]
    
    created_at = models.DateTimeField(default=timezone.now)
    malware_type = models.CharField(max_length=50, choices=MALWARE_TYPES)
    confidence = models.FloatField(help_text='Confianza de la predicción')
    f1_score = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Análisis de Malware'
        verbose_name_plural = 'Análisis de Malware'
    
    def __str__(self):
        return f"{self.malware_type} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class FeatureImportance(models.Model):
    """
    Modelo para almacenar la importancia de características
    """
    feature_name = models.CharField(max_length=200, unique=True)
    importance_score = models.FloatField()
    rank = models.IntegerField()
    
    class Meta:
        ordering = ['rank']
        verbose_name = 'Importancia de Característica'
        verbose_name_plural = 'Importancia de Características'
    
    def __str__(self):
        return f"{self.feature_name} - {self.importance_score:.4f}"


class ModelMetrics(models.Model):
    """
    Modelo para almacenar métricas del modelo
    """
    MODEL_TYPES = [
        ('decision_forest', 'Decision Forest'),
        ('random_forest_classification', 'Random Forest (Clasificación)'),
        ('random_forest_regression', 'Random Forest (Regresión)'),
    ]
    
    model_type = models.CharField(max_length=50, choices=MODEL_TYPES)
    metric_name = models.CharField(max_length=100)
    metric_value = models.FloatField()
    with_scaler = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['model_type', 'metric_name']
        verbose_name = 'Métrica del Modelo'
        verbose_name_plural = 'Métricas del Modelo'
    
    def __str__(self):
        return f"{self.model_type} - {self.metric_name}: {self.metric_value:.4f}"
