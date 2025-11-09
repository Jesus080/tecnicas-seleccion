# Guía de Deployment con GitHub y Render

## Paso 1: Preparar el Repositorio en GitHub

### 1.1 Crear el repositorio en GitHub
1. Ir a [GitHub](https://github.com)
2. Click en el botón "New repository" (Nuevo repositorio)
3. Llenar los datos:
   - **Repository name**: `malware-detection-api`
   - **Description**: "API REST para detección de malware en Android usando Random Forest"
   - **Visibility**: Public o Private (según prefieras)
   - **NO marcar**: "Add a README file" (ya tenemos uno)
4. Click en "Create repository"

### 1.2 Inicializar Git y subir el código

Desde la carpeta `malware_detection_api/`:

```bash
# Inicializar repositorio Git
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Initial commit: Malware Detection API with Django"

# Configurar la rama principal
git branch -M main

# Agregar el repositorio remoto (reemplaza YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/malware-detection-api.git

# Subir el código
git push -u origin main
```

**Nota importante sobre el dataset:**
El archivo CSV es grande (probablemente >100MB). Tienes dos opciones:

#### Opción A: No subir el CSV a GitHub (Recomendado)
Ya está configurado en `.gitignore` para que NO se suba. Luego lo subirás directamente a Render.

#### Opción B: Usar Git LFS para archivos grandes
```bash
# Instalar Git LFS
git lfs install

# Trackear archivos CSV grandes
git lfs track "*.csv"

# Agregar el archivo .gitattributes
git add .gitattributes

# Agregar el CSV
git add data/TotalFeatures-ISCXFlowMeter.csv

# Commit y push
git commit -m "Add dataset with Git LFS"
git push
```

## Paso 2: Configurar Render

### 2.1 Crear cuenta en Render
1. Ir a [Render](https://render.com)
2. Registrarse con tu cuenta de GitHub (recomendado)
3. Autorizar a Render para acceder a tus repositorios

### 2.2 Crear un nuevo Web Service

1. En el dashboard de Render, click en "New +" → "Web Service"
2. Conectar tu repositorio:
   - Si usaste la opción de registro con GitHub, verás tus repos
   - Buscar y seleccionar `malware-detection-api`
   - Click en "Connect"

3. Configurar el servicio:

   **Basic Settings:**
   - **Name**: `malware-detection-api` (o el nombre que prefieras)
   - **Region**: Elegir la más cercana (ej: Oregon, USA)
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Python 3`

   **Build & Deploy:**
   - **Build Command**: 
     ```bash
     ./build.sh
     ```
   - **Start Command**: 
     ```bash
     gunicorn core.wsgi:application
     ```

   **Plan:**
   - Seleccionar **Free** (o el plan que prefieras)

4. Click en "Advanced" para configurar variables de entorno

### 2.3 Configurar Variables de Entorno

En la sección "Environment Variables", agregar:

```
SECRET_KEY=tu-clave-secreta-super-segura-aqui-cambiala
DEBUG=False
ALLOWED_HOSTS=.render.com
PYTHON_VERSION=3.11.6
```

Para generar una SECRET_KEY segura:
```python
# En una terminal Python
import secrets
print(secrets.token_urlsafe(50))
```

5. Click en "Create Web Service"

### 2.4 Primer Deploy

Render automáticamente:
- ✅ Clonará tu repositorio
- ✅ Instalará las dependencias de `requirements.txt`
- ✅ Ejecutará `build.sh` (migraciones y collectstatic)
- ✅ Iniciará el servidor con Gunicorn

Este proceso puede tomar 5-10 minutos.

## Paso 3: Subir el Dataset a Render

### Opción A: Via Render Shell (Recomendado)

1. En tu dashboard de Render, ir a tu servicio
2. Click en "Shell" en el menú lateral
3. Se abrirá una terminal en el servidor

```bash
# Crear directorio data si no existe
mkdir -p data

# Opción 1: Descargar desde una URL (si tienes el CSV en algún lugar)
wget -O data/TotalFeatures-ISCXFlowMeter.csv "URL_DEL_CSV"

# Opción 2: Usar curl
curl -o data/TotalFeatures-ISCXFlowMeter.csv "URL_DEL_CSV"
```

### Opción B: Via Persistent Disk (Para archivos grandes)

1. En Render, ir a "Disks" → "New Disk"
2. Configurar:
   - **Name**: `malware-data`
   - **Mount Path**: `/opt/render/project/src/data`
   - **Size**: 1 GB (o lo necesario)
3. Adjuntar el disco a tu servicio
4. Subir archivos via SFTP o Shell

### Opción C: Desde tu máquina via SCP

```bash
# Obtener la URL de Render Shell y usar rsync/scp
# (Requiere configuración SSH adicional)
```

## Paso 4: Entrenar el Modelo en Producción

Una vez que el CSV esté en el servidor:

### Via Render Shell:

```bash
# En Render Shell
python train_model.py

# O usando el comando de Django
python manage.py train_model
```

## Paso 5: Verificar el Deployment

1. Render te dará una URL como: `https://malware-detection-api.onrender.com`

2. Verificar que funciona:
   ```bash
   # Probar el home
   curl https://malware-detection-api.onrender.com/home/
   
   # Probar la API
   curl https://malware-detection-api.onrender.com/api/
   
   # Probar estadísticas
   curl https://malware-detection-api.onrender.com/api/stats/
   ```

3. Abrir en el navegador:
   - Home: `https://malware-detection-api.onrender.com/home/`
   - Dashboard: `https://malware-detection-api.onrender.com/dashboard/`
   - API: `https://malware-detection-api.onrender.com/api/`

## Paso 6: Actualizaciones Futuras

### Hacer cambios y redeployar:

```bash
# 1. Hacer cambios en el código
# 2. Commit
git add .
git commit -m "Descripción de los cambios"

# 3. Push a GitHub
git push origin main
```

Render detectará automáticamente el push y redesplegará la aplicación.

### Forzar redeploy sin cambios:

En Render Dashboard:
1. Ir a tu servicio
2. Click en "Manual Deploy"
3. Seleccionar "Deploy latest commit"

## Paso 7: Monitoreo y Logs

### Ver logs en tiempo real:

En Render Dashboard:
1. Ir a "Logs" en el menú lateral
2. Ver logs en tiempo real del servidor

### Ver métricas:

1. Ir a "Metrics" para ver:
   - CPU usage
   - Memory usage
   - Request count
   - Response times

## Troubleshooting

### Error: Dataset no encontrado

```bash
# Verificar en Render Shell
ls -la data/

# Si no está, subirlo nuevamente
```

### Error: Modelo no entrenado

```bash
# En Render Shell
python train_model.py
```

### Error: Migraciones pendientes

```bash
# En Render Shell
python manage.py migrate
```

### Error: Archivos estáticos no se cargan

```bash
# En Render Shell
python manage.py collectstatic --noinput
```

### Error: 502 Bad Gateway

- Verificar que el comando de inicio sea correcto
- Revisar los logs para ver el error específico
- Verificar que todas las dependencias estén instaladas

## Configuración de Dominio Personalizado (Opcional)

Si tienes un dominio propio:

1. En Render → Settings → Custom Domain
2. Agregar tu dominio
3. Configurar los DNS según las instrucciones de Render

## Configuración de HTTPS

Render proporciona HTTPS automáticamente para todos los servicios. No necesitas configurar nada adicional.

## Backup de la Base de Datos

Para SQLite (desarrollo):
```bash
# Descargar db.sqlite3 via Shell
# Copiar y pegar el contenido
```

Para PostgreSQL (producción):
- Render hace backups automáticos en planes pagos
- Para el plan Free, necesitas hacer backups manuales

## Recursos Adicionales

- [Render Docs](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Django REST Framework](https://www.django-rest-framework.org/)

## Costos

**Plan Free de Render:**
- ✅ 750 horas/mes
- ✅ HTTPS automático
- ✅ Redeploy automático desde GitHub
- ⚠️ El servicio se "duerme" después de 15 minutos de inactividad
- ⚠️ Tarda ~1 minuto en "despertar" en la primera request

**Plan Starter ($7/mes):**
- ✅ Siempre activo
- ✅ Sin tiempo de espera
- ✅ Más recursos (RAM, CPU)

---

¡Listo! Tu API de detección de malware ya está en producción 🚀
