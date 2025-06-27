"""
css_loader.py - Utilitaire pour charger les styles CSS (version silencieuse)
"""

import streamlit as st
from pathlib import Path

def load_css(css_file_path):
    """
    Charge un fichier CSS et l'applique à la page Streamlit
    
    Args:
        css_file_path (str ou Path): Chemin vers le fichier CSS
    """
    try:
        css_path = Path(css_file_path)
        
        if not css_path.exists():
            # Supprimé: st.warning(f"⚠️ Fichier CSS non trouvé: {css_path}")
            return False
        
        with open(css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()
        
        st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
        return True
        
    except Exception as e:
        # Supprimé: st.error(f"❌ Erreur lors du chargement du CSS: {e}")
        return False

def get_css_path():
    """
    Obtient le chemin vers le fichier CSS dans le dossier streamlit
    """
    # Obtenir le dossier du script actuel
    if '__file__' in globals():
        current_dir = Path(__file__).parent
    else:
        current_dir = Path.cwd()
    
    # Chercher le fichier CSS
    css_file = current_dir / "styles.css"
    
    # Si pas trouvé, chercher dans le dossier parent
    if not css_file.exists():
        css_file = current_dir.parent / "streamlit" / "styles.css"
    
    return css_file

def apply_custom_styles():
    """
    Applique les styles personnalisés à l'application (mode silencieux)
    """
    css_path = get_css_path()
    
    if load_css(css_path):
        
        pass  # CSS chargé en silence
    else:
        # CSS de fallback si le fichier n'est pas trouvé
        fallback_css = """
        <style>
        .main {
            background-color: #FEFEFE;
            font-family: 'Times New Roman', serif;
            color: #000000;
        }
        .title-container {
            background-color: white;
            padding: 20px;
            border: 2px solid #333;
            margin-bottom: 20px;
            text-align: center;
            color: #000000;
            border-radius: 10px;
        }
        .step-container {
            background-color: white;
            border: 1px solid #333;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            color: #000000;
        }
        </style>
        """
        st.markdown(fallback_css, unsafe_allow_html=True)
        # Supprimé: st.info("ℹ️ Styles CSS de base appliqués")