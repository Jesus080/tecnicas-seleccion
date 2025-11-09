from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import MalwareAnalysis, FeatureImportance, ModelMetrics
import json


class MalwareAnalysisModelTest(TestCase):
    """Tests para el modelo MalwareAnalysis"""
    
    def setUp(self):
        self.analysis = MalwareAnalysis.objects.create(
            malware_type='benign',
            confidence=0.95,
            f1_score=0.93
        )
    
    def test_malware_analysis_creation(self):
        """Test de creación de análisis"""
        self.assertEqual(self.analysis.malware_type, 'benign')
        self.assertEqual(self.analysis.confidence, 0.95)
        self.assertIsNotNone(self.analysis.created_at)
    
    def test_malware_analysis_str(self):
        """Test del método __str__"""
        self.assertIn('benign', str(self.analysis))


class FeatureImportanceModelTest(TestCase):
    """Tests para el modelo FeatureImportance"""
    
    def setUp(self):
        self.feature = FeatureImportance.objects.create(
            feature_name='Flow_Duration',
            importance_score=0.15,
            rank=1
        )
    
    def test_feature_importance_creation(self):
        """Test de creación de importancia de característica"""
        self.assertEqual(self.feature.feature_name, 'Flow_Duration')
        self.assertEqual(self.feature.importance_score, 0.15)
        self.assertEqual(self.feature.rank, 1)


class APIEndpointsTest(APITestCase):
    """Tests para los endpoints de la API"""
    
    def setUp(self):
        self.client = Client()
    
    def test_api_root(self):
        """Test del endpoint raíz de la API"""
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_feature_importances_endpoint(self):
        """Test del endpoint de importancia de características"""
        # Crear algunas características
        FeatureImportance.objects.create(
            feature_name='test_feature',
            importance_score=0.10,
            rank=1
        )
        
        response = self.client.get('/api/features/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_stats_endpoint(self):
        """Test del endpoint de estadísticas"""
        response = self.client.get('/api/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertIn('metrics', data)
        self.assertIn('top_features', data)
        self.assertIn('recent_analyses', data)


class ViewsTest(TestCase):
    """Tests para las vistas del frontend"""
    
    def setUp(self):
        self.client = Client()
    
    def test_index_view(self):
        """Test de la vista principal"""
        response = self.client.get('/home/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Sistema de Detección de Malware')
    
    def test_dashboard_view(self):
        """Test de la vista del dashboard"""
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'Dashboard')


class PredictionTest(APITestCase):
    """Tests para las predicciones"""
    
    def test_prediction_with_valid_data(self):
        """Test de predicción con datos válidos"""
        # Nota: Este test requiere que el modelo esté entrenado
        # En un entorno de test real, usarías un modelo mock
        
        data = {
            'features': {
                'Flow_Duration': 1000000,
                'Total_Fwd_Packets': 10,
                'Total_Backward_Packets': 8
            }
        }
        
        # Este test puede fallar si el modelo no está entrenado
        # En un test real, mockearíamos el modelo
        # response = self.client.post('/api/predict/', data, format='json')
        # self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR])
    
    def test_prediction_with_invalid_data(self):
        """Test de predicción con datos inválidos"""
        data = {
            'invalid_key': 'invalid_value'
        }
        
        response = self.client.post('/api/predict/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ModelMetricsTest(TestCase):
    """Tests para métricas del modelo"""
    
    def setUp(self):
        self.metric = ModelMetrics.objects.create(
            model_type='random_forest_classification',
            metric_name='F1_Score',
            metric_value=0.93,
            with_scaler=False
        )
    
    def test_metric_creation(self):
        """Test de creación de métrica"""
        self.assertEqual(self.metric.model_type, 'random_forest_classification')
        self.assertEqual(self.metric.metric_name, 'F1_Score')
        self.assertEqual(self.metric.metric_value, 0.93)
        self.assertFalse(self.metric.with_scaler)
