"""
Script para guardar los resultados del entrenamiento como datos estáticos
Ejecuta este script después de entrenar el modelo localmente
"""
import json
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from api.models import FeatureImportance, ModelMetrics, MalwareAnalysis

def save_static_data():
    """Guardar datos estáticos en JSON"""
    
    print("📊 Guardando resultados del entrenamiento como datos estáticos...")
    
    # Crear directorio para datos estáticos
    static_data_dir = 'api/static_data'
    os.makedirs(static_data_dir, exist_ok=True)
    
    # 1. Guardar características importantes
    print("💾 Guardando características importantes...")
    features = list(FeatureImportance.objects.all().order_by('rank').values(
        'feature_name', 'importance_score', 'rank'
    ))
    
    with open(f'{static_data_dir}/feature_importances.json', 'w') as f:
        json.dump(features, f, indent=2)
    
    print(f"✅ Guardadas {len(features)} características")
    
    # 2. Guardar métricas del modelo
    print("💾 Guardando métricas...")
    metrics = list(ModelMetrics.objects.all().values(
        'model_type', 'metric_name', 'metric_value', 'with_scaler'
    ))
    
    with open(f'{static_data_dir}/model_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"✅ Guardadas {len(metrics)} métricas")
    
    # 3. Guardar análisis recientes (ejemplos)
    print("💾 Guardando análisis recientes...")
    analyses = list(MalwareAnalysis.objects.all()[:20].values(
        'malware_type', 'confidence', 'f1_score', 'created_at'
    ))
    
    # Convertir datetime a string
    for analysis in analyses:
        if analysis['created_at']:
            analysis['created_at'] = analysis['created_at'].isoformat()
    
    with open(f'{static_data_dir}/recent_analyses.json', 'w') as f:
        json.dump(analyses, f, indent=2, default=str)
    
    print(f"✅ Guardados {len(analyses)} análisis")
    
    # 4. Guardar resumen general
    print("💾 Guardando resumen general...")
    summary = {
        'model_info': {
            'name': 'Random Forest Classifier',
            'n_estimators': 50,
            'random_state': 42,
            'features_total': 79,
            'features_selected': 10
        },
        'dataset_info': {
            'total_apps': 1900,
            'benign': 1500,
            'adware': 250,
            'malware': 150
        },
        'training_results': {
            'f1_score': 0.9292,
            'precision': 0.9292,
            'recall': 0.9305
        }
    }
    
    with open(f'{static_data_dir}/summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    
    print("✅ Guardado resumen general")
    
    print("\n" + "="*70)
    print("✅ Todos los resultados guardados en api/static_data/")
    print("="*70)
    print("\nArchivos creados:")
    print(f"  - {static_data_dir}/feature_importances.json")
    print(f"  - {static_data_dir}/model_metrics.json")
    print(f"  - {static_data_dir}/recent_analyses.json")
    print(f"  - {static_data_dir}/summary.json")
    print("\nAhora puedes subir el proyecto a GitHub sin los archivos grandes.")

if __name__ == '__main__':
    save_static_data()
