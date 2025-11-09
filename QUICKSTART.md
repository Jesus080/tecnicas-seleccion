# Guía Rápida de Inicio

## Instalación Rápida (Linux/Mac)

```bash
# 1. Ejecutar script de setup
chmod +x setup.sh
./setup.sh

# 2. Copiar el dataset
cp ../TotalFeatures-ISCXFlowMeter.csv data/

# 3. Entrenar el modelo
python train_model.py

# 4. Ejecutar servidor
python manage.py runserver
```

## Instalación Rápida (Windows)

```powershell
# 1. Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Copiar el dataset
copy ..\TotalFeatures-ISCXFlowMeter.csv data\

# 4. Aplicar migraciones
python manage.py migrate

# 5. Recolectar estáticos
python manage.py collectstatic --noinput

# 6. Entrenar modelo
python train_model.py

# 7. Ejecutar servidor
python manage.py runserver
```

## Comandos Útiles

### Desarrollo

```bash
# Ejecutar tests
python manage.py test

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell
```

### Deployment

```bash
# Recolectar archivos estáticos
python manage.py collectstatic --noinput

# Ejecutar con Gunicorn
gunicorn core.wsgi:application

# Verificar configuración
python manage.py check --deploy
```

## Endpoints Disponibles

### Frontend
- `/home/` - Página principal
- `/dashboard/` - Dashboard con resultados
- `/admin/` - Panel de administración

### API
- `GET /api/` - Root de la API
- `POST /api/predict/` - Realizar predicción
- `GET /api/feature-importances/` - Importancia de características
- `GET /api/stats/` - Estadísticas del modelo
- `POST /api/train/` - Entrenar modelo (desarrollo)
- `GET /api/analyses/` - Lista de análisis
- `GET /api/features/` - Lista de características
- `GET /api/metrics/` - Lista de métricas

## Ejemplo de Predicción

```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "Flow_Duration": 1000000,
      "Total_Fwd_Packets": 10,
      "Total_Backward_Packets": 8,
      "Flow_Bytes_s": 15000,
      "Flow_Packets_s": 18
    }
  }'
```

## Troubleshooting

### Error: Dataset no encontrado
```bash
# Copiar el archivo CSV a la carpeta data/
cp ../TotalFeatures-ISCXFlowMeter.csv data/
```

### Error: Modelo no entrenado
```bash
# Entrenar el modelo
python train_model.py
```

### Error: Puertos en uso
```bash
# Usar otro puerto
python manage.py runserver 8080
```

### Error: Migraciones pendientes
```bash
# Aplicar migraciones
python manage.py migrate
```

## Variables de Entorno Importantes

```env
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Estructura Mínima Requerida

```
malware_detection_api/
├── data/
│   └── TotalFeatures-ISCXFlowMeter.csv  # REQUERIDO
├── ml_model/
│   └── (modelos entrenados se generan aquí)
├── manage.py
└── requirements.txt
```

## Deploy en Render - Checklist

- [ ] Código subido a GitHub
- [ ] `requirements.txt` actualizado
- [ ] `runtime.txt` con versión de Python
- [ ] `Procfile` configurado
- [ ] `build.sh` con permisos de ejecución
- [ ] Variables de entorno configuradas en Render
- [ ] Dataset disponible (subir después del deploy)
- [ ] Entrenar modelo en producción después del primer deploy

## Soporte

Para más información, consulta el archivo `README.md` completo.
