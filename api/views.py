from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import MalwareAnalysis, FeatureImportance, ModelMetrics
from .serializers import (
    MalwareAnalysisSerializer, 
    FeatureImportanceSerializer,
    ModelMetricsSerializer,
    PredictionInputSerializer,
    PredictionOutputSerializer
)
import json
import os
from pathlib import Path

# Intentar cargar el modelo ML, pero no fallar si no existe
try:
    from ml_model.model import ml_model
    ML_MODEL_AVAILABLE = True
except:
    ML_MODEL_AVAILABLE = False
    ml_model = None


# ViewSets para la API REST
class MalwareAnalysisViewSet(viewsets.ModelViewSet):
    """
    ViewSet para análisis de malware
    """
    queryset = MalwareAnalysis.objects.all()
    serializer_class = MalwareAnalysisSerializer


class FeatureImportanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para importancia de características
    """
    queryset = FeatureImportance.objects.all()
    serializer_class = FeatureImportanceSerializer


class ModelMetricsViewSet(viewsets.ModelViewSet):
    """
    ViewSet para métricas del modelo
    """
    queryset = ModelMetrics.objects.all()
    serializer_class = ModelMetricsSerializer


# Vista para predicción
class PredictMalwareView(APIView):
    """
    Vista para realizar predicciones de malware
    """
    
    def post(self, request):
        """
        Realizar predicción con características proporcionadas
        """
        serializer = PredictionInputSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            features = serializer.validated_data['features']
            
            # Realizar predicción
            result = ml_model.predict(features)
            
            # Agregar timestamp
            result['timestamp'] = timezone.now()
            
            # Guardar en base de datos
            analysis = MalwareAnalysis.objects.create(
                malware_type=result['prediction'],
                confidence=result['confidence']
            )
            
            output_serializer = PredictionOutputSerializer(result)
            
            return Response(
                output_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@api_view(['GET'])
def get_feature_importances(request):
    """
    Obtener importancia de características del modelo (datos estáticos)
    """
    try:
        # Cargar desde archivos estáticos
        features = load_static_data('feature_importances.json')
        
        # Convertir a diccionario
        importances = {f['feature_name']: f['importance_score'] for f in features}
        sorted_importances = dict(
            sorted(importances.items(), key=lambda x: x[1], reverse=True)
        )
        
        return Response({
            'feature_importances': sorted_importances,
            'top_10': dict(list(sorted_importances.items())[:10])
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def train_model_view(request):
    """
    Vista para entrenar el modelo (solo para desarrollo)
    """
    try:
        result = ml_model.train_model()
        
        # Guardar importancia de características
        for rank, (feature_name, importance) in enumerate(
            result['feature_importances'].items(), start=1
        ):
            FeatureImportance.objects.update_or_create(
                feature_name=feature_name,
                defaults={
                    'importance_score': importance,
                    'rank': rank
                }
            )
        
        # Guardar métricas
        ModelMetrics.objects.create(
            model_type='random_forest_classification',
            metric_name='F1-Score',
            metric_value=result['f1_score']
        )
        ModelMetrics.objects.create(
            model_type='random_forest_classification',
            metric_name='Precision',
            metric_value=result['precision']
        )
        ModelMetrics.objects.create(
            model_type='random_forest_classification',
            metric_name='Recall',
            metric_value=result['recall']
        )
        
        return Response({
            'status': 'success',
            'message': 'Modelo entrenado exitosamente',
            'metrics': {
                'f1_score': result['f1_score'],
                'precision': result['precision'],
                'recall': result['recall']
            },
            'top_features': result['top_features']
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_model_stats(request):
    """
    Obtener estadísticas del modelo (usando datos estáticos si es necesario)
    """
    try:
        # Intentar obtener desde BD
        try:
            metrics = ModelMetrics.objects.filter(
                model_type='random_forest_classification'
            ).values('metric_name', 'metric_value', 'with_scaler')
            
            top_features = FeatureImportance.objects.all()[:10]
            features_serializer = FeatureImportanceSerializer(top_features, many=True)
            
            recent_analyses = MalwareAnalysis.objects.all()[:20]
            analyses_serializer = MalwareAnalysisSerializer(recent_analyses, many=True)
            
            return Response({
                'metrics': list(metrics),
                'top_features': features_serializer.data,
                'recent_analyses': analyses_serializer.data
            })
        except:
            # Usar datos estáticos si la BD falla
            metrics = load_static_data('model_metrics.json')
            top_features = load_static_data('feature_importances.json')[:10]
            recent_analyses = load_static_data('recent_analyses.json')[:20]
            
            return Response({
                'metrics': metrics,
                'top_features': top_features,
                'recent_analyses': recent_analyses
            })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# Función para cargar datos estáticos
def load_static_data(filename):
    """Cargar datos desde archivos JSON estáticos"""
    static_data_path = Path(__file__).parent / 'static_data' / filename
    if static_data_path.exists():
        with open(static_data_path, 'r') as f:
            return json.load(f)
    return []


# Vistas para el frontend HTML
def index(request):
    """
    Vista principal de la página
    """
    return render(request, 'index.html')


def dashboard(request):
    """
    Vista del dashboard con resultados (usando datos estáticos)
    """
    # Intentar cargar desde base de datos, si no, usar archivos estáticos
    try:
        metrics = ModelMetrics.objects.filter(
            model_type='random_forest_classification'
        )
        top_features = FeatureImportance.objects.all()[:10]
        recent_analyses = MalwareAnalysis.objects.all()[:10]
    except:
        # Si la BD no está disponible, usar datos estáticos
        metrics = load_static_data('model_metrics.json')
        top_features = load_static_data('feature_importances.json')[:10]
        recent_analyses = load_static_data('recent_analyses.json')[:10]
    
    # Cargar resumen
    summary = load_static_data('summary.json')
    
    context = {
        'metrics': metrics,
        'top_features': top_features,
        'recent_analyses': recent_analyses,
        'summary': summary
    }
    
    return render(request, 'dashboard.html', context)
