# ✅ Solución al Error y Cómo Usar el Proyecto

## 🐛 Problema Resuelto

El error que tenías era: **`no such table: api_featureimportance`**

### Causa
Las migraciones de Django no se habían aplicado, por lo que las tablas de la base de datos no existían.

### Solución Aplicada

```bash
# 1. Crear las migraciones
python manage.py makemigrations api

# 2. Aplicar las migraciones
python manage.py migrate

# 3. Entrenar el modelo
python train_model.py

# 4. Recolectar archivos estáticos
python manage.py collectstatic --noinput

# 5. Iniciar el servidor
python manage.py runserver
```

## ✅ Resultado

- ✅ **Modelo entrenado exitosamente**
  - F1-Score: 0.9292
  - Precision: 0.9292
  - Recall: 0.9305

- ✅ **79 características guardadas en BD**

- ✅ **Servidor funcionando en http://localhost:8000**

## 🌐 URLs Disponibles

Abre tu navegador en:

1. **Página Principal**: http://localhost:8000/home/
   - Información del proyecto
   - Descripción del dataset
   - Endpoints de la API

2. **Dashboard**: http://localhost:8000/dashboard/
   - ✅ Tablas de resultados (como en tus imágenes)
   - ✅ Decision Forest
   - ✅ Random Forest (Clasificación)
   - ✅ Random Forest (Regresión)
   - ✅ Comparación Sin Escalar vs Con Escalado
   - ✅ Gráficos interactivos
   - ✅ Top 10 características más importantes
   - ✅ Formulario de predicción en tiempo real

3. **API REST**: http://localhost:8000/api/
   - Navegador de API interactivo

4. **Admin Panel**: http://localhost:8000/admin/
   - Panel de administración de Django

## 📊 Dashboard - Características

El dashboard ahora incluye (similar a tus imágenes):

### ✅ Resultados del Experimento

**1. Decision Forest**
```
Métrica                | Valor
-----------------------|--------
F1 Score (Entrenamiento) | 0.930275
F1 Score (Validación)    | 0.930006
```

**2. Random Forest (Clasificación)**
```
Métrica                | Valor
-----------------------|--------
F1_Train_SinEscalar    | 0.9810
F1_Train_Escalar       | 0.9809
F1_Val_SinEscalar      | 0.9301
F1_Val_Escalar         | 0.9299
Recall_Val_SinEscalar  | 0.9315
Recall_Val_Escalar     | 0.9313
Precision_Val_SinEscalar| 0.9302
Precision_Val_Escalar  | 0.9300
```

**3. Random Forest (Regresión)**
```
Métrica                | Valor
-----------------------|--------
MSE_Train_SinEscalar   | 0.0199
R2_Train_SinEscalar    | 0.9042
MSE_Val_SinEscalar     | 0.0555
R2_Val_SinEscalar      | 0.7332
MSE_Train_Escalar      | 0.0199
R2_Train_Escalar       | 0.9043
MSE_Val_Escalar        | 0.0554
R2_Val_Escalar         | 0.7335
```

**4. Comparaciones**
- Escalado vs Sin Escalar (Clasificación)
- Escalado vs Sin Escalar (Regresión)

**5. Gráficos**
- Gráfico de Clasificación
- Random Forest Regressor - Sin escalar (con línea de tendencia)

**6. Top 10 Características**
- Visualización con barras de importancia
- Valores numéricos de importancia

**7. Predicción en Tiempo Real**
- Formulario para ingresar características
- Resultado con tipo de malware y confianza
- Probabilidades para cada clase

## 🔌 Usar la API

### Ejemplo 1: Hacer una Predicción

```bash
curl -X POST http://localhost:8000/api/predict/ \
  -H "Content-Type: application/json" \
  -d '{
    "features": {
      "Init_Win_bytes_forward": 8192,
      "max_flowiat": 1000,
      "duration": 5000,
      "flowBytesPerSecond": 15000,
      "mean_flowiat": 500,
      "Init_Win_bytes_backward": 8192,
      "flow_fin": 1,
      "flowPktsPerSecond": 20,
      "fPktsPerSecond": 10,
      "min_flowpktl": 40
    }
  }'
```

### Ejemplo 2: Ver Características Importantes

```bash
curl http://localhost:8000/api/feature-importances/
```

### Ejemplo 3: Ver Estadísticas

```bash
curl http://localhost:8000/api/stats/
```

## 🎨 Diseño del Dashboard

El dashboard tiene el mismo estilo de tus imágenes:
- ✅ Tema oscuro (negro/verde)
- ✅ Tablas con bordes verdes
- ✅ Encabezados con fondo verde oscuro
- ✅ Hover effects en las filas
- ✅ Badges de colores para tipos de malware:
  - 🟢 Verde: Benigno
  - 🟠 Naranja: Adware
  - 🔴 Rojo: Malware
- ✅ Barras de progreso para importancia de características
- ✅ Gráficos interactivos con Chart.js

## 📝 Próximos Pasos

### 1. Crear un Superusuario (Opcional)

```bash
python manage.py createsuperuser
```

Luego accede a http://localhost:8000/admin/

### 2. Probar la Predicción en el Dashboard

1. Ir a http://localhost:8000/dashboard/
2. Scroll hasta "Hacer Predicción"
3. Modificar el JSON con características
4. Click en "Predecir"
5. Ver el resultado con tipo de malware y confianza

### 3. Ver los Datos en el Admin

1. Ir a http://localhost:8000/admin/
2. Login con el superusuario
3. Ver:
   - Análisis de Malware
   - Importancia de Características
   - Métricas del Modelo

### 4. Deployment en Render

Cuando estés listo para deployment:

```bash
# 1. Inicializar Git
git init
git add .
git commit -m "Initial commit: Malware Detection API"

# 2. Subir a GitHub
git remote add origin https://github.com/TU_USUARIO/malware-detection-api.git
git push -u origin main

# 3. Seguir la guía en DEPLOYMENT.md
```

## 🔧 Comandos Útiles

```bash
# Ver logs del servidor
# (Se muestran automáticamente en la terminal)

# Ejecutar tests
python manage.py test

# Entrenar el modelo nuevamente
python train_model.py
# o
python manage.py train_model

# Shell interactivo de Django
python manage.py shell

# Ver migraciones
python manage.py showmigrations

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate
```

## 📊 Métricas Obtenidas

Después de entrenar el modelo, obtuviste:

```
F1-Score:  0.9292
Precision: 0.9292
Recall:    0.9305
```

**Top 10 características más importantes:**
1. Init_Win_bytes_forward (0.144417)
2. max_flowiat (0.038199)
3. duration (0.032465)
4. flowBytesPerSecond (0.031431)
5. mean_flowiat (0.031313)
6. Init_Win_bytes_backward (0.031048)
7. flow_fin (0.030457)
8. flowPktsPerSecond (0.028556)
9. fPktsPerSecond (0.024760)
10. min_flowpktl (0.024143)

## 🎯 Resumen

✅ **Problema resuelto**: Migraciones aplicadas
✅ **Modelo entrenado**: F1-Score de 0.9292
✅ **Servidor funcionando**: http://localhost:8000
✅ **Dashboard operativo**: Con todas las tablas y gráficos
✅ **API REST funcionando**: Endpoints disponibles
✅ **Frontend completo**: Diseño como en las imágenes

## 🚀 ¡Disfruta tu API de Detección de Malware!

Todo está funcionando correctamente. Puedes:
- Navegar por el dashboard
- Hacer predicciones
- Ver las métricas
- Usar la API REST
- Prepararte para el deployment

Si necesitas ayuda adicional, revisa:
- README.md - Documentación completa
- QUICKSTART.md - Guía rápida
- DEPLOYMENT.md - Guía de deployment
