#!/bin/bash

echo "=========================================="
echo "🛡️  MALWARE DETECTION API - SETUP"
echo "=========================================="
echo ""

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar Python
echo -e "${BLUE}[1/8]${NC} Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 no está instalado${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python encontrado${NC}"

# Crear entorno virtual
echo -e "${BLUE}[2/8]${NC} Creando entorno virtual..."
python3 -m venv venv
echo -e "${GREEN}✓ Entorno virtual creado${NC}"

# Activar entorno virtual
echo -e "${BLUE}[3/8]${NC} Activando entorno virtual..."
source venv/bin/activate
echo -e "${GREEN}✓ Entorno virtual activado${NC}"

# Instalar dependencias
echo -e "${BLUE}[4/8]${NC} Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencias instaladas${NC}"

# Verificar dataset
echo -e "${BLUE}[5/8]${NC} Verificando dataset..."
if [ ! -f "data/TotalFeatures-ISCXFlowMeter.csv" ]; then
    echo -e "${RED}⚠ Dataset no encontrado en data/TotalFeatures-ISCXFlowMeter.csv${NC}"
    echo "Por favor, copia el archivo CSV a la carpeta data/"
else
    echo -e "${GREEN}✓ Dataset encontrado${NC}"
fi

# Aplicar migraciones
echo -e "${BLUE}[6/8]${NC} Aplicando migraciones de base de datos..."
python manage.py migrate
echo -e "${GREEN}✓ Migraciones aplicadas${NC}"

# Recolectar archivos estáticos
echo -e "${BLUE}[7/8]${NC} Recolectando archivos estáticos..."
python manage.py collectstatic --noinput
echo -e "${GREEN}✓ Archivos estáticos recolectados${NC}"

# Crear superusuario
echo -e "${BLUE}[8/8]${NC} Crear superusuario (opcional)"
read -p "¿Deseas crear un superusuario? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    python manage.py createsuperuser
fi

echo ""
echo "=========================================="
echo -e "${GREEN}✅ CONFIGURACIÓN COMPLETADA${NC}"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo ""
echo "1. Entrenar el modelo:"
echo "   python train_model.py"
echo ""
echo "2. Ejecutar el servidor:"
echo "   python manage.py runserver"
echo ""
echo "3. Acceder a la aplicación:"
echo "   http://localhost:8000/home/"
echo ""
echo "=========================================="
