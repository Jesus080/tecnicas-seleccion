"""
Script de gestión para entrenar el modelo
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from ml_model.model import ml_model
from api.models import FeatureImportance, ModelMetrics
from django.conf import settings


def train_and_save_model():
    """
    Entrenar el modelo y guardar los resultados en la base de datos
    """
    print("=" * 80)
    print("INICIANDO ENTRENAMIENTO DEL MODELO")
    print("=" * 80)
    
    # Verificar que existe el archivo CSV
    csv_path = settings.DATA_DIR / 'TotalFeatures-ISCXFlowMeter.csv'
    if not csv_path.exists():
        print(f"ERROR: No se encuentra el archivo {csv_path}")
        print("Por favor, copia el archivo TotalFeatures-ISCXFlowMeter.csv a la carpeta 'data'")
        return
    
    # Entrenar modelo
    result = ml_model.train_model(csv_path=csv_path)
    
    print("\n" + "=" * 80)
    print("GUARDANDO RESULTADOS EN LA BASE DE DATOS")
    print("=" * 80)
    
    # Limpiar datos antiguos
    FeatureImportance.objects.all().delete()
    ModelMetrics.objects.filter(model_type='random_forest_classification').delete()
    
    # Guardar importancia de características
    for rank, (feature_name, importance) in enumerate(
        result['feature_importances'].items(), start=1
    ):
        FeatureImportance.objects.create(
            feature_name=feature_name,
            importance_score=importance,
            rank=rank
        )
    
    print(f"✓ Guardadas {len(result['feature_importances'])} características")
    
    # Guardar métricas
    ModelMetrics.objects.create(
        model_type='random_forest_classification',
        metric_name='F1_Score',
        metric_value=result['f1_score'],
        with_scaler=False
    )
    ModelMetrics.objects.create(
        model_type='random_forest_classification',
        metric_name='Precision',
        metric_value=result['precision'],
        with_scaler=False
    )
    ModelMetrics.objects.create(
        model_type='random_forest_classification',
        metric_name='Recall',
        metric_value=result['recall'],
        with_scaler=False
    )
    
    print("✓ Guardadas las métricas del modelo")
    
    print("\n" + "=" * 80)
    print("RESUMEN DEL ENTRENAMIENTO")
    print("=" * 80)
    print(f"F1-Score:  {result['f1_score']:.4f}")
    print(f"Precision: {result['precision']:.4f}")
    print(f"Recall:    {result['recall']:.4f}")
    print(f"\nTop 10 características más importantes:")
    for i, feature in enumerate(result['top_features'], 1):
        importance = result['feature_importances'][feature]
        print(f"  {i:2d}. {feature:40s} {importance:.6f}")
    
    print("\n" + "=" * 80)
    print("✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
    print("=" * 80)


if __name__ == '__main__':
    train_and_save_model()
