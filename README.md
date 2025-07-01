# 🍎 EduFruit V3 - Classification de Fruits Éducative



## 🎯 Description

EduFruit V3 est un système intelligent de classification de fruits développé dans un contexte éducatif. Utilisant l'apprentissage profond avec TensorFlow, ce projet offre une solution complète avec un modèle CNN de bonne performaance et une interface web interactive construite avec Streamlit.

Le projet combine :
- 🧠 **Modélisation CNN robuste** avec TensorFlow/Keras
- 🎨 **Interface pédagogique interactive** avec Streamlit
- 📊 **Visualisation des couches internes** du réseau
- 🔍 **Approche scientifique** avec validation externe

## 🚀 Démonstration en ligne

**[🔗 Essayer l'application](https://edufruitsv3-fgwb3rbfajrpqeoc3vaftc.streamlit.app)**

## ✨ Fonctionnalités

- **Classification en temps réel** d'images de fruits
- **Visualisation couche par couche** du processus CNN
- **Interface pédagogique** avec explications intégrées
- **Tests de robustesse** sur images réelles et synthétiques
- **Analyse des performances** avec métriques détaillées

## 🎯 Performances du modèle

| Métrique | Score |
|----------|-------|
| Précision globale | 93.2% |
| Précision validation | 98.2% |
| Classes supportées | 5 fruits |
| Paramètres | ~846,000 |
| Taille du modèle | 3.5 MB |

## 🚀 Installation

```bash


# 2. Créer l'environnement virtuel
python -m venv edufruits_env

# 3. Activer l'environnement
# Windows
edufruits_env\Scripts\activate
# Linux/Mac
source edufruits_env/bin/activate

# 4. Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# 5. Vérifier l'installation
python verify_environment.py
```

## 🏃‍♂️ Utilisation

### Interface Web Streamlit

```bash
# Lancer l'application web interactive
streamlit run app.py
```

### Tests effectués
- ✅ **Images réelles** (smartphone, conditions variées)
- ✅ **Images synthétiques** (test de biais couleur)
- ✅ **Images bruitées** (robustesse)
- ✅ **Validation croisée** train/test stricte

### Cas d'usage typiques
- 🍌 **Bananes :** Très haute précision (>95%)
- 🍎 **Pommes :** Bonne reconnaissance toutes variétés
- 🥒 **Concombres :** Sensible au cadrage et orientation
- 🍋 **Citrons :** Parfois confondus avec bananes si allongés

## 📜 Évolution du projet

### Version 3.0 (Actuelle)
- ✅ Architecture CNN optimisée
- ✅ Interface Streamlit complète
- ✅ Validation externe robuste
- ✅ Documentation pédagogique

### Futures améliorations
- 🔄 Visualisation Grad-CAM
- 📱 Version mobile native
- 🌐 Déploiement TensorFlow.js
- 📈 Apprentissage continu


## 👥 Auteurs

- **Mamadou Fall** - *Développement initial* - [Mamdou025](https://github.com/Mamdou025)

## 📞 Support

- **Issues GitHub** : [Signaler un problème](https://github.com/Mamdou025/Edufruits_V3/issues)
- **Email** : fallmamadou151@gmail.com

---

*Développé  pour l'éducation en intelligence artificielle*