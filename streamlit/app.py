#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EduFruit V3 - Application Streamlit Interactive
Visualisation du fonctionnement interne d'un réseau de neurones CNN
"""

import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageFilter, ImageEnhance
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import glob
from pathlib import Path
import sys          # ADD THIS LINE
import platform     # ADD THIS LINE

#importer des illustrations 
import architecture_images


# Add this in your sidebar section 1234
def is_streamlit_cloud():
    """Detect if running on Streamlit Cloud"""
    return 'STREAMLIT_SERVER_PORT' in os.environ or 'STREAMLIT_CLOUD' in os.environ




# Smart path detection with debug
if os.path.exists("images"):
    image_path = "images/"
else:
    image_path = "streamlit/images/"
    

# Import du chargeur CSS
from css_loader import apply_custom_styles

# Configuration de la page
st.set_page_config(
    page_title="EduFruit V3 - Explorateur CNN",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Appliquer les styles CSS
apply_custom_styles()


class EduFruitExplorer:
    def __init__(self):
        self.classes = ['Pomme', 'Banane', 'Avocat', 'Concombre', 'Citron']
        self.class_emojis = ['🍎', '🍌', '🥑', '🥒', '🍋']
        self.model = None
        self.feature_extractor = None
        self.models_dir = self.get_models_directory()
        
    def get_models_directory(self):
        """Obtenir le chemin vers le dossier models dans le root du projet"""
         # Toujours chercher dans le dossier models au niveau racine
        if os.path.exists("models"):
         # Déjà dans le root (Streamlit Cloud)
           models_dir = Path("models")
        else:
         # Dans le dossier streamlit, remonter au root
           models_dir = Path("../models")
    
        print(f"Chemin recherché pour models: {models_dir}")
        print(f"Le dossier models existe: {models_dir.exists()}")
     
        return models_dir
    
    def get_latest_model(self):
        """Trouver le dernier modèle dans le dossier models"""
        try:
            model_pattern = str(self.models_dir / "*.h5")
            model_files = glob.glob(model_pattern)
            
            if not model_files:
                return None
                
            latest_model = max(model_files, key=os.path.getmtime)
            return latest_model
            
        except Exception as e:
            st.error(f"Erreur lors de la recherche des modèles: {e}")
            return None
    
    def list_available_models(self):
        """Lister tous les modèles disponibles"""
        try:
            model_pattern = str(self.models_dir / "*.h5")
            model_files = glob.glob(model_pattern)
            
            if not model_files:
                return []
                
            model_files.sort(key=os.path.getmtime, reverse=True)
            return [os.path.basename(f) for f in model_files]
            
        except Exception as e:
            st.error(f"Erreur lors de la liste des modèles: {e}")
            return []
    
    def auto_load_latest_model(self):
        """Charger automatiquement le dernier modèle disponible"""
        try:
            latest_model_path = self.get_latest_model()
            if latest_model_path:
                print(f"Chargement automatique du modèle: {latest_model_path}")
                self.model = self.load_model(latest_model_path)
                if self.model:
                    st.success(f"🚀 Modèle chargé automatiquement: {os.path.basename(latest_model_path)}")
                    return True
            else:
                st.warning("⚠️ Aucun modèle trouvé dans le dossier models/")
                return False
        except Exception as e:
            st.error(f"❌ Erreur lors du chargement automatique: {e}")
            return False
        
    @st.cache_resource
    def load_model(_self, model_path):
        """Charger le modèle entraîné"""
        try:
            model = load_model(model_path)
            
            # CORRECTION: Forcer une prédiction factice pour initialiser le modèle
            dummy_input = np.random.random((1, 100, 100, 3)).astype('float32')
            _ = model.predict(dummy_input, verbose=0)
            
            st.success(f"Modèle chargé avec succès: {os.path.basename(model_path)}")
            return model
        except Exception as e:
            st.error(f"Erreur lors du chargement du modèle: {e}")
            return None
    
    def preprocess_image(self, image):
        """Prétraiter l'image pour le modèle"""
        # Convertir en RGB si nécessaire
        if image.mode == 'RGBA':
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Redimensionner à 100x100
        image = image.resize((100, 100), Image.Resampling.LANCZOS)
        
        # Convertir en array et normaliser
        image_array = np.array(image, dtype=np.float32) / 255.0
        
        # Ajouter dimension batch
        image_array = np.expand_dims(image_array, axis=0)
        
        return image_array
    
    def apply_preprocessing_filters(self, image):
        """Applique le préprocessing avec visualisation des étapes"""
        results = {}
        
        # 1. Image originale
        results['original'] = image
        
        # 2. Redimensionnement à 100x100
        resized = image.resize((100, 100), Image.Resampling.LANCZOS)
        results['resized'] = resized
        
        # 3. Normalisation de luminosité
        enhancer = ImageEnhance.Brightness(resized)
        brightness_enhanced = enhancer.enhance(1.2)
        results['brightness'] = brightness_enhanced
        
        # 4. Image finale préprocessée
        enhancer = ImageEnhance.Contrast(brightness_enhanced)
        final_preprocessed = enhancer.enhance(1.1)
        results['final'] = final_preprocessed
        
        return results
    
    def apply_conv_filters(self, image, block_number):
        """Applique différents filtres selon le bloc convolutionnel"""
        results = {}
        
        # Convertir en array numpy pour OpenCV
        if isinstance(image, Image.Image):
            img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
        else:
            img_array = image
        
        if block_number == 1:
            # Bloc 1: Détection de base (32 filtres)
            # Filtre Sobel horizontal
            sobel_h = cv2.Sobel(img_array, cv2.CV_64F, 0, 1, ksize=3)
            results['Sobel Horizontal'] = Image.fromarray(np.uint8(np.absolute(sobel_h)))
            
            # Filtre Sobel vertical
            sobel_v = cv2.Sobel(img_array, cv2.CV_64F, 1, 0, ksize=3)
            results['Sobel Vertical'] = Image.fromarray(np.uint8(np.absolute(sobel_v)))
            
            # Filtre Laplacien
            laplacian = cv2.Laplacian(img_array, cv2.CV_64F)
            results['Laplacien'] = Image.fromarray(np.uint8(np.absolute(laplacian)))
            
            # Détection de coins
            corners = cv2.cornerHarris(img_array.astype(np.float32), 2, 3, 0.04)
            corners = cv2.dilate(corners, None)
            corners_img = np.zeros_like(img_array)
            corners_img[corners > 0.01 * corners.max()] = 255
            results['Coins Harris'] = Image.fromarray(corners_img)
            
        elif block_number == 2:
            # Bloc 2: Textures et motifs (64 filtres)
            # Filtre Gabor horizontal
            kernel_gabor = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=np.float32)
            gabor_h = cv2.filter2D(img_array, -1, kernel_gabor)
            results['Gabor Horizontal'] = Image.fromarray(np.uint8(np.clip(gabor_h + 128, 0, 255)))
            
            # Filtre diagonal
            kernel_diag = np.array([[1, 0, -1], [0, 0, 0], [-1, 0, 1]], dtype=np.float32)
            diagonal = cv2.filter2D(img_array, -1, kernel_diag)
            results['Diagonal'] = Image.fromarray(np.uint8(np.clip(diagonal + 128, 0, 255)))
            
            # Filtre circulaire
            kernel_circle = np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]], dtype=np.float32)
            circle_detect = cv2.filter2D(img_array, -1, kernel_circle)
            results['Circulaire'] = Image.fromarray(np.uint8(np.clip(circle_detect + 128, 0, 255)))
            
            # Lissage gaussien
            gaussian = cv2.GaussianBlur(img_array, (5, 5), 1.0)
            results['Gaussien'] = Image.fromarray(gaussian)
            
        elif block_number == 3:
            # Bloc 3: Formes complexes (128 filtres)
            # Détection Canny
            edges = cv2.Canny(img_array, 50, 150)
            results['Canny'] = Image.fromarray(edges)
            
            # Morphologie
            kernel = np.ones((5,5), np.uint8)
            opening = cv2.morphologyEx(img_array, cv2.MORPH_OPEN, kernel)
            results['Morphologie'] = Image.fromarray(opening)
            
            # Détection de lignes Hough
            edges_for_lines = cv2.Canny(img_array, 50, 150)
            lines = cv2.HoughLines(edges_for_lines, 1, np.pi/180, threshold=60)
            line_img = np.zeros_like(img_array)
            if lines is not None:
                for line in lines[:5]:
                    rho, theta = line[0]
                    a = np.cos(theta)
                    b = np.sin(theta)
                    x0 = a * rho
                    y0 = b * rho
                    x1 = int(x0 + 1000 * (-b))
                    y1 = int(y0 + 1000 * (a))
                    x2 = int(x0 - 1000 * (-b))
                    y2 = int(y0 - 1000 * (a))
                    cv2.line(line_img, (x1,y1), (x2,y2), 255, 2)
            results['Hough Lines'] = Image.fromarray(line_img)
            
            # LBP simplifié
            lbp_img = np.zeros_like(img_array)
            rows, cols = img_array.shape
            for i in range(1, rows-1):
                for j in range(1, cols-1):
                    center = img_array[i, j]
                    code = 0
                    code |= (img_array[i-1, j-1] > center) << 7
                    code |= (img_array[i-1, j] > center) << 6
                    code |= (img_array[i-1, j+1] > center) << 5
                    code |= (img_array[i, j+1] > center) << 4
                    lbp_img[i, j] = code
            results['LBP Texture'] = Image.fromarray(lbp_img)
            
        elif block_number == 4:
            # Bloc 4: Analyse couleur spécialisée (256 filtres)
            img_color = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            hsv = cv2.cvtColor(img_color, cv2.COLOR_BGR2HSV)
            
            # Masque rouge (Pomme)
            lower_red1 = np.array([0, 50, 50])
            upper_red1 = np.array([10, 255, 255])
            lower_red2 = np.array([170, 50, 50])
            upper_red2 = np.array([180, 255, 255])
            red_mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            red_mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
            red_mask = red_mask1 + red_mask2
            results['Masque Rouge'] = Image.fromarray(red_mask)
            
            # Masque vert (Concombre/Avocat)
            lower_green = np.array([40, 50, 50])
            upper_green = np.array([80, 255, 255])
            green_mask = cv2.inRange(hsv, lower_green, upper_green)
            results['Masque Vert'] = Image.fromarray(green_mask)
            
            # Masque jaune (Banane/Citron)
            lower_yellow = np.array([20, 50, 50])
            upper_yellow = np.array([40, 255, 255])
            yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            results['Masque Jaune'] = Image.fromarray(yellow_mask)
            
            # Analyse de forme
            gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            shape_analysis = np.zeros_like(gray)
            for contour in contours:
                if cv2.contourArea(contour) > 50:
                    epsilon = 0.02 * cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, epsilon, True)
                    
                    if len(approx) > 8:
                        cv2.drawContours(shape_analysis, [contour], -1, 255, -1)
                    elif len(approx) > 4:
                        cv2.drawContours(shape_analysis, [contour], -1, 128, -1)
            
            results['Analyse Forme'] = Image.fromarray(shape_analysis)
        
        return results
    
    def predict_with_model(self, image):
        """Faire une prédiction avec le modèle chargé"""
        if self.model is None:
            return self.simulate_prediction(image)
        
        try:
            processed_image = self.preprocess_image(image)
            predictions = self.model.predict(processed_image, verbose=0)
            
            results = {}
            for i, class_name in enumerate(self.classes):
                confidence = float(predictions[0][i] * 100)
                results[class_name] = round(confidence, 1)
            
            return results
        except Exception as e:
            st.error(f"Erreur lors de la prédiction: {e}")
            return self.simulate_prediction(image)
    
    def simulate_prediction(self, image):
        """Simuler une prédiction basée sur l'analyse des couleurs"""
        img_array = np.array(image)
        
        red_avg = np.mean(img_array[:, :, 0])
        green_avg = np.mean(img_array[:, :, 1])
        blue_avg = np.mean(img_array[:, :, 2])
        
        predictions = {"Pomme": 5, "Banane": 5, "Avocat": 5, "Concombre": 5, "Citron": 5}
        
        # Logique de simulation basée sur les couleurs dominantes
        if red_avg > green_avg and red_avg > blue_avg:
            predictions["Pomme"] = min(85, 60 + (red_avg - 120) / 3)
        elif green_avg > red_avg and green_avg > blue_avg:
            if green_avg > 140:
                predictions["Avocat"] = min(80, 50 + green_avg / 4)
            else:
                predictions["Concombre"] = min(80, 50 + green_avg / 5)
        elif red_avg > 120 and green_avg > 120 and blue_avg < 100:
            if red_avg > green_avg:
                predictions["Banane"] = min(85, 70 + (red_avg + green_avg - 240) / 3)
            else:
                predictions["Citron"] = min(80, 65 + (red_avg + green_avg - 240) / 3)
        
        # Ajouter du bruit réaliste
        for fruit in predictions:
            predictions[fruit] = max(1, predictions[fruit] + np.random.randint(-8, 12))
        
        # Normaliser
        total = sum(predictions.values())
        if total > 100:
            factor = 100 / total
            for fruit in predictions:
                predictions[fruit] = int(predictions[fruit] * factor)
        
        return predictions

def create_filter_grid(filter_results, title):
    """Créer une grille de visualisation des filtres"""
    st.markdown(f"**{title}**")
    
    if not filter_results:
        st.warning("Aucun filtre à afficher - uploadez une image pour voir les transformations")
        return
    
    # Créer une grille 2x2 ou 2x3 selon le nombre de filtres
    num_filters = len(filter_results)
    if num_filters <= 4:
        cols = st.columns(2)
        for i, (name, img) in enumerate(filter_results.items()):
            with cols[i % 2]:
                st.image(img, caption=name, use_container_width=True)
    else:
        cols = st.columns(3)
        for i, (name, img) in enumerate(filter_results.items()):
            with cols[i % 3]:
                st.image(img, caption=name, use_container_width=True)

def main():
    # Titre principal
    st.markdown("""
    <div class="title-container">
        <h1>EduFruit V3 - Explorateur de Réseau de Neurones</h1>
        <h3>Comprendre comment l'intelligence artificielle reconnaît les fruits</h3>
        <p><em>Une exploration interactive du fonctionnement interne d'un réseau de neurones convolutionnel</em></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialiser l'explorateur
    if 'explorer' not in st.session_state:
        st.session_state.explorer = EduFruitExplorer()
    
    explorer = st.session_state.explorer
    
    # Sidebar enrichie
    with st.sidebar:
                    # In your sidebar, add this 1234:
        
        if is_streamlit_cloud():
          st.write("**Deployed Environment Debug:**")
          st.write(f"TensorFlow: {tf.__version__}")
          st.write(f"Python: {sys.version}")
          st.write(f"Platform: {platform.platform()}")
        
                                   
        st.markdown("###  Paramètres & Informations")
        
        # Chargement du modèle
        st.markdown("####  Modèle")
        
        # Auto-chargement au premier démarrage
        if 'model_auto_loaded' not in st.session_state:
            st.session_state.model_auto_loaded = True
            with st.spinner(" Recherche et chargement du dernier modèle..."):
                if explorer.auto_load_latest_model():
                    st.session_state.model_loaded = True
                    st.rerun()
        
        available_models = explorer.list_available_models()
        
        if available_models:
            st.success(f" {len(available_models)} modèle(s) trouvé(s)")
            

            
            selected_model = st.selectbox(
                "Choisir un modèle différent:",
                available_models,
                help="Le premier modèle est le plus récent"
            )
            
            model_path = str(explorer.models_dir / selected_model)
            
            if st.button(" Charger ce modèle"):
                with st.spinner("Chargement..."):
                    explorer.model = explorer.load_model(model_path)
                    if explorer.model:
                        st.session_state.model_loaded = True
                        st.rerun()
                        
        else:
            st.error("❌ Aucun modèle (.h5) trouvé dans le dossier models/")
            st.info(f"📁 Dossier recherché: {explorer.models_dir}")
        
        # Informations sur le modèle
        if explorer.model:
            total_params = explorer.model.count_params()
            st.info(f"**Paramètres:** {total_params:,}")
            st.info(f"**Classes:** {len(explorer.classes)}")
        else:
            st.markdown("#### En attente")
            st.info("Prédictions simulées activées")
        
        # Options d'affichage
        
        show_formulas = st.checkbox("Afficher les formules mathématiques", value=False)
        
        st.markdown("---")
        
        # Informations éducatives (déplacées de la colonne droite)
        st.markdown("""
        <div class="info-box">
            <h4> Comment ça marche?</h4>
            <p>Un réseau de neurones convolutionnel (CNN) analyse l'image étape par étape:</p>
            <ol>
                <li><strong>Détection des bords</strong> - Contours du fruit</li>
                <li><strong>Textures</strong> - Peau lisse/rugueuse</li>
                <li><strong>Formes</strong> - Rond, allongé, etc.</li>
                <li><strong>Couleurs</strong> - Rouge, jaune, vert</li>
                <li><strong>Classification</strong> - Décision finale</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="warning-box">
            <h4> Détails Techniques</h4>
            <ul>
                <li><strong>Taille d'entrée:</strong> 100×100 pixels</li>
                <li><strong>4 blocs convolutionnels</strong></li>
                <li><strong>Filtres:</strong> 32→64→128→256</li>
                <li><strong>Régularisation:</strong> Dropout, BatchNorm</li>
                <li><strong>Classification:</strong> 5 classes de fruits</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Conseils d'utilisation
        st.markdown("""
        <div class="success-box">
            <h4> Conseils pour de meilleurs résultats</h4>
            <ul>
                <li><strong>Image claire</strong> - Bonne résolution</li>
                <li><strong>Fruit centré</strong> - Bien visible</li>
                <li><strong>Fond neutre</strong> - Pas de distractions</li>
                <li><strong>Éclairage uniforme</strong> - Éviter les ombres</li>
                <li><strong>Un seul fruit</strong> - Pas de mélanges</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Fruits supportés
        st.markdown("""
        <div class="info-box">
            <h4> Fruits supportés par EduFruit V3</h4>
            <ul>
                <li>🍎 <strong>Pommes</strong> - Toutes variétés</li>
                <li>🍌 <strong>Bananes</strong> - Mûres ou vertes</li>
                <li>🥑 <strong>Avocats</strong> - Différents stades</li>
                <li>🥒 <strong>Concombres</strong> - Formes diverses</li>
                <li>🍋 <strong>Citrons</strong> - Meyer et classiques</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Contenu principal - Une seule colonne
    # Étape 1: Upload d'image
    with st.expander("**Étape 1 - Choisir une image de fruit**", expanded=True):
        st.write("Sélectionnez une image claire d'un fruit pour commencer l'analyse du réseau de neurones.")
        

        
        uploaded_file = st.file_uploader(
            "Sélectionnez une image de fruit (JPG, PNG)",
            type=['jpg', 'jpeg', 'png'],
            help="Choisissez une image claire d'un fruit sur fond neutre"
        )
        
        # Variables pour l'image
        current_image = None
        preprocessed_image = None
        
        if uploaded_file is not None:
            # Image uploadée
            current_image = Image.open(uploaded_file)
            col_img1, col_img2 = st.columns(2)
            
            with col_img1:
                st.markdown("**Image originale**")
                st.image(current_image, caption="Votre image", use_container_width=True)
            
            # Prétraitement
            preprocessing_results = explorer.apply_preprocessing_filters(current_image)
            preprocessed_image = preprocessing_results['final']
            
            with col_img2:
                st.markdown("**Image prétraitée (100×100)**")
                st.image(preprocessed_image, caption="Prête pour l'IA", use_container_width=True)
        
        else:
            # Image par défaut pour démonstration
            st.info("📸 Uploadez une image ou explorez avec l'exemple ci-dessous")
            
            try:
                demo_img = Image.open(f"{image_path}pomme1.png")  # Votre image
                current_image = demo_img
                preprocessed_image = demo_img
            except:
                # Fallback si l'image n'est pas trouvée
                demo_img = Image.new('RGB', (100, 100), color=(255, 200, 50))
                current_image = demo_img
                preprocessed_image = demo_img
            
            col_demo1, col_demo2 = st.columns(2)
            with col_demo1:
                st.markdown("**Image de démonstration**")
                st.image(demo_img, caption="Exemple (couleur banane)", use_container_width=True)
            with col_demo2:
                st.markdown("**Prêt pour analyse**")
                st.image(demo_img, caption="Format 100×100", use_container_width=True)
        
        if show_formulas:
            st.markdown("""
            <div class="formula-box">
            <strong>Prétraitement:</strong><br>
            • Redimensionnement: Image → 100×100 pixels<br>
            • Normalisation: Pixel(0-255) → Pixel(0-1)<br>
            • Formule: pixel_normalisé = pixel_original ÷ 255
            </div>
            """, unsafe_allow_html=True)
    
    # Étape 2: Bloc Convolutionnel 1
    with st.expander("**Bloc 1 - Détection des contours de base (32 filtres)**", expanded=True):
        st.write("Le réseau commence par détecter les formes de base comme les bords et les contours du fruit. Cette première couche convolutionnelle détecte les caractéristiques simples : bords, lignes, contours. C'est comme si le réseau apprenait à \"voir\" les formes basiques de votre fruit.")
        st.write("""
Le réseau commence par analyser l'image avec **deux couches convolutionnelles successives** utilisant 32 filtres chacune. 

**Processus détaillé :**
- **1ère Conv2D(32)** : Détecte les bords horizontaux, verticaux et diagonaux
- **BatchNormalization** : Stabilise l'apprentissage et accélère la convergence  
- **2ème Conv2D(32)** : Affine la détection des contours et combine les caractéristiques
- **MaxPooling2D(2×2)** : Réduit la taille de 100×100 → ~48×48 tout en gardant l'essentiel
- **Dropout(25%)** : Prévient le surapprentissage en désactivant aléatoirement des neurones

**Résultat :** Le bloc transforme l'image RGB en 32 cartes de caractéristiques qui "voient" les contours du fruit.
""")
        
        





               # === AJOUT DE L'ILLUSTRATION ===
        st.markdown("####  Visualisation du processus")
        st.image(f"{image_path}bloc1.png", caption="Description de votre image", width=900) 
        
        st.markdown("""
        <div class="info-box">
            <h4> Fonctionnement interne</h4>
            <ul>
                <li><strong>Détection de contours</strong> : Trouve où l'objet commence et finit</li>
                <li><strong>Filtres multiples</strong> : 32 détecteurs différents pour capturer diverses caractéristiques</li>
                <li><strong>Invariance spatiale</strong> : Peut détecter un contour n'importe où dans l'image</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        

        # Visualisations des filtres
        if current_image:
            block1_results = explorer.apply_conv_filters(preprocessed_image, 1)
            create_filter_grid(block1_results, "Exemples de filtres du Bloc 1")
        else:
            st.info("Uploadez une image pour voir les transformations réelles")
      
        
      
    if show_formulas:
        st.markdown("""
        <div class="formula-box">
        <strong>Convolution 2D:</strong><br>
        S(i,j) = ΣΣ I(i+m,j+n) × K(m,n)<br>
        <strong>Dimension:</strong> 100×100×3 → 50×50×32
        </div>
        """, unsafe_allow_html=True)
    
    # Étape 3: Bloc Convolutionnel 2
    with st.expander("**Bloc 2 - Textures et Motifs (64 filtres)**", expanded=True):
        st.write("Le réseau détecte maintenant les textures de la peau du fruit et les motifs répétitifs.")
        
        st.write("""
Le deuxième bloc se concentre sur l'analyse des **textures et motifs complexes** avec 64 filtres pour capturer plus de nuances que le bloc précédent.

**Architecture du Bloc 2 :**
- **1ère Conv2D(64, 3×3)** : Détecte les micro-textures de la peau des fruits
- **BatchNormalization** : Stabilise l'apprentissage avec plus de filtres actifs
- **2ème Conv2D(64, 3×3)** : Combine les textures en motifs plus sophistiqués
- **MaxPooling2D(2×2)** : Réduit la résolution de ~48×48 → ~22×22
- **Dropout(25%)** : Évite la spécialisation excessive sur des textures spécifiques

**Ce que détecte ce bloc :**
- **Peau lisse** d'une pomme vs **surface rugueuse** d'un avocat
- **Motifs striés** d'une banane vs **texture granuleuse** d'une orange
- **Variations de brillance** et micro-détails de surface
- **Patterns répétitifs** caractéristiques de chaque type de fruit

**Transformation :** L'image passe de 32 → 64 cartes de caractéristiques, doublant la capacité d'analyse des textures tout en réduisant la taille spatiale pour se concentrer sur l'essentiel.
""")
                # === AJOUT DE L'ILLUSTRATION ===
        st.markdown("####  Visualisation du processus")
        st.image(f"{image_path}bloc2.png", caption="Description de votre image", width=900) 
        
        st.markdown("""
        <div class="info-box">
            <h4> Fonctionnement interne</h4>
            <ul>
                <li><strong>Analyse de texture</strong> : Distingue peau lisse (pomme) vs rugueuse (avocat)</li>
                <li><strong>Motifs complexes</strong> : 64 filtres pour détecter des patterns plus sophistiqués</li>
                <li><strong>Combinaison de caractéristiques</strong> : Combine les contours du bloc 1 avec les textures</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualisations des filtres
        if current_image:
            block2_results = explorer.apply_conv_filters(preprocessed_image, 2)
            create_filter_grid(block2_results, "Exemples de filtres du Bloc 2")
        else:
            st.info("Uploadez une image pour voir les transformations réelles")
    
    # Étape 4: Bloc Convolutionnel 3
    with st.expander("**Bloc 3 - Formes Complexes (128 filtres)**", expanded=True):
        st.write("Reconnaissance de formes plus complexes et spécifiques à chaque type de fruit.")
        
        st.write("""
Le troisième bloc se concentre sur la **reconnaissance de formes géométriques** avec 128 filtres pour une analyse encore plus fine des caractéristiques structurelles.

**Architecture du Bloc 3 :**
- **1ère Conv2D(128, 3×3)** : Identifie les formes globales et leurs contours
- **BatchNormalization** : Maintient la stabilité avec 128 filtres simultanés
- **2ème Conv2D(128, 3×3)** : Affine la détection des formes et capture leurs variations
- **MaxPooling2D(2×2)** : Compresse de ~22×22 → ~9×9 en préservant la géométrie
- **Dropout(25%)** : Prévient la mémorisation de formes spécifiques

**Ce que détecte ce bloc :**
- **Forme ronde** d'une pomme vs **forme allongée** d'une banane
- **Silhouette ovale** d'un avocat vs **forme sphérique** d'une orange
- **Courbures caractéristiques** et angles spécifiques à chaque fruit
- **Proportions géométriques** : rapport largeur/hauteur distinctif
- **Symétries** et **asymétries** naturelles des fruits
- **Contours globaux** qui définissent la signature visuelle de chaque espèce

**Transformation :** L'image évolue de 64 → 128 cartes de caractéristiques, doublant la capacité d'analyse des formes tout en se concentrant sur les aspects géométriques essentiels.
""")
                # === AJOUT DE L'ILLUSTRATION ===
        st.markdown("####  Visualisation du processus")
        st.image(f"{image_path}bloc3.png", caption="Description de votre image", width=900) 
        
        
        st.markdown("""
        <div class="info-box">
            <h4> Fonctionnement interne</h4>
            <ul>
                <li><strong>Formes géométriques</strong> : Distingue rond (pomme) vs allongé (banane)</li>
                <li><strong>Caractéristiques spécifiques</strong> : 128 filtres pour capturer des détails uniques</li>
                <li><strong>Abstraction croissante</strong> : Passe des pixels aux concepts de forme</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualisations des filtres
        if current_image:
            block3_results = explorer.apply_conv_filters(preprocessed_image, 3)
            create_filter_grid(block3_results, "Exemples de filtres du Bloc 3")
        else:
            st.info("Uploadez une image pour voir les transformations réelles")
    
    # Étape 5: Bloc Convolutionnel 4
    with st.expander("**Bloc 4 - Caractéristiques Spécialisées (256 filtres)**", expanded=True):
        st.write("Détection des caractéristiques très spécifiques qui permettent de distinguer chaque fruit.")
        
        st.write("""
Le bloc final est **hautement spécialisé** avec 256 filtres et une architecture unique sans pooling pour préserver les détails les plus fins.

**Architecture du Bloc 4 :**
- **Conv2D(256, 3×3)** : UNE SEULE convolution avec 256 filtres ultra-spécialisés
- **BatchNormalization** : Stabilise les 256 activations simultanées
- **Dropout(25%)** : Régularisation finale avant la classification
- **AUCUN MaxPooling** : Préserve la résolution spatiale (~9×9 → ~7×7) pour les détails critiques

**Ce que détecte ce bloc :**
- **Rouge intense** d'une pomme vs **rouge-orangé** d'une pêche
- **Vert foncé** d'un avocat mûr vs **vert clair** d'un avocat jeune
- **Jaune uniforme** d'une banane vs **jaune tacheté** d'une banane mûre
- **Orange vif** d'une orange vs **orange pâle** d'un citron Meyer
- **Nuances de brillance** : peau mate vs peau luisante
- **Dégradés de couleurs** spécifiques à chaque variété de fruit
- **Zones de transition** entre différentes teintes sur un même fruit
- **Micro-détails colorimétriques** invisibles à l'œil nu mais cruciaux pour l'IA

**Transformation :** Passage de 128 → 256 cartes ultra-spécialisées qui capturent les signatures colorimétriques uniques, permettant une discrimination fine entre fruits similaires.
""")
                # === AJOUT DE L'ILLUSTRATION ===
        st.markdown("####  Visualisation du processus")
        st.image(f"{image_path}bloc4.png", caption="Description de votre image", width=900) 
        
        st.markdown("""
        <div class="info-box">
            <h4> Fonctionnement interne</h4>
            <ul>
                <li><strong>Analyse couleur avancée</strong> : Sépare rouge-pomme, vert-avocat, jaune-banane</li>
                <li><strong>Spécialisation maximum</strong> : 256 filtres ultra-spécialisés par type de fruit</li>
                <li><strong>Représentation finale</strong> : Combine forme, texture, couleur en signature unique</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Visualisations des filtres
        if current_image:
            block4_results = explorer.apply_conv_filters(preprocessed_image, 4)
            create_filter_grid(block4_results, "Exemples de filtres du Bloc 4")
        else:
            st.info("Uploadez une image pour voir les transformations réelles")
    
    # Étape 6: Global Average Pooling
    with st.expander("**Étape 6 - Moyenne Globale**", expanded=True):
        st.write(" À cette étape, nous avons 256 cartes de caractéristiques de 12×12 pixels chacune.\n\n Le Global Average Pooling calcule la **valeur moyenne** de chaque carte : il additionne tous les pixels d'une carte (144 valeurs) puis divise par 144. Cette opération transforme nos 256 cartes en exactement **256 valeurs numériques** - une par caractéristique détectée.\n\n  Peu importe où se trouve une caractéristique dans l'image, sa 'force moyenne' sera capturée de la même façon. Ces 256 nombres résument parfaitement toute l'information nécessaire pour identifier le fruit !")
        
        st.write("""
**Transformation cruciale :** Les 256 cartes de caractéristiques de 7×7 pixels (soit 12,544 valeurs) sont compressées en exactement **256 valeurs numériques**.

**Comment ça fonctionne :**
- Pour chaque carte de 7×7 = 49 pixels, calcule la **moyenne arithmétique**
- Résultat : 49 valeurs → 1 seule valeur représentative
- Répète l'opération pour les 256 cartes
- **Avantage :** Peu importe où se trouve la caractéristique dans l'image, sa 'force moyenne' est capturée

**Résultat :** 256 nombres qui résument TOUTE l'information visuelle nécessaire pour identifier le fruit.
""")
                        # === AJOUT DE L'ILLUSTRATION ===
        st.markdown("####  Visualisation du processus")
        st.image(f"{image_path}moyenne.png", caption="Description de votre image", width=900) 
        


        st.markdown("""
        <div class="info-box">
            <h4> Fonctionnement interne</h4>
            <ul>
                <li><strong>Compression intelligente</strong> : Résume 12×12×256 = 36,864 valeurs en 256</li>
                <li><strong>Invariance à la position</strong> : Peu importe où est le fruit dans l'image</li>
                <li><strong>Préparation classification</strong> : Convertit les cartes 2D en vecteur 1D</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Simulation des valeurs GAP
        if current_image:
            # Simuler 256 valeurs pour Global Average Pooling
            gap_values = np.random.random(256) * 2 - 1  # Valeurs entre -1 et 1
            
            fig_gap = px.bar(
                x=list(range(len(gap_values))),
                y=gap_values,
                title="256 Valeurs de la Moyenne Globale",
                labels={'x': 'Caractéristique', 'y': 'Valeur'}
            )
            fig_gap.update_layout(height=400)
            st.plotly_chart(fig_gap, use_container_width=True)
        else:
            st.info("Uploadez une image pour voir les valeurs numériques")
    
    if show_formulas:
        st.markdown("""
        <div class="formula-box">
        <strong>Global Average Pooling :</strong><br>
        GAP = (1/HW) × ΣᵢΣⱼ feature_map[i,j]<br>
        <strong>Résultat:</strong> 12×12×256 → 256 valeurs
        </div>
        """, unsafe_allow_html=True)
    
    # Étape 7: Classification finale
    with st.expander("**Étape 7 - Classification Finale**", expanded=True):
        st.write("Le réseau transforme les 256 valeurs en probabilités pour chaque type de fruit.")
        
        st.write("""
La classification utilise **trois couches denses successives** pour transformer les 256 caractéristiques extraites en décision finale ultra-précise.

**Architecture de classification :**

**1. Dense Layer 1 (256 → 512 neurones) :**
- **Expansion :** Multiplie les possibilités de combinaisons par 2
- **ReLU + BatchNorm + Dropout(50%)** : Apprentissage robuste et régularisé

**2. Dense Layer 2 (512 → 256 neurones) :**  
- **Consolidation :** Affine et optimise les combinaisons importantes
- **ReLU + BatchNorm + Dropout(50%)** : Évite le surapprentissage

**3. Dense Layer 3 (256 → 5 classes) :**
- **Décision finale :** Transforme en probabilités via Softmax
- **Sortie :** 5 probabilités qui somment à 100%

**Ce que traite cette étape :**
- **Combinaisons complexes** : "Rouge + rond + lisse" = forte probabilité de pomme
- **Associations multi-caractéristiques** : "Jaune + allongé + strié" = signature banane
- **Exclusions logiques** : Si "vert dominant" alors probabilité faible pour orange
- **Pondérations intelligentes** : Importance relative des couleurs vs formes selon le contexte
- **Résolution d'ambiguïtés** : Distinguer citron vert d'avocat vert par la forme
- **Calibrage des certitudes** : Ajuster les probabilités selon la clarté des signaux
- **Décision multicritères** : Synthèse finale de tous les indices visuels collectés
- **Gestion des cas limites** : Fruits partiellement visibles ou en transition de maturité

**Transformation :** Les 256 caractéristiques abstraites deviennent 5 probabilités concrètes permettant l'identification précise du fruit.
""")
                                # === AJOUT DE L'ILLUSTRATION ===
        st.markdown("####  Visualisation du processus")
        st.image(f"{image_path}finale.png", caption="Description de votre image", width=900) 
        
        st.markdown("""
        <div class="info-box">
            <h4> Fonctionnement interne</h4>
            <ul>
                <li><strong>Décision finale</strong> : Convertit les caractéristiques en probabilités</li>
                <li><strong>Fonction Softmax</strong> : Assure que toutes les probabilités somment à 100%</li>
                <li><strong>Confiance mesurable</strong> : Plus la probabilité est élevée, plus le modèle est sûr</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Prédictions avec nouveau layout
        if current_image:
            predictions = explorer.predict_with_model(current_image)
            
            col_prob, col_pred = st.columns([2, 1])  # 2/3 pour probas, 1/3 pour prédiction
            
            with col_prob:
                # Graphique des probabilités (plus large)
                prob_df = pd.DataFrame({
                    'Fruit': [f"{name}" for name in explorer.classes],  # Sans emojis dans le graphique
                    'Probabilité': [predictions[name] for name in explorer.classes]
                })
                
                fig_prob = px.bar(
                    prob_df,
                    x='Probabilité',
                    y='Fruit',
                    orientation='h',
                    title="Probabilités pour chaque fruit",
                    color='Probabilité',
                    color_continuous_scale='Blues'
                )
                fig_prob.update_layout(height=350, showlegend=False)
                fig_prob.update_traces(texttemplate='%{x:.1f}%', textposition='outside')
                st.plotly_chart(fig_prob, use_container_width=True)
            
            with col_pred:
                # Prédiction finale (plus compact)
                best_fruit = max(predictions, key=predictions.get)
                best_confidence = predictions[best_fruit]
                fruit_emoji = explorer.class_emojis[explorer.classes.index(best_fruit)]
                
                st.markdown(f"""
                <div class="prediction-result-compact">
                    <h3> Résultat</h3>
                    <div class="fruit-prediction">
                        <span class="fruit-emoji">{fruit_emoji}</span>
                        <span class="fruit-name">{best_fruit}</span>
                    </div>
                    <div class="confidence-score">{best_confidence:.1f}%</div>
                    <div class="confidence-label">de confiance</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Uploadez une image pour voir la prédiction finale")
    
    if show_formulas:
        st.markdown("""
        <div class="formula-box">
        <strong>Fonction Softmax:</strong><br>
        P(classe_i) = exp(score_i) ÷ Σ exp(score_j)<br>
        <strong>Résultat:</strong>Probabilités qui somment à 100%
        </div>
        """, unsafe_allow_html=True)
        

    architecture_images.display_complete_architecture()


if __name__ == "__main__":
    main()