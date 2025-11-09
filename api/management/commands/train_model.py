"""
Comando de gestión para entrenar el modelo de Machine Learning
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from ml_model.model import ml_model
from api.models import FeatureImportance, ModelMetrics


class Command(BaseCommand):
    help = 'Entrena el modelo de Random Forest para detección de malware'

    def add_arguments(self, parser):
        parser.add_argument(
            '--csv-path',
            type=str,
            help='Ruta al archivo CSV con el dataset',
        )
        parser.add_argument(
            '--n-estimators',
            type=int,
            default=50,
            help='Número de árboles en el Random Forest',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 80))
        self.stdout.write(self.style.SUCCESS('INICIANDO ENTRENAMIENTO DEL MODELO'))
        self.stdout.write(self.style.SUCCESS('=' * 80))
        
        # Obtener ruta del CSV
        csv_path = options.get('csv_path')
        if csv_path is None:
            csv_path = settings.DATA_DIR / 'TotalFeatures-ISCXFlowMeter.csv'
        
        # Verificar que existe
        if not csv_path.exists():
            self.stdout.write(
                self.style.ERROR(f'ERROR: No se encuentra el archivo {csv_path}')
            )
            self.stdout.write(
                self.style.WARNING('Por favor, copia el archivo a la carpeta data/')
            )
            return
        
        try:
            # Entrenar modelo
            n_estimators = options.get('n_estimators', 50)
            result = ml_model.train_model(
                csv_path=csv_path,
                n_estimators=n_estimators
            )
            
            # Limpiar datos antiguos
            self.stdout.write('Limpiando datos antiguos...')
            FeatureImportance.objects.all().delete()
            ModelMetrics.objects.filter(
                model_type='random_forest_classification'
            ).delete()
            
            # Guardar importancia de características
            self.stdout.write('Guardando importancia de características...')
            for rank, (feature_name, importance) in enumerate(
                result['feature_importances'].items(), start=1
            ):
                FeatureImportance.objects.create(
                    feature_name=feature_name,
                    importance_score=importance,
                    rank=rank
                )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Guardadas {len(result["feature_importances"])} características'
                )
            )
            
            # Guardar métricas
            self.stdout.write('Guardando métricas...')
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
            
            self.stdout.write(self.style.SUCCESS('✓ Métricas guardadas'))
            
            # Mostrar resumen
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 80))
            self.stdout.write(self.style.SUCCESS('RESUMEN DEL ENTRENAMIENTO'))
            self.stdout.write(self.style.SUCCESS('=' * 80))
            self.stdout.write(f'F1-Score:  {result["f1_score"]:.4f}')
            self.stdout.write(f'Precision: {result["precision"]:.4f}')
            self.stdout.write(f'Recall:    {result["recall"]:.4f}')
            self.stdout.write('')
            self.stdout.write('Top 10 características más importantes:')
            for i, feature in enumerate(result['top_features'], 1):
                importance = result['feature_importances'][feature]
                self.stdout.write(f'  {i:2d}. {feature:40s} {importance:.6f}')
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('=' * 80))
            self.stdout.write(self.style.SUCCESS('✅ ENTRENAMIENTO COMPLETADO EXITOSAMENTE'))
            self.stdout.write(self.style.SUCCESS('=' * 80))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error durante el entrenamiento: {str(e)}')
            )
            raise
