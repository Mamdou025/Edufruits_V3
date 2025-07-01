#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
filter_test_page.py - Page de test pour les filtres CNN
Page Streamlit simple pour tester les visualisations de filtres avant intégration
"""

import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="Test Filtres CNN - EduFruit V3",
    page_icon="🔬",
    layout="wide"
)

class SimpleFilterTester:
    def __init__(self):
        self.filter_examples = {
            'bloc1_conv1': {
                'Sobel Vertical': np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
                'Sobel Horizontal': np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]]),
            },
            'bloc1_conv2': {
                'Edge Enhancement': np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
                'Gaussian Blur': np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 16,
            },
            'bloc2_conv1': {
                'Diagonale': np.array([[1, 0, -1], [0, 0, 0], [-1, 0, 1]]),
                'Détection Lignes': np.array([[-1, -1, -1], [2, 2, 2], [-1, -1, -1]]),
            },
            'bloc2_conv2': {
                'Détection Coins': np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]),
                'Emboss': np.array([[-2, -1, 0], [-1, 1, 1], [0, 1, 2]]),
            },
            'bloc3_conv1': {
                'Forme 1': np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]),
                'Motifs': np.array([[1, -1, 1], [-1, 0, -1], [1, -1, 1]]),
            },
            'bloc3_conv2': {
                'Contours Complexes': np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]),
                'Détection Crêtes': np.array([[0, -1, 0], [-1, 4, -1], [0, -1, 0]]),
            },
            'bloc4_conv1': {
                'Gradient Couleur': np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]]),
                'Détails Fins': np.array([[0, -1, 0], [-1, 6, -1], [0, -1, 0]]) / 2,
            }
        }
    
    def apply_filter(self, image, kernel):
        """Applique un filtre de convolution à une image"""
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image.copy()
        
        # Gérer les images RGB
        if len(img_array.shape) == 3:
            filtered_channels = []
            for channel in range(img_array.shape[2]):
                filtered_channel = cv2.filter2D(img_array[:,:,channel], -1, kernel)
                filtered_channels.append(filtered_channel)
            filtered_img = np.stack(filtered_channels, axis=2)
        else:
            filtered_img = cv2.filter2D(img_array, -1, kernel)
        
        # Normaliser
        filtered_img = np.clip(filtered_img, 0, 255)
        return filtered_img.astype(np.uint8)
    
    def simulate_pooling(self, image, pool_size=2):
        """Simule le max pooling"""
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        
        h, w = img_array.shape[:2]
        new_h, new_w = h // pool_size, w // pool_size
        
        return cv2.resize(img_array, (new_w, new_h))
    
    def visualize_bloc(self, image, bloc_number):
        """Visualise la transformation complète d'un bloc"""
        # Redimensionner l'image à 100x100
        if isinstance(image, Image.Image):
            img_resized = image.resize((100, 100))
            img_array = np.array(img_resized)
        else:
            img_array = cv2.resize(image, (100, 100))
        
        # Obtenir les filtres pour ce bloc
        conv1_key = f'bloc{bloc_number}_conv1'
        conv2_key = f'bloc{bloc_number}_conv2'
        
        conv1_filters = self.filter_examples.get(conv1_key, {})
        conv2_filters = self.filter_examples.get(conv2_key, {})
        
        results = {
            'input': img_array,
            'conv1_results': {},
            'conv2_results': {},
            'final_result': None
        }
        
        # Première convolution
        conv1_outputs = []
        for name, kernel in conv1_filters.items():
            filtered = self.apply_filter(img_array, kernel)
            results['conv1_results'][name] = filtered
            conv1_outputs.append(filtered)
        
        # Moyenne des sorties Conv1 pour l'entrée de Conv2
        if conv1_outputs:
            conv1_combined = np.mean(conv1_outputs, axis=0).astype(np.uint8)
        else:
            conv1_combined = img_array
        
        # Deuxième convolution
        conv2_outputs = []
        for name, kernel in conv2_filters.items():
            filtered = self.apply_filter(conv1_combined, kernel)
            results['conv2_results'][name] = filtered
            conv2_outputs.append(filtered)
        
        # Résultat final avec pooling (sauf bloc 4)
        if conv2_outputs:
            conv2_combined = np.mean(conv2_outputs, axis=0).astype(np.uint8)
            if bloc_number != 4:
                final_result = self.simulate_pooling(conv2_combined)
            else:
                final_result = conv2_combined
            results['final_result'] = final_result
        
        return results

def main():
    # Titre principal
    st.title("🔬 Test des Filtres CNN - EduFruit V3")
    st.markdown("---")
    st.markdown("**Testez les transformations de filtres avant intégration dans l'application principale**")
    
    # Sidebar pour les contrôles
    with st.sidebar:
        st.header("⚙️ Paramètres")
        
        # Sélection du bloc
        bloc_number = st.selectbox(
            "Choisir le bloc à tester:",
            [1, 2, 3, 4],
            format_func=lambda x: f"Bloc {x}"
        )
        
        # Options d'affichage
        show_kernels = st.checkbox("Afficher les noyaux de convolution", value=True)
        show_intermediate = st.checkbox("Afficher les résultats intermédiaires", value=True)
        
        st.markdown("---")
        st.markdown("### 📝 Infos du bloc")
        bloc_info = {
            1: "**Bloc 1:** Détection des contours\n- 2 Conv2D(32) + MaxPooling\n- Sortie: ~50×50×32",
            2: "**Bloc 2:** Textures et motifs\n- 2 Conv2D(64) + MaxPooling\n- Sortie: ~25×25×64", 
            3: "**Bloc 3:** Formes complexes\n- 2 Conv2D(128) + MaxPooling\n- Sortie: ~12×12×128",
            4: "**Bloc 4:** Couleurs spécialisées\n- 1 Conv2D(256), sans pooling\n- Sortie: ~7×7×256"
        }
        st.markdown(bloc_info[bloc_number])
    
    # Upload d'image
    st.header("📤 Upload d'image")
    uploaded_file = st.file_uploader(
        "Choisissez une image de fruit:",
        type=['jpg', 'jpeg', 'png'],
        help="Format recommandé: 100×100 pixels"
    )
    
    # Zone principale
    if uploaded_file is not None:
        # Charger l'image
        image = Image.open(uploaded_file)
        
        # Créer le testeur
        tester = SimpleFilterTester()
        
        # Obtenir les résultats
        results = tester.visualize_bloc(image, bloc_number)
        
        st.header(f"🔍 Résultats - Bloc {bloc_number}")
        
        # === TRANSFORMATION PRINCIPALE ===
        st.subheader("Transformation étape par étape")
        
        col1, col2, col3, col4, col5 = st.columns([2, 0.5, 2, 0.5, 2])
        
        with col1:
            st.markdown("**🖼️ Image d'entrée**")
            st.image(results['input'], width=150)
            st.caption(f"100×100×3")
        
        with col2:
            st.markdown("<div style='text-align:center; padding-top:60px; font-size:24px;'>→</div>", 
                       unsafe_allow_html=True)
        
        with col3:
            st.markdown("**🎯 Après Conv1**")
            if results['conv1_results']:
                # Afficher les résultats des 2 filtres
                filter_names = list(results['conv1_results'].keys())
                for i, (name, result) in enumerate(results['conv1_results'].items()):
                    st.image(result, width=70, caption=f"{name}")
                    if i >= 1:  # Limiter à 2 filtres
                        break
        
        with col4:
            st.markdown("<div style='text-align:center; padding-top:60px; font-size:24px;'>→</div>", 
                       unsafe_allow_html=True)
        
        with col5:
            st.markdown("**🏁 Résultat final**")
            if results['final_result'] is not None:
                st.image(results['final_result'], width=120)
                h, w = results['final_result'].shape[:2]
                
                # Dimensions selon le bloc
                dimensions = {
                    1: f"~{w}×{h}×32",
                    2: f"~{w}×{h}×64", 
                    3: f"~{w}×{h}×128",
                    4: f"~{w}×{h}×256"
                }
                st.caption(dimensions[bloc_number])
        
        # === RÉSULTATS INTERMÉDIAIRES ===
        if show_intermediate:
            st.subheader("🔬 Résultats intermédiaires détaillés")
            
            # Conv1
            st.markdown("**Première convolution (Conv1):**")
            if results['conv1_results']:
                cols = st.columns(len(results['conv1_results']))
                for i, (name, result) in enumerate(results['conv1_results'].items()):
                    with cols[i]:
                        st.image(result, caption=name, width=150)
            
            # Conv2
            st.markdown("**Deuxième convolution (Conv2):**")
            if results['conv2_results']:
                cols = st.columns(len(results['conv2_results']))
                for i, (name, result) in enumerate(results['conv2_results'].items()):
                    with cols[i]:
                        st.image(result, caption=name, width=150)
        
        # === NOYAUX DE CONVOLUTION ===
        if show_kernels:
            st.subheader("🧮 Noyaux de convolution utilisés")
            
            conv1_key = f'bloc{bloc_number}_conv1'
            conv2_key = f'bloc{bloc_number}_conv2'
            
            col_k1, col_k2 = st.columns(2)
            
            with col_k1:
                st.markdown("**Filtres Conv1:**")
                conv1_filters = tester.filter_examples.get(conv1_key, {})
                if conv1_filters:
                    fig, axes = plt.subplots(1, len(conv1_filters), figsize=(8, 3))
                    if len(conv1_filters) == 1:
                        axes = [axes]
                    
                    for i, (name, kernel) in enumerate(conv1_filters.items()):
                        im = axes[i].imshow(kernel, cmap='RdBu', vmin=-2, vmax=2)
                        axes[i].set_title(name, fontsize=10)
                        axes[i].axis('off')
                        
                        # Valeurs dans les cellules
                        for (j, k), val in np.ndenumerate(kernel):
                            axes[i].text(k, j, f'{val:.1f}', ha='center', va='center', 
                                       color='white' if abs(val) > 1 else 'black', fontsize=8)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
            
            with col_k2:
                st.markdown("**Filtres Conv2:**")
                conv2_filters = tester.filter_examples.get(conv2_key, {})
                if conv2_filters:
                    fig, axes = plt.subplots(1, len(conv2_filters), figsize=(8, 3))
                    if len(conv2_filters) == 1:
                        axes = [axes]
                    
                    for i, (name, kernel) in enumerate(conv2_filters.items()):
                        im = axes[i].imshow(kernel, cmap='RdBu', vmin=-2, vmax=2)
                        axes[i].set_title(name, fontsize=10)
                        axes[i].axis('off')
                        
                        # Valeurs dans les cellules
                        for (j, k), val in np.ndenumerate(kernel):
                            axes[i].text(k, j, f'{val:.1f}', ha='center', va='center', 
                                       color='white' if abs(val) > 1 else 'black', fontsize=8)
                    
                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close()
        
        # === CODE POUR INTÉGRATION ===
        with st.expander("💻 Code pour intégrer dans votre application"):
            st.code(f"""
# Dans votre bloc {bloc_number}, remplacez :
st.markdown("#### Visualisation du processus")
bloc{bloc_number}_fig = illustrations.get_bloc{bloc_number}_illustration()
st.plotly_chart(bloc{bloc_number}_fig, use_container_width=True)

# Par :
from cnn_filter_visualizer import add_filter_visualization_to_bloc

st.markdown("#### 🔍 Transformation avec filtres réels")
if current_image is not None:
    add_filter_visualization_to_bloc(current_image, {bloc_number}, explorer.model)
else:
    st.info("Uploadez une image pour voir les transformations")
""", language='python')
    
    else:
        # État initial
        st.info("👆 Uploadez une image de fruit pour voir les transformations par les filtres CNN")
        
        # Exemple visuel
        st.subheader("📖 Comment ça fonctionne")
        st.markdown("""
        **Chaque bloc applique :**
        1. **Première convolution** avec 2 filtres différents
        2. **Deuxième convolution** avec 2 autres filtres  
        3. **Max Pooling** pour réduire la taille (sauf Bloc 4)
        
        **Visualisation :** `Image → Conv1 → Conv2 → Résultat`
        """)
    
    # Footer
    st.markdown("---")
    st.markdown("🎯 **Testez différents blocs et images pour voir comment les filtres transforment vos données !**")

if __name__ == "__main__":
    main()