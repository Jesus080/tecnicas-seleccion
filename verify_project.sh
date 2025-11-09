#!/bin/bash

# Script de verificación del proyecto
# Verifica que todos los archivos necesarios estén presentes

echo "🔍 Verificando estructura del proyecto..."
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador
TOTAL=0
OK=0
MISSING=0

check_file() {
    TOTAL=$((TOTAL+1))
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        OK=$((OK+1))
    else
        echo -e "${RED}✗${NC} $1 (FALTA)"
        MISSING=$((MISSING+1))
    fi
}

check_dir() {
    TOTAL=$((TOTAL+1))
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1/"
        OK=$((OK+1))
    else
        echo -e "${RED}✗${NC} $1/ (FALTA)"
        MISSING=$((MISSING+1))
    fi
}

echo "📁 Archivos de configuración:"
check_file "manage.py"
check_file "train_model.py"
check_file "requirements.txt"
check_file "runtime.txt"
check_file "Procfile"
check_file ".gitignore"
check_file ".env.example"
check_file "setup.sh"
check_file "build.sh"
echo ""

echo "📚 Documentación:"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "DEPLOYMENT.md"
check_file "PROJECT_SUMMARY.md"
echo ""

echo "📂 Directorios principales:"
check_dir "core"
check_dir "api"
check_dir "ml_model"
check_dir "templates"
check_dir "static"
check_dir "data"
echo ""

echo "🔧 Archivos de core/:"
check_file "core/__init__.py"
check_file "core/settings.py"
check_file "core/urls.py"
check_file "core/wsgi.py"
check_file "core/asgi.py"
echo ""

echo "🔌 Archivos de api/:"
check_file "api/__init__.py"
check_file "api/models.py"
check_file "api/views.py"
check_file "api/serializers.py"
check_file "api/urls.py"
check_file "api/admin.py"
check_file "api/tests.py"
echo ""

echo "🧠 Archivos de ml_model/:"
check_file "ml_model/__init__.py"
check_file "ml_model/model.py"
echo ""

echo "🎨 Templates:"
check_file "templates/index.html"
check_file "templates/dashboard.html"
echo ""

echo "💅 Static files:"
check_file "static/css/style.css"
check_file "static/js/dashboard.js"
echo ""

echo "📊 Dataset:"
check_file "data/TotalFeatures-ISCXFlowMeter.csv"
echo ""

echo "=================================="
echo "RESUMEN DE VERIFICACIÓN"
echo "=================================="
echo -e "Total de elementos: $TOTAL"
echo -e "${GREEN}✓ Presentes: $OK${NC}"
if [ $MISSING -gt 0 ]; then
    echo -e "${RED}✗ Faltantes: $MISSING${NC}"
    echo ""
    echo -e "${YELLOW}⚠ Hay archivos faltantes. Por favor revisa.${NC}"
    exit 1
else
    echo -e "${GREEN}✓ Faltantes: 0${NC}"
    echo ""
    echo -e "${GREEN}✅ ¡Todo está en orden! El proyecto está completo.${NC}"
    echo ""
    echo "Próximos pasos:"
    echo "1. Ejecutar ./setup.sh para instalar dependencias"
    echo "2. Entrenar el modelo: python train_model.py"
    echo "3. Iniciar el servidor: python manage.py runserver"
    exit 0
fi
