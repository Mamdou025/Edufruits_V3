#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
architecture_modular.py - Architecture EduFruit V3 avec méthode colonnes
Chaque élément est créé séparément puis assemblé avec des colonnes Streamlit
"""

import plotly.graph_objects as go
import streamlit as st

def create_input_image():
    """Crée l'illustration de l'image d'entrée 100×100×3"""
    fig = go.Figure()
    
    # Rectangle principal (représente l'image)
    fig.add_shape(
        type="rect", 
        x0=0.1, y0=0.1, x1=0.9, y1=0.9,
        fillcolor="rgba(173, 216, 230, 0.8)",  # Bleu clair
        line=dict(color="black", width=2)
    )
    
    # Grille pour représenter les pixels
    grid_size = 6
    for i in range(grid_size):
        for j in range(grid_size):
            fig.add_shape(
                type="rect",
                x0=0.15 + i * 0.7/grid_size,
                y0=0.15 + j * 0.7/grid_size,
                x1=0.15 + (i + 1) * 0.7/grid_size,
                y1=0.15 + (j + 1) * 0.7/grid_size,
                fillcolor="rgba(255, 255, 255, 0.3)",
                line=dict(color="gray", width=0.5)
            )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        height=140,
        margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_bloc_stack(color, num_rects=4):
    """Crée un stack de rectangles pour représenter les feature maps"""
    fig = go.Figure()
    
    for i in range(num_rects):
        fig.add_shape(
            type="rect",
            x0=0.1 + i * 0.08,
            y0=0.1 + i * 0.08,
            x1=0.7 + i * 0.08,
            y1=0.7 + i * 0.08,
            fillcolor=color,
            line=dict(width=0)  # Pas de bordure pour éviter les triangles
        )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        height=140,
        margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_gap_illustration():
    """Crée l'illustration du Global Average Pooling"""
    fig = go.Figure()
    
    # Cercles représentant les 256 valeurs
    for i in range(12):
        fig.add_shape(
            type="circle",
            x0=0.4, y0=0.05 + i * 0.08,
            x1=0.6, y1=0.25 + i * 0.08,
            fillcolor="#9333ea",
            line=dict(width=0)
        )
    
    # Points de suspension
    fig.add_annotation(
        x=0.5, y=0.85, text="⋮", 
        showarrow=False, 
        font=dict(size=20, color="#9333ea")
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        height=140,
        margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_neural_network():
    """Crée l'illustration du réseau de neurones dense"""
    fig = go.Figure()
    
    # Neurones d'entrée (gauche)
    for i in range(6):
        fig.add_shape(
            type="circle",
            x0=0.1, y0=0.1 + i * 0.13,
            x1=0.2, y1=0.2 + i * 0.13,
            fillcolor="#9333ea",
            line=dict(color="black", width=1)
        )
    
    # Neurones de sortie (droite) - 5 fruits
    fruit_colors = ["#ef4444", "#f97316", "#eab308", "#84cc16", "#8b5cf6"]
    for i, color in enumerate(fruit_colors):
        fig.add_shape(
            type="circle",
            x0=0.7, y0=0.15 + i * 0.15,
            x1=0.8, y1=0.25 + i * 0.15,
            fillcolor=color,
            line=dict(color="black", width=1)
        )
    
    # Connexions (quelques exemples)
    connections = [
        (0.2, 0.15, 0.7, 0.2),
        (0.2, 0.28, 0.7, 0.35),
        (0.2, 0.41, 0.7, 0.5),
        (0.2, 0.54, 0.7, 0.65),
        (0.2, 0.67, 0.7, 0.8)
    ]
    
    for x0, y0, x1, y1 in connections:
        fig.add_shape(
            type="line",
            x0=x0, y0=y0, x1=x1, y1=y1,
            line=dict(color="rgba(99, 102, 241, 0.4)", width=1)
        )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        height=140,
        margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_predictions_bars():
    """Crée les barres de prédictions finales"""
    fig = go.Figure()
    
    fruits = ["Pomme", "Orange", "Banane", "Avocat", "Citron"]
    probabilities = [82, 12, 4, 1, 1]
    colors = ["#ef4444", "#f97316", "#eab308", "#84cc16", "#8b5cf6"]
    
    for i, (fruit, prob, color) in enumerate(zip(fruits, probabilities, colors)):
        # Barre de probabilité
        fig.add_shape(
            type="rect",
            x0=0.1, y0=0.8 - i * 0.18,
            x1=0.1 + prob * 0.008, y1=0.9 - i * 0.18,
            fillcolor=color,
            line=dict(width=0)
        )
        
        # Texte du fruit et pourcentage
        fig.add_annotation(
            x=0.05, y=0.85 - i * 0.18,
            text=fruit,
            showarrow=False,
            font=dict(size=9, color="#374151"),
            xanchor="right"
        )
        
        fig.add_annotation(
            x=0.95, y=0.85 - i * 0.18,
            text=f"{prob}%",
            showarrow=False,
            font=dict(size=9, color="#374151"),
            xanchor="left"
        )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        height=140,
        margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def create_arrow():
    """Crée une flèche simple"""
    fig = go.Figure()
    
    fig.add_annotation(
        x=0.5, y=0.5,
        text="→",
        showarrow=False,
        font=dict(size=24, color="black")
    )
    
    fig.update_layout(
        showlegend=False,
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        height=80,
        margin=dict(l=5, r=5, t=5, b=5),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    return fig

def display_modular_architecture():
    """
    Affiche l'architecture complète avec la méthode colonnes modulaire
    """
    st.markdown("---")
    st.markdown("### 📋 EduFruit V3 - Architecture Complète du Réseau de Neurones")
    st.markdown("*Vue d'ensemble modulaire du processus complet*")
    
    # === PREMIÈRE LIGNE : ILLUSTRATIONS ===
    cols = st.columns([1.2, 0.3, 1.5, 0.3, 1.5, 0.3, 1.5, 0.3, 1.5, 0.3, 1.2, 0.3, 1.8, 0.3, 2.0])
    
    with cols[0]:  # Image d'entrée
        fig_image = create_input_image()
        st.plotly_chart(fig_image, use_container_width=True, key="input_img")
    
    with cols[1]:  # Flèche 1
        fig_arrow1 = create_arrow()
        st.plotly_chart(fig_arrow1, use_container_width=True, key="arrow1")
    
    with cols[2]:  # Bloc 1
        fig_bloc1 = create_bloc_stack("rgba(34, 197, 94, 0.8)")
        st.plotly_chart(fig_bloc1, use_container_width=True, key="bloc1")
    
    with cols[3]:  # Flèche 2
        fig_arrow2 = create_arrow()
        st.plotly_chart(fig_arrow2, use_container_width=True, key="arrow2")
    
    with cols[4]:  # Bloc 2
        fig_bloc2 = create_bloc_stack("rgba(168, 85, 247, 0.8)")
        st.plotly_chart(fig_bloc2, use_container_width=True, key="bloc2")
    
    with cols[5]:  # Flèche 3
        fig_arrow3 = create_arrow()
        st.plotly_chart(fig_arrow3, use_container_width=True, key="arrow3")
    
    with cols[6]:  # Bloc 3
        fig_bloc3 = create_bloc_stack("rgba(251, 146, 60, 0.8)")
        st.plotly_chart(fig_bloc3, use_container_width=True, key="bloc3")
    
    with cols[7]:  # Flèche 4
        fig_arrow4 = create_arrow()
        st.plotly_chart(fig_arrow4, use_container_width=True, key="arrow4")
    
    with cols[8]:  # Bloc 4
        fig_bloc4 = create_bloc_stack("rgba(248, 113, 113, 0.8)")
        st.plotly_chart(fig_bloc4, use_container_width=True, key="bloc4")
    
    with cols[9]:  # Flèche 5
        fig_arrow5 = create_arrow()
        st.plotly_chart(fig_arrow5, use_container_width=True, key="arrow5")
    
    with cols[10]:  # GAP
        fig_gap = create_gap_illustration()
        st.plotly_chart(fig_gap, use_container_width=True, key="gap")
    
    with cols[11]:  # Flèche 6
        fig_arrow6 = create_arrow()
        st.plotly_chart(fig_arrow6, use_container_width=True, key="arrow6")
    
    with cols[12]:  # Réseau neuronal
        fig_network = create_neural_network()
        st.plotly_chart(fig_network, use_container_width=True, key="network")
    
    with cols[13]:  # Flèche 7
        fig_arrow7 = create_arrow()
        st.plotly_chart(fig_arrow7, use_container_width=True, key="arrow7")
    
    with cols[14]:  # Prédictions
        fig_predictions = create_predictions_bars()
        st.plotly_chart(fig_predictions, use_container_width=True, key="predictions")
    
    # === DEUXIÈME LIGNE : TITRES ===
    st.markdown("<br>", unsafe_allow_html=True)
    cols_titles = st.columns([1.2, 0.3, 1.5, 0.3, 1.5, 0.3, 1.5, 0.3, 1.5, 0.3, 1.2, 0.3, 1.8, 0.3, 2.0])
    
    titles = [
        ("Image", "#374151"),
        ("", ""),
        ("Bloc 1", "#22c55e"), 
        ("", ""),
        ("Bloc 2", "#a855f7"),
        ("", ""),
        ("Bloc 3", "#fb923c"),
        ("", ""),
        ("Bloc 4", "#f87171"),
        ("", ""),
        ("Moyenne Globale", "#9333ea"),
        ("", ""),
        ("Couche Dense", "#6366f1"),
        ("", ""),
        ("Prédictions de Sortie", "#374151")
    ]
    
    for i, (title, color) in enumerate(titles):
        if i < len(cols_titles) and title:
            with cols_titles[i]:
                st.markdown(f"<div style='text-align:center; font-weight:bold; color:{color}'>{title}</div>", 
                           unsafe_allow_html=True)
    
    # === TROISIÈME LIGNE : DÉTAILS TECHNIQUES ===
    st.markdown("<br>", unsafe_allow_html=True)
    cols_details = st.columns([1.2, 0.3, 1.5, 0.3, 1.5, 0.3, 1.5, 0.3, 1.5, 0.3, 1.2, 0.3, 1.8, 0.3, 2.0])
    
    details = [
        "100×100×3",
        "",
        "Convolution + ReLU<br>32 filtres<br>50×50×32",
        "",
        "Convolution + ReLU<br>64 filtres<br>25×25×64", 
        "",
        "Convolution + ReLU<br>128 filtres<br>12×12×128",
        "",
        "Convolution + ReLU<br>256 filtres<br>12×12×256",
        "",
        "Global Average<br>Pooling<br>256 valeurs",
        "",
        "Entièrement<br>Connectée<br>256 → 5 + Softmax",
        "",
        "5 classes<br>Probabilités<br>Somme = 100%"
    ]
    
    for i, detail in enumerate(details):
        if i < len(cols_details) and detail:
            with cols_details[i]:
                st.markdown(f"<div style='text-align:center; font-size:11px; color:#6b7280'>{detail}</div>", 
                           unsafe_allow_html=True)
    
    # === SECTIONS AVEC ACCOLADES ===
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col_section1, col_section2 = st.columns([6, 4])
    
    with col_section1:
        st.markdown("""
        <div style="text-align:center; padding:10px; border:2px solid #0ea5e9; border-radius:8px; background:#eff6ff;">
            <strong style="color:#0ea5e9; font-size:14px;">🔍 Extraction de Caractéristiques de l'Image</strong><br>
            <span style="color:#1e40af; font-size:12px;">Analyse progressive : contours → textures → formes → couleurs</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col_section2:
        st.markdown("""
        <div style="text-align:center; padding:10px; border:2px solid #0ea5e9; border-radius:8px; background:#eff6ff;">
            <strong style="color:#0ea5e9; font-size:14px;">🎯 Classification</strong><br>
            <span style="color:#1e40af; font-size:12px;">Décision finale avec probabilités</span>
        </div>
        """, unsafe_allow_html=True)
    
    # === RÉSUMÉ FINAL ===
    st.markdown("""
    <div style="background-color: #f8fafc; padding: 16px; border-radius: 8px; margin-top: 20px;">
        <h4 style="color: #374151; margin-bottom: 8px;">🧠 Résumé du processus :</h4>
        <p style="color: #6b7280; margin: 0; text-align: justify;">
            L'image passe par 4 blocs convolutionnels qui extraient progressivement des caractéristiques 
            (contours → textures → formes → couleurs), puis la Moyenne Globale compresse ces 
            informations en 256 valeurs numériques, et finalement la couche dense + Softmax 
            produit les probabilités finales pour chaque fruit.
        </p>
    </div>
    """, unsafe_allow_html=True)