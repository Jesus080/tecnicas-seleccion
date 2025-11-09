# 🛡️ API de Detección de Malware Android

Sistema de detección de malware en aplicaciones Android mediante análisis de tráfico de red con Machine Learning (Random Forest).

## 📋 Descripción

Este proyecto implementa una API REST con Django que utiliza técnicas de Machine Learning para detectar malware en aplicaciones Android. El sistema está basado en el dataset CICAAGM de la Universidad de New Brunswick y utiliza Random Forest para clasificar aplicaciones en tres categorías:

- **Benigno**: Aplicaciones legítimas
- **Adware**: Software publicitario (Airpush, Dowgin, Kemoge, Mobidash, Shuanet)
- **Malware General**: Malware tradicional (AVpass, FakeAV, FakeFlash, GGtracker, Penetho)

### 🎯 Características Principales

- ✅ API REST completa con Django REST Framework
- ✅ Clasificación con Random Forest (F1-Score > 0.93)
- ✅ Reducción de características de 79 a 10 más importantes
- ✅ Dashboard web interactivo con visualizaciones
- ✅ Despliegue en Render con GitHub
- ✅ Análisis en tiempo real de aplicaciones

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.11+
- pip
- Git
- Cuenta en [Render](https://render.com) (para deployment)

### Instalación Local

1. **Clonar el repositorio**
```bash
git clone <tu-repositorio>
cd malware_detection_api
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Linux/Mac
# o
venv\Scripts\activate  # En Windows
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Copiar el dataset**
```bash
# Copiar TotalFeatures-ISCXFlowMeter.csv a la carpeta data/
cp ../TotalFeatures-ISCXFlowMeter.csv data/
```

5. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

6. **Aplicar migraciones**
```bash
python manage.py migrate
```

7. **Crear superusuario (opcional)**
```bash
python manage.py createsuperuser
```

8. **Entrenar el modelo**
```bash
python train_model.py
```

9. **Recolectar archivos estáticos**
```bash
python manage.py collectstatic --noinput
```

10. **Ejecutar servidor de desarrollo**
```bash
python manage.py runserver
```

La aplicación estará disponible en: `http://localhost:8000`

## 📊 Dataset

El proyecto utiliza el dataset **CICAAGM** (CIC Android Adware and General Malware):

- **Total de aplicaciones**: 1900
  - Adware: 250 apps
  - Malware General: 150 apps
  - Benignas: 1500 apps

- **Características**: 79 características de tráfico de red extraídas con CIC-flowmeter
- **Fuente**: [Universidad de New Brunswick](https://www.unb.ca/cic/datasets/android-adware.html)

### Características Principales Seleccionadas (Top 10)

El modelo reduce las características de 79 a 10 más importantes, mejorando el rendimiento sin pérdida significativa de precisión.

## 🔌 API Endpoints

### Endpoints Principales

#### 1. Realizar Predicción
```http
POST /api/predict/
Content-Type: application/json

{
  "features": {
    "Flow_Duration": 1000000,
    "Total_Fwd_Packets": 10,
    "Total_Backward_Packets": 8,
    "Flow_Bytes_s": 15000,
    "Flow_Packets_s": 18
  }
}
```

**Respuesta:**
```json
{
  "prediction": "benign",
  "confidence": 0.95,
  "probabilities": {
    "benign": 0.95,
    "adware": 0.03,
    "malware": 0.02
  },
  "timestamp": "2024-11-09T10:30:00Z"
}
```

#### 2. Obtener Importancia de Características
```http
GET /api/feature-importances/
```

#### 3. Obtener Estadísticas del Modelo
```http
GET /api/stats/
```

#### 4. Entrenar Modelo (Desarrollo)
```http
POST /api/train/
```

#### 5. API Browsable
```http
GET /api/
```

### Acceso al Dashboard

- **Página Principal**: `http://localhost:8000/home/`
- **Dashboard**: `http://localhost:8000/dashboard/`
- **API REST**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`

## 🎨 Frontend

El frontend está construido con HTML, CSS y JavaScript vanilla. Incluye:

- **Página de inicio**: Información del proyecto y características
- **Dashboard interactivo**: 
  - Métricas del modelo (F1-Score, Precision, Recall)
  - Top 10 características más importantes
  - Gráficos de visualización
  - Formulario de predicción en tiempo real
  - Historial de análisis

## 🚢 Deployment en Render

### Pasos para Deploy

1. **Crear repositorio en GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <tu-repositorio-github>
git push -u origin main
```

2. **Configurar Render**
   - Ir a [Render Dashboard](https://dashboard.render.com/)
   - Click en "New +" → "Web Service"
   - Conectar tu repositorio de GitHub
   - Configurar:
     - **Name**: malware-detection-api
     - **Environment**: Python
     - **Build Command**: `./build.sh`
     - **Start Command**: `gunicorn core.wsgi:application`
     - **Plan**: Free

3. **Variables de Entorno en Render**
   
   Agregar en la sección "Environment":
   ```
   SECRET_KEY=<tu-secret-key-seguro>
   DEBUG=False
   ALLOWED_HOSTS=.render.com
   PYTHON_VERSION=3.11.6
   ```

4. **Deploy**
   - Click en "Create Web Service"
   - Render automáticamente:
     - Clonará el repositorio
     - Instalará dependencias
     - Ejecutará build.sh
     - Iniciará el servidor

5. **Subir el dataset**
   
   Después del primer deploy, conectar por SSH o usar Render Shell para subir el CSV:
   ```bash
   # Opción 1: Subir via git (si el archivo no es muy grande)
   git lfs track "*.csv"
   git add data/TotalFeatures-ISCXFlowMeter.csv
   git commit -m "Add dataset"
   git push
   
   # Opción 2: Subir manualmente via Render Shell
   # En Render Dashboard → Shell
   # Luego usar wget, curl o similar para descargar
   ```

6. **Entrenar el modelo en producción**
   
   Desde Render Shell:
   ```bash
   python train_model.py
   ```

### URL de Producción

Tu aplicación estará disponible en:
```
https://malware-detection-api.onrender.com
```

## 📁 Estructura del Proyecto

```
malware_detection_api/
├── api/                        # Aplicación Django principal
│   ├── models.py              # Modelos de base de datos
│   ├── views.py               # Vistas y lógica de API
│   ├── serializers.py         # Serializadores DRF
│   ├── urls.py                # Rutas de la API
│   └── admin.py               # Configuración del admin
├── core/                       # Configuración del proyecto
│   ├── settings.py            # Configuración Django
│   ├── urls.py                # URLs principales
│   ├── wsgi.py                # WSGI para producción
│   └── asgi.py                # ASGI para async
├── ml_model/                   # Módulo de Machine Learning
│   ├── model.py               # Clase del modelo ML
│   └── *.pkl                  # Modelos entrenados
├── templates/                  # Templates HTML
│   ├── index.html             # Página principal
│   └── dashboard.html         # Dashboard
├── static/                     # Archivos estáticos
│   ├── css/
│   │   └── style.css          # Estilos CSS
│   └── js/
│       └── dashboard.js       # JavaScript
├── data/                       # Datos
│   └── TotalFeatures-ISCXFlowMeter.csv
├── manage.py                   # Script de gestión Django
├── train_model.py             # Script para entrenar modelo
├── requirements.txt           # Dependencias Python
├── runtime.txt                # Versión de Python
├── Procfile                   # Comando para Render
├── build.sh                   # Script de build
├── .gitignore                 # Archivos ignorados por Git
├── .env.example               # Ejemplo de variables de entorno
└── README.md                  # Este archivo
```

## 🧪 Métricas del Modelo

### Random Forest Classifier

- **F1-Score (Validación)**: 0.9301
- **Precision**: 0.9302
- **Recall**: 0.9315
- **Número de estimadores**: 50
- **Características utilizadas**: 10 (de 79 originales)

### Comparación Sin Escalar vs Con Escalar

El análisis demuestra que el escalado de características tiene un impacto mínimo en el rendimiento del Random Forest, por lo que se optó por no usar escalado para simplificar el modelo.

## 🛠️ Tecnologías Utilizadas

### Backend
- **Django 4.2**: Framework web
- **Django REST Framework**: API REST
- **scikit-learn**: Machine Learning
- **pandas**: Manipulación de datos
- **numpy**: Operaciones numéricas

### Frontend
- **HTML5**: Estructura
- **CSS3**: Estilos (diseño tipo dashboard oscuro)
- **JavaScript**: Interactividad
- **Chart.js**: Visualizaciones

### Deployment
- **Gunicorn**: Servidor WSGI
- **WhiteNoise**: Archivos estáticos
- **Render**: Plataforma de hosting
- **GitHub**: Control de versiones

## 📝 Uso de la API

### Ejemplo con cURL

```bash
# Realizar predicción
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{"features": {"Flow_Duration": 1000000, "Total_Fwd_Packets": 10}}'

# Obtener características importantes
curl http://localhost:8000/api/feature-importances/

# Obtener estadísticas
curl http://localhost:8000/api/stats/
```

### Ejemplo con Python

```python
import requests

# Realizar predicción
url = "http://localhost:8000/api/predict/"
features = {
    "features": {
        "Flow_Duration": 1000000,
        "Total_Fwd_Packets": 10,
        "Total_Backward_Packets": 8
    }
}

response = requests.post(url, json=features)
result = response.json()

print(f"Predicción: {result['prediction']}")
print(f"Confianza: {result['confidence']:.2%}")
```

## 🔒 Seguridad

- Cambiar `SECRET_KEY` en producción
- Configurar `ALLOWED_HOSTS` correctamente
- Mantener `DEBUG=False` en producción
- Usar HTTPS en producción (Render lo proporciona automáticamente)
- Actualizar dependencias regularmente

## 📚 Referencias

- **Dataset**: [CIC Android Adware and General Malware Dataset](https://www.unb.ca/cic/datasets/android-adware.html)
- **Paper**: Arash Habibi Lashkari et al., "Towards a Network-Based Framework for Android Malware Detection and Characterization", PST 2017

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es parte de un trabajo académico sobre técnicas de selección de características en Machine Learning.

## 👤 Autor

Proyecto desarrollado como caso práctico de Técnicas de Selección de Características para la detección de malware Android.

## 🙏 Agradecimientos

- Universidad de New Brunswick por el dataset CICAAGM
- Comunidad de Django y scikit-learn
- Render por la plataforma de hosting

---

**Nota**: Este proyecto está diseñado con fines educativos y de investigación en el campo de la detección de malware mediante Machine Learning.
