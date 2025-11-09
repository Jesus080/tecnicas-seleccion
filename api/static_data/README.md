# Datos Estáticos del Entrenamiento

Este directorio contiene los resultados del entrenamiento del modelo guardados como JSON.

## Archivos

### `feature_importances.json`
Importancia de cada característica en el modelo Random Forest.

```json
[
  {
    "feature_name": "Init_Win_bytes_forward",
    "importance_score": 0.144417,
    "rank": 1
  },
  ...
]
```

### `model_metrics.json`
Métricas del rendimiento del modelo.

```json
[
  {
    "model_type": "random_forest_classification",
    "metric_name": "F1_Score",
    "metric_value": 0.9292,
    "with_scaler": false
  },
  ...
]
```

### `recent_analyses.json`
Análisis recientes de malware (ejemplos).

```json
[
  {
    "malware_type": "benign",
    "confidence": 0.95,
    "f1_score": 0.93,
    "created_at": "2024-11-09T..."
  },
  ...
]
```

### `summary.json`
Resumen general del modelo y dataset.

```json
{
  "model_info": {
    "name": "Random Forest Classifier",
    "n_estimators": 50,
    ...
  },
  "dataset_info": {
    "total_apps": 1900,
    ...
  },
  "training_results": {
    "f1_score": 0.9292,
    ...
  }
}
```

## Actualizar Datos

Para actualizar estos archivos después de un nuevo entrenamiento:

```bash
python save_training_results.py
```

## Uso en la Aplicación

La aplicación carga automáticamente estos datos cuando:
- El modelo `.pkl` no está disponible
- La base de datos no tiene datos
- Se ejecuta en un entorno sin el dataset completo

Esto permite que la aplicación funcione en GitHub/Render sin necesidad de subir archivos grandes.
