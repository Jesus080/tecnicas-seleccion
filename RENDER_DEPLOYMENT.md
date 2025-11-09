# 🚀 Configuración para Render (Dashboard Estático)

Este proyecto está configurado para **visualización estática** en Render, sin necesidad de entrenar el modelo en producción.

## ✅ Requisitos Previos

- Los datos del modelo ya están pre-calculados en archivos JSON (`api/static_data/`)
- No se requieren librerías de ML (pandas, numpy, scikit-learn) en producción
- Solo se sirven visualizaciones estáticas del dashboard

---

## ⚙️ Configuración en Render

### 1. **General Settings**

```
Name: malware-detection-api
Region: Frankfurt (EU Central)
Branch: main
Root Directory: [DEJAR VACÍO]
Environment: Python 3
```

### 2. **Build & Deploy Commands**

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
```

**Start Command:**
```bash
gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```

### 3. **Environment Variables** (Click "Advanced")

Agrega estas 4 variables:

```bash
# 1. SECRET_KEY (genera una con el comando de abajo)
SECRET_KEY=tu-clave-secreta-aqui

# 2. DEBUG
DEBUG=False

# 3. ALLOWED_HOSTS
ALLOWED_HOSTS=.onrender.com

# 4. PYTHON_VERSION (IMPORTANTE: especifica versión para evitar 3.13)
PYTHON_VERSION=3.11.0
```

#### Generar SECRET_KEY (ejecuta localmente):
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📝 Checklist de Deployment

- [ ] Repositorio conectado: `Jesus080/tecnicas-seleccion`
- [ ] Build Command configurado correctamente
- [ ] Start Command: `gunicorn core.wsgi:application --bind 0.0.0.0:$PORT`
- [ ] 4 variables de entorno agregadas (especialmente `PYTHON_VERSION=3.11.0`)
- [ ] Root Directory: **VACÍO** (no poner "malware_detection_api")
- [ ] Plan: Free (0$/mes)

---

## 🎯 URLs de la Aplicación Desplegada

Una vez desplegado, tu aplicación estará disponible en:

- **Dashboard**: `https://tu-app.onrender.com/dashboard/`
- **API Root**: `https://tu-app.onrender.com/api/`
- **Estadísticas**: `https://tu-app.onrender.com/api/stats/`
- **Features**: `https://tu-app.onrender.com/api/feature-importances/`

---

## 🔧 Troubleshooting

### Error: Python 3.13 incompatibilidad

**Solución**: Asegúrate de agregar la variable de entorno:
```
PYTHON_VERSION=3.11.0
```

### Error: No module named 'pandas'

**Esto es correcto**: La aplicación ya no necesita pandas en producción. Los datos están en JSON.

### Error: DisallowedHost

**Solución**: Verifica la variable de entorno:
```
ALLOWED_HOSTS=.onrender.com
```

El punto (`.`) antes de `onrender.com` es importante.

---

## 📦 Dependencias

### Production (`requirements.txt`)
- Django 4.2.7
- Django REST Framework 3.14.0
- Gunicorn 21.2.0
- WhiteNoise 6.6.0
- psycopg2-binary 2.9.9

**NO incluye**: pandas, numpy, scikit-learn, matplotlib (no necesarios para visualización estática)

---

## 🎨 Características del Dashboard Estático

✅ Visualización de métricas pre-calculadas (F1: 0.9292)  
✅ Top 10 características más importantes  
✅ Gráficos interactivos con Chart.js  
✅ Análisis recientes de malware  
✅ Tema oscuro/verde profesional  
✅ Responsive design  

---

## 🔄 Actualizar la Aplicación

Cada push a GitHub despliega automáticamente:

```bash
git add .
git commit -m "Update dashboard"
git push origin main
```

Render detectará el cambio y redesplegará (2-5 minutos).

---

## 📊 Datos Estáticos Incluidos

Los siguientes archivos JSON contienen los datos pre-calculados:

```
api/static_data/
├── feature_importances.json  (79 características)
├── model_metrics.json        (F1, Precision, Recall)
├── recent_analyses.json      (4 análisis de ejemplo)
└── summary.json              (Información del modelo)
```

Estos archivos permiten que el dashboard funcione sin necesidad de entrenar el modelo.

---

## ✨ Ventajas de este Approach

✅ **Deploy rápido**: ~2 minutos (vs 10+ minutos compilando pandas)  
✅ **Sin errores de compilación**: No hay problemas de compatibilidad Python 3.13  
✅ **Lightweight**: ~50MB (vs 500MB+ con ML libs)  
✅ **Funciona en plan Free**: No excede límites de memoria  
✅ **Mantenible**: Actualizaciones sin recompilar librerías C  

---

🎉 **¡Tu aplicación está lista para producción!**
