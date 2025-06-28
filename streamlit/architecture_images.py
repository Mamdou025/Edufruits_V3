#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
architecture_images.py - Architecture EduFruit V3 avec images pré-fabriquées
Assemble des images PNG/JPG créées séparément dans une mise en page Streamlit
"""

import streamlit as st
from PIL import Image
import os


# Smart path detection with debug
if os.path.exists("images"):
    image_path = "images/"
else:
    image_path = "streamlit/images/"
    


def check_image_exists(image_path):
    """Vérifie si une image existe, sinon affiche un placeholder avec debug info"""
    if os.path.exists(image_path):
        return Image.open(image_path)
    else:
        # Debug : afficher le chemin recherché
        st.warning(f"⚠️ Image non trouvée : {image_path}")
        
        # Crée un placeholder si l'image n'existe pas
        placeholder = Image.new('RGB', (200, 150), color=(200, 200, 200))
        return placeholder

def display_architecture_with_images():
    """
    Affiche l'architecture complète en utilisant des images pré-créées
    """
    st.markdown("---")
    st.markdown("###  EduFruit V3 - Architecture Complète du Réseau de Neurones")
    st.markdown("*Architecture assemblée avec images personnalisées*")
    
    # === PREMIÈRE LIGNE : IMAGES PRINCIPALES ===
    # Colonnes avec espacement pour les flèches
    cols = st.columns([1.2, 0.2, 1.5, 0.2, 1.5, 0.2, 1.5, 0.2, 1.5, 0.2, 1.2, 0.2, 1.8, 0.2, 2.0])
    
    # Définir les chemins des images (vos images créées)
    image_paths = {
    'input': f'{image_path}input_100x100.png',      # Image 1: Grille grise
    'bloc1': f'{image_path}bloc1_stack.png',        # Image 2: Stack vert
    'bloc2': f'{image_path}bloc2_stack.png',        # Image 3: Stack violet
    'bloc3': f'{image_path}bloc3_stack.png',        # Image 4: Stack orange
    'bloc4': f'{image_path}bloc4_stack.png',        # Image 5: Stack rouge
    'gap': f'{image_path}gap_circles.png',          # Image 6: Cercles violets
    'dense': f'{image_path}neural_network.png',     # Image 7: Réseau de neurones
    'predictions': f'{image_path}predictions_bars.png'  # Image 8: À créer (barres)
    }
    
    with cols[0]:  # Image d'entrée
        img_input = check_image_exists(image_paths['input'])
        st.image(img_input, width=900)  # ← Taille contrôlée
    
    with cols[1]:  # Flèche 1
        st.markdown("<div style='text-align:center; font-size:20px; padding-top:40px;'>→</div>", 
                   unsafe_allow_html=True)
    
    with cols[2]:  # Bloc 1
        img_bloc1 = check_image_exists(image_paths['bloc1'])
        st.image(img_bloc1, width=200)  # ← Taille contrôlée
    
    with cols[3]:  # Flèche 2
        st.markdown("<div style='text-align:center; font-size:20px; padding-top:40px;'>→</div>", 
                   unsafe_allow_html=True)
    
    with cols[4]:  # Bloc 2
        img_bloc2 = check_image_exists(image_paths['bloc2'])
        st.image(img_bloc2, width=200)  # ← Taille contrôlée
    
    with cols[5]:  # Flèche 3
        st.markdown("<div style='text-align:center; font-size:20px; padding-top:40px;'>→</div>", 
                   unsafe_allow_html=True)
    
    with cols[6]:  # Bloc 3
        img_bloc3 = check_image_exists(image_paths['bloc3'])
        st.image(img_bloc3, width=200)  # ← Taille contrôlée
    
    with cols[7]:  # Flèche 4
        st.markdown("<div style='text-align:center; font-size:20px; padding-top:40px;'>→</div>", 
                   unsafe_allow_html=True)
    
    with cols[8]:  # Bloc 4
        img_bloc4 = check_image_exists(image_paths['bloc4'])
        st.image(img_bloc4, width=200)  # ← Taille contrôlée
    
    with cols[9]:  # Flèche 5
        st.markdown("<div style='text-align:center; font-size:20px; padding-top:40px;'>→</div>", 
                   unsafe_allow_html=True)
    
    with cols[10]:  # GAP
        img_gap = check_image_exists(image_paths['gap'])
        st.image(img_gap, width=300)  # ← Contrôle de la largeur
    
    with cols[11]:  # Flèche 6
        st.markdown("<div style='text-align:center; font-size:20px; padding-top:40px;'>→</div>", 
                   unsafe_allow_html=True)
    
    with cols[12]:  # Réseau neuronal
        img_dense = check_image_exists(image_paths['dense'])
        st.image(img_dense, width=200)  # ← Contrôle de la largeur
    
    with cols[13]:  # Flèche 7
        st.markdown("<div style='text-align:center; font-size:20px; padding-top:40px;'>→</div>", 
                   unsafe_allow_html=True)
    
    with cols[14]:  # Prédictions
        img_predictions = check_image_exists(image_paths['predictions'])
        st.image(img_predictions, width=200)  # ← Contrôle de la largeur
    
    # === DEUXIÈME LIGNE : TITRES ===
    st.markdown("<br>", unsafe_allow_html=True)
    cols_titles = st.columns([1.2, 0.2, 1.5, 0.2, 1.5, 0.2, 1.5, 0.2, 1.5, 0.2, 1.2, 0.2, 1.8, 0.2, 2.0])
    
    titles_and_colors = [
        ("**Image**", "#374151"),
        ("", ""),
        ("**Bloc 1**", "#22c55e"), 
        ("", ""),
        ("**Bloc 2**", "#a855f7"),
        ("", ""),
        ("**Bloc 3**", "#fb923c"),
        ("", ""),
        ("**Bloc 4**", "#f87171"),
        ("", ""),
        ("**Moyenne Globale**", "#9333ea"),
        ("", ""),
        ("**Couche Dense**", "#6366f1"),
        ("", ""),
        ("**Prédictions**", "#374151")
    ]
    
    for i, (title, color) in enumerate(titles_and_colors):
        if i < len(cols_titles) and title:
            with cols_titles[i]:
                st.markdown(f"<div style='text-align:center; color:{color}'>{title}</div>", 
                           unsafe_allow_html=True)
    
    # === TROISIÈME LIGNE : DESCRIPTIONS TECHNIQUES ===
    st.markdown("<br>", unsafe_allow_html=True)
    cols_details = st.columns([1.2, 0.2, 1.5, 0.2, 1.5, 0.2, 1.5, 0.2, 1.5, 0.2, 1.2, 0.2, 1.8, 0.2, 2.0])
    
    technical_details = [
        "100×100×3<br><small>Image RGB</small>",
        "",
        "Convolution + ReLU<br><small>32 filtres</small><br><small>50×50×32</small>",
        "",
        "Convolution + ReLU<br><small>64 filtres</small><br><small>25×25×64</small>", 
        "",
        "Convolution + ReLU<br><small>128 filtres</small><br><small>12×12×128</small>",
        "",
        "Convolution + ReLU<br><small>256 filtres</small><br><small>12×12×256</small>",
        "",
        "Global Average<br>Pooling<br><small>256 valeurs</small>",
        "",
        "Entièrement<br>Connectée<br><small>256 → 5 + Softmax</small>",
        "",
        "5 classes de fruits<br><small>Probabilités</small><br><small>Somme = 100%</small>"
    ]
    
    for i, detail in enumerate(technical_details):
        if i < len(cols_details) and detail:
            with cols_details[i]:
                st.markdown(f"<div style='text-align:center; font-size:11px; color:#6b7280'>{detail}</div>", 
                           unsafe_allow_html=True)
    
    # === SECTIONS AVEC ACCOLADES ===
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_section1, col_section2 = st.columns([7, 3])
    
    with col_section1:
        st.markdown("""
        <div style="text-align:center; padding:12px; border:2px solid #0ea5e9; border-radius:8px; background:#eff6ff;">
            <strong style="color:#0ea5e9; font-size:15px;"> Extraction de Caractéristiques de l'Image</strong><br>
            <span style="color:#1e40af; font-size:13px;">Analyse progressive : contours → textures → formes → couleurs spécialisées</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_section2:
        st.markdown("""
        <div style="text-align:center; padding:12px; border:2px solid #0ea5e9; border-radius:8px; background:#eff6ff;">
            <strong style="color:#0ea5e9; font-size:15px;"> Classification</strong><br>
            <span style="color:#1e40af; font-size:13px;">Décision finale avec probabilités</span>
        </div>
        """, unsafe_allow_html=True)
    
   
    
    # === RÉSUMÉ FINAL ===
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 16px; border-radius: 8px; margin-top: 20px;">
        <h4 style="color: #374151; margin-bottom: 8px;"> Résumé du processus :</h4>
        <p style="color: #6b7280; margin: 0; text-align: justify;">
            L'image passe par 4 blocs convolutionnels qui extraient progressivement des caractéristiques 
            (contours → textures → formes → couleurs), puis la Moyenne Globale compresse ces 
            informations en 256 valeurs numériques, et finalement la couche dense + Softmax 
            produit les probabilités finales pour chaque fruit.
        </p>
    </div>
    """, unsafe_allow_html=True)


def create_image_templates():
    """
    Fonction optionnelle pour créer des templates d'images avec PIL
    Peut servir de base pour créer vos images personnalisées
    """
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Créer le dossier images s'il n'existe pas
    os.makedirs('images', exist_ok=True)
    
    # Template pour l'image d'entrée
    def create_input_template():
        img = Image.new('RGBA', (200, 150), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # Rectangle principal
        draw.rectangle([20, 20, 180, 130], fill=(173, 216, 230, 200), outline=(0, 0, 0, 255), width=3)
        
        # Grille
        for i in range(6):
            for j in range(4):
                x1 = 30 + i * 25
                y1 = 30 + j * 25
                x2 = x1 + 25
                y2 = y1 + 25
                draw.rectangle([x1, y1, x2, y2], outline=(128, 128, 128, 128))
        
        img.save('images/input_100x100.png')
    
    # Template pour un stack de blocs
    def create_stack_template(filename, color):
        img = Image.new('RGBA', (200, 150), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        
        # 4 rectangles en stack
        for i in range(4):
            offset = i * 8
            draw.rectangle([20 + offset, 20 + offset, 160 + offset, 120 + offset], 
                         fill=color, outline=(0, 0, 0, 100))
        
        img.save(f'images/{filename}')
    
    # Créer les templates
    create_input_template()
    create_stack_template('bloc1_stack.png', (34, 197, 94, 200))    # Vert
    create_stack_template('bloc2_stack.png', (168, 85, 247, 200))   # Violet
    create_stack_template('bloc3_stack.png', (251, 146, 60, 200))   # Orange
    create_stack_template('bloc4_stack.png', (248, 113, 113, 200))  # Rouge
    


# Fonction principale pour l'utilisation
def display_complete_architecture():
    """
    Fonction principale à importer dans votre streamlit
    """
    display_architecture_with_images()