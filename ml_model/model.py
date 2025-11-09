"""
Módulo para entrenar y cargar el modelo de Machine Learning
"""
import os
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import f1_score, precision_score, recall_score
from django.conf import settings


class MalwareDetectionModel:
    """
    Clase para manejar el modelo de detección de malware
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.top_features = None
        self.class_labels = None
        self.model_path = settings.MODEL_DIR / 'random_forest_model.pkl'
        self.scaler_path = settings.MODEL_DIR / 'scaler.pkl'
        self.features_path = settings.MODEL_DIR / 'features.pkl'
    
    def train_val_test_split(self, df, rstate=42, shuffle=True, stratify=None):
        """
        Función para particionar el dataset en train/val/test
        """
        strat = df[stratify] if stratify else None
        train_set, test_set = train_test_split(
            df, test_size=0.4, random_state=rstate, shuffle=shuffle, stratify=strat)
        strat = test_set[stratify] if stratify else None
        val_set, test_set = train_test_split(
            test_set, test_size=0.5, random_state=rstate, shuffle=shuffle, stratify=strat)
        return (train_set, val_set, test_set)
    
    def remove_labels(self, df, label_name):
        """
        Separar características y etiquetas
        """
        X = df.drop(label_name, axis=1)
        y = df[label_name].copy()
        return (X, y)
    
    def train_model(self, csv_path=None, n_estimators=50, random_state=42):
        """
        Entrenar el modelo Random Forest con el dataset
        """
        if csv_path is None:
            csv_path = settings.DATA_DIR / 'TotalFeatures-ISCXFlowMeter.csv'
        
        print(f"Cargando dataset desde: {csv_path}")
        df = pd.read_csv(csv_path)
        
        # Transformar la variable de salida a numérica
        X = df.copy()
        X['calss'] = X['calss'].factorize()[0]
        
        # Guardar las etiquetas de clase
        self.class_labels = df['calss'].unique().tolist()
        
        # División del dataset
        train_set, val_set, test_set = self.train_val_test_split(X, stratify='calss')
        
        X_train, y_train = self.remove_labels(train_set, 'calss')
        X_val, y_val = self.remove_labels(val_set, 'calss')
        X_test, y_test = self.remove_labels(test_set, 'calss')
        
        # Guardar nombres de características
        self.feature_names = X_train.columns.tolist()
        
        # Entrenar modelo
        print("Entrenando Random Forest...")
        self.model = RandomForestClassifier(
            n_estimators=n_estimators, 
            random_state=random_state, 
            n_jobs=-1
        )
        self.model.fit(X_train, y_train)
        
        # Obtener importancia de características
        feature_importances = {
            name: score 
            for name, score in zip(self.feature_names, self.model.feature_importances_)
        }
        feature_importances_sorted = pd.Series(feature_importances).sort_values(ascending=False)
        
        # Guardar top 10 características
        self.top_features = list(feature_importances_sorted.head(10).index)
        
        # Evaluar modelo
        y_pred = self.model.predict(X_val)
        f1 = f1_score(y_val, y_pred, average='weighted')
        precision = precision_score(y_val, y_pred, average='weighted')
        recall = recall_score(y_val, y_pred, average='weighted')
        
        print(f"\nMétricas del modelo:")
        print(f"F1-Score: {f1:.4f}")
        print(f"Precision: {precision:.4f}")
        print(f"Recall: {recall:.4f}")
        
        # Guardar modelo y características
        self.save_model()
        
        return {
            'f1_score': f1,
            'precision': precision,
            'recall': recall,
            'top_features': self.top_features,
            'feature_importances': feature_importances_sorted.to_dict()
        }
    
    def save_model(self):
        """
        Guardar el modelo entrenado
        """
        os.makedirs(settings.MODEL_DIR, exist_ok=True)
        
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        
        with open(self.features_path, 'wb') as f:
            pickle.dump({
                'feature_names': self.feature_names,
                'top_features': self.top_features,
                'class_labels': self.class_labels
            }, f)
        
        print(f"Modelo guardado en: {self.model_path}")
    
    def load_model(self):
        """
        Cargar modelo pre-entrenado
        """
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(
                f"Modelo no encontrado en {self.model_path}. "
                "Por favor entrena el modelo primero."
            )
        
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        with open(self.features_path, 'rb') as f:
            features_data = pickle.load(f)
            self.feature_names = features_data['feature_names']
            self.top_features = features_data['top_features']
            self.class_labels = features_data['class_labels']
        
        print("Modelo cargado exitosamente")
    
    def predict(self, features_dict):
        """
        Hacer predicción con nuevas características
        
        Args:
            features_dict: Diccionario con las características
        
        Returns:
            dict: Predicción, confianza y probabilidades
        """
        if self.model is None:
            self.load_model()
        
        # Crear DataFrame con las características
        df = pd.DataFrame([features_dict])
        
        # Asegurar que tenemos todas las características necesarias
        for feature in self.feature_names:
            if feature not in df.columns:
                df[feature] = 0
        
        # Reordenar columnas para que coincidan con el entrenamiento
        df = df[self.feature_names]
        
        # Hacer predicción
        prediction = self.model.predict(df)[0]
        probabilities = self.model.predict_proba(df)[0]
        
        # Obtener clase predicha
        predicted_class = self.class_labels[prediction] if self.class_labels else str(prediction)
        
        # Crear diccionario de probabilidades
        prob_dict = {
            str(label): float(prob) 
            for label, prob in zip(self.class_labels or range(len(probabilities)), probabilities)
        }
        
        return {
            'prediction': predicted_class,
            'confidence': float(max(probabilities)),
            'probabilities': prob_dict
        }
    
    def get_feature_importances(self):
        """
        Obtener importancia de características
        """
        if self.model is None:
            self.load_model()
        
        return {
            name: float(score) 
            for name, score in zip(self.feature_names, self.model.feature_importances_)
        }


# Instancia global del modelo
ml_model = MalwareDetectionModel()
