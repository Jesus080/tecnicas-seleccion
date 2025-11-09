// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dashboard loaded');

    // Manejar el formulario de predicción
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        predictionForm.addEventListener('submit', handlePrediction);
    }

    // Cargar estadísticas del modelo
    loadModelStats();

    // Actualizar gráficos cada 30 segundos
    setInterval(loadModelStats, 30000);
});

async function handlePrediction(event) {
    event.preventDefault();
    
    const resultDiv = document.getElementById('predictionResult');
    const resultContent = document.getElementById('resultContent');
    const featuresJson = document.getElementById('featuresJson').value;
    
    try {
        // Parsear el JSON de entrada
        const features = JSON.parse(featuresJson);
        
        // Mostrar loading
        resultContent.innerHTML = '<div class="loading"></div> Analizando...';
        resultDiv.style.display = 'block';
        
        // Hacer la petición a la API
        const response = await fetch('/api/predict/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ features: features })
        });
        
        if (!response.ok) {
            throw new Error('Error en la predicción');
        }
        
        const result = await response.json();
        
        // Mostrar resultado
        displayPredictionResult(result);
        
    } catch (error) {
        resultContent.innerHTML = `
            <div class="message error">
                <strong>Error:</strong> ${error.message}
                <p>Asegúrate de que el JSON sea válido y contenga las características necesarias.</p>
            </div>
        `;
    }
}

function displayPredictionResult(result) {
    const resultContent = document.getElementById('resultContent');
    
    // Determinar el color del badge según la predicción
    let badgeClass = 'badge-benign';
    if (result.prediction.toLowerCase().includes('adware')) {
        badgeClass = 'badge-adware';
    } else if (result.prediction.toLowerCase().includes('malware')) {
        badgeClass = 'badge-malware';
    }
    
    // Crear el HTML del resultado
    let html = `
        <div class="message success">
            <h3>✅ Predicción completada</h3>
            <div style="margin-top: 20px;">
                <p><strong>Tipo detectado:</strong></p>
                <span class="badge ${badgeClass}" style="font-size: 1.2em; margin: 10px 0; display: inline-block;">
                    ${result.prediction}
                </span>
                
                <p style="margin-top: 15px;"><strong>Confianza:</strong> 
                    <span style="font-size: 1.3em; color: var(--accent-color);">
                        ${(result.confidence * 100).toFixed(2)}%
                    </span>
                </p>
                
                <div style="margin-top: 20px;">
                    <p><strong>Probabilidades por clase:</strong></p>
                    <table style="margin-top: 10px;">
                        <thead>
                            <tr>
                                <th>Clase</th>
                                <th>Probabilidad</th>
                                <th>Barra</th>
                            </tr>
                        </thead>
                        <tbody>
    `;
    
    // Agregar probabilidades
    for (const [className, prob] of Object.entries(result.probabilities)) {
        const percentage = (prob * 100).toFixed(2);
        html += `
            <tr>
                <td>${className}</td>
                <td>${percentage}%</td>
                <td>
                    <div class="importance-bar">
                        <div class="importance-fill" style="width: ${percentage}%"></div>
                    </div>
                </td>
            </tr>
        `;
    }
    
    html += `
                        </tbody>
                    </table>
                </div>
                
                <p style="margin-top: 15px; font-size: 0.9em; opacity: 0.8;">
                    <strong>Timestamp:</strong> ${new Date(result.timestamp).toLocaleString('es-ES')}
                </p>
            </div>
        </div>
    `;
    
    resultContent.innerHTML = html;
}

async function loadModelStats() {
    try {
        const response = await fetch('/api/stats/');
        if (!response.ok) return;
        
        const stats = await response.json();
        
        // Actualizar tabla de características si existe
        updateFeaturesTable(stats.top_features);
        
        // Actualizar análisis recientes si existe
        updateRecentAnalyses(stats.recent_analyses);
        
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function updateFeaturesTable(features) {
    const tbody = document.getElementById('featuresTableBody');
    if (!tbody || !features || features.length === 0) return;
    
    let html = '';
    features.forEach((feature, index) => {
        const percentage = (feature.importance_score * 100).toFixed(2);
        html += `
            <tr>
                <td>${index + 1}</td>
                <td>${feature.feature_name}</td>
                <td>${feature.importance_score.toFixed(6)}</td>
                <td>
                    <div class="importance-bar">
                        <div class="importance-fill" style="width: ${percentage}%"></div>
                    </div>
                </td>
            </tr>
        `;
    });
    
    tbody.innerHTML = html;
}

function updateRecentAnalyses(analyses) {
    // Esta función se puede implementar para actualizar la tabla de análisis recientes
    console.log('Recent analyses:', analyses);
}

// Función para cargar importancia de características
async function loadFeatureImportances() {
    try {
        const response = await fetch('/api/feature-importances/');
        if (!response.ok) return;
        
        const data = await response.json();
        
        // Crear visualización de las características
        console.log('Feature importances:', data);
        
    } catch (error) {
        console.error('Error loading feature importances:', error);
    }
}

// Cambiar entre método de entrada JSON y formulario
const inputMethod = document.getElementById('inputMethod');
if (inputMethod) {
    inputMethod.addEventListener('change', function(e) {
        const jsonInput = document.getElementById('jsonInput');
        const formInput = document.getElementById('formInput');
        
        if (e.target.value === 'json') {
            if (jsonInput) jsonInput.style.display = 'block';
            if (formInput) formInput.style.display = 'none';
        } else {
            if (jsonInput) jsonInput.style.display = 'none';
            if (formInput) formInput.style.display = 'block';
        }
    });
}

// Función auxiliar para formatear fechas
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('es-ES', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Exportar funciones para uso global
window.handlePrediction = handlePrediction;
window.loadModelStats = loadModelStats;
window.loadFeatureImportances = loadFeatureImportances;
