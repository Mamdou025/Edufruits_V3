# 🍎 EduFruit V3 - Classification de Fruits Éducative

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10%2B-orange)](https://tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-red)](https://streamlit.io)
[![Accuracy](https://img.shields.io/badge/Accuracy-99.6%25-brightgreen)](#-performance)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Description

EduFruit V3 est un système intelligent de classification de fruits développé dans un contexte éducatif. Utilisant l'apprentissage profond avec TensorFlow, ce projet offre une solution complète avec un modèle CNN haute performance (99,6% de précision) et une interface web interactive construite avec Streamlit.



## 🚀 Installation

```bash


# 2. Créer l'environnement virtuel
python -m venv edufruistv3_env

# 3. Activer l'environnement
# Windows
edufruistv3_env\Scripts\activate
# Linux/Mac
source edufruit_env/bin/activate

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

### Utilisation Programmatique

```python
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Charger le modèle
model = load_model('models\edufruit_best_20250622_224456.h5')

# Préparer l'image
img = Image.open('votre_image.jpg').resize((100, 100))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Prédiction
prediction = model.predict(img_array)
classes = ['Pomme', 'Banane', 'Avocat', 'Concombre', 'Citron']
predicted_class = classes[np.argmax(prediction)]
confidence = np.max(prediction) * 100

print(f"Prédiction: {predicted_class} ({confidence:.2f}%)")
```

## 👥 Auteurs

- **Mamadou Fall** - *Développement initial* - [Mamdou025](https://github.com/Mamdou025)

## 📞 Support

- **Issues GitHub** : [Signaler un problème](https://github.com/Mamdou025/Edufruits_V3/issues)
- **Email** : fallmamadou151@gmail.com
- **Documentation** : [Wiki du projet](https://github.com/Mamdou025/Edufruits_V3/wiki)

---

*Développé avec ❤️ pour l'éducation en intelligence artificielle*