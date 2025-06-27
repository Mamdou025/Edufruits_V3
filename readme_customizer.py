#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
README Customization Helper
Helps you customize the README template with your specific project details
"""

import os
import json
from pathlib import Path
from datetime import datetime

class ReadmeCustomizer:
    def __init__(self):
        """Initialize README customizer"""
        self.project_root = Path(".")
        self.project_details = {}
        
        print("📝 EduFruit README Customization Helper")
        print("🎯 This will help you personalize your README")
    
    def gather_project_info(self):
        """Gather project-specific information"""
        print("\n📊 Gathering project information...")
        
        # Find Streamlit files
        streamlit_files = []
        for file_path in self.project_root.rglob("*.py"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'streamlit' in content.lower():
                    streamlit_files.append(file_path.relative_to(self.project_root))
            except:
                continue
        
        # Find model files
        model_files = list(self.project_root.glob("models/*.h5"))
        if not model_files:
            model_files = list(self.project_root.glob("*.h5"))
        
        # Get latest model
        latest_model = None
        if model_files:
            latest_model = max(model_files, key=lambda f: f.stat().st_mtime)
            latest_model = latest_model.relative_to(self.project_root)
        
        # Find git repository info
        git_remote = None
        try:
            import subprocess
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                git_remote = result.stdout.strip()
        except:
            pass
        
        self.project_details = {
            'streamlit_files': streamlit_files,
            'main_streamlit_file': streamlit_files[0] if streamlit_files else None,
            'latest_model': latest_model,
            'git_remote': git_remote,
            'project_size': self._get_project_size()
        }
        
        return self.project_details
    
    def _get_project_size(self):
        """Calculate project size"""
        total_size = 0
        for file_path in self.project_root.rglob("*"):
            if file_path.is_file():
                try:
                    total_size += file_path.stat().st_size
                except:
                    continue
        
        return total_size / (1024 * 1024)  # MB
    
    def interactive_customization(self):
        """Interactive customization process"""
        print("\n🎨 Let's customize your README!")
        print("Press Enter to keep default values in brackets")
        
        customizations = {}
        
        # GitHub username
        default_username = "your-username"
        if self.project_details.get('git_remote'):
            # Try to extract username from git remote
            remote = self.project_details['git_remote']
            if 'github.com' in remote:
                parts = remote.split('/')
                if len(parts) >= 2:
                    default_username = parts[-2].split(':')[-1]
        
        username = input(f"\n👤 GitHub username [{default_username}]: ").strip()
        customizations['github_username'] = username or default_username
        
        # Repository name
        default_repo = "edufruit-v3"
        repo_name = input(f"📂 Repository name [{default_repo}]: ").strip()
        customizations['repo_name'] = repo_name or default_repo
        
        # Your name
        your_name = input(f"👨‍💻 Your name [Your Name]: ").strip()
        customizations['author_name'] = your_name or "Your Name"
        
        # Email
        email = input(f"📧 Your email [your.email@example.com]: ").strip()
        customizations['email'] = email or "your.email@example.com"
        
        # Streamlit main file
        if self.project_details.get('main_streamlit_file'):
            default_streamlit = str(self.project_details['main_streamlit_file'])
            streamlit_file = input(f"🌐 Main Streamlit file [{default_streamlit}]: ").strip()
            customizations['streamlit_main'] = streamlit_file or default_streamlit
        else:
            streamlit_file = input(f"🌐 Main Streamlit file [main.py]: ").strip()
            customizations['streamlit_main'] = streamlit_file or "main.py"
        
        # Model file
        if self.project_details.get('latest_model'):
            default_model = str(self.project_details['latest_model'])
            model_file = input(f"🧠 Model file [{default_model}]: ").strip()
            customizations['model_file'] = model_file or default_model
        else:
            model_file = input(f"🧠 Model file [models/edufruit_final_YYYYMMDD_HHMMSS.h5]: ").strip()
            customizations['model_file'] = model_file or "models/edufruit_final_YYYYMMDD_HHMMSS.h5"
        
        # Project description
        description = input(f"📝 Short project description [Press Enter for default]: ").strip()
        if description:
            customizations['description'] = description
        
        return customizations
    
    def customize_readme(self, customizations):
        """Apply customizations to README"""
        print("\n🔧 Applying customizations...")
        
        # Read the template README
        readme_content = """# 🍎 EduFruit V3 - Classification de Fruits Éducative

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10%2B-orange)](https://tensorflow.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.20%2B-red)](https://streamlit.io)
[![Accuracy](https://img.shields.io/badge/Accuracy-99.6%25-brightgreen)](#-performance)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Description

EduFruit V3 est un système intelligent de classification de fruits développé dans un contexte éducatif. Utilisant l'apprentissage profond avec TensorFlow, ce projet offre une solution complète avec un modèle CNN haute performance (99,6% de précision) et une interface web interactive construite avec Streamlit.

{custom_description}

## 🚀 Installation

```bash
# 1. Cloner le repository
git clone https://github.com/{github_username}/{repo_name}.git
cd {repo_name}

# 2. Créer l'environnement virtuel
python -m venv edufruit_env

# 3. Activer l'environnement
# Windows
edufruit_env\\Scripts\\activate
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
streamlit run {streamlit_main}
```

### Utilisation Programmatique

```python
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image

# Charger le modèle
model = load_model('{model_file}')

# Préparer l'image
img = Image.open('votre_image.jpg').resize((100, 100))
img_array = np.array(img) / 255.0
img_array = np.expand_dims(img_array, axis=0)

# Prédiction
prediction = model.predict(img_array)
classes = ['Pomme', 'Banane', 'Avocat', 'Concombre', 'Citron']
predicted_class = classes[np.argmax(prediction)]
confidence = np.max(prediction) * 100

print(f"Prédiction: {{predicted_class}} ({{confidence:.2f}}%)")
```

## 👥 Auteurs

- **{author_name}** - *Développement initial* - [{github_username}](https://github.com/{github_username})

## 📞 Support

- **Issues GitHub** : [Signaler un problème](https://github.com/{github_username}/{repo_name}/issues)
- **Email** : {email}
- **Documentation** : [Wiki du projet](https://github.com/{github_username}/{repo_name}/wiki)

---

*Développé avec ❤️ pour l'éducation en intelligence artificielle*"""
        
        # Apply customizations
        custom_description = ""
        if 'description' in customizations:
            custom_description = f"\n**Description personnalisée :** {customizations['description']}\n"
        
        readme_content = readme_content.format(
            github_username=customizations['github_username'],
            repo_name=customizations['repo_name'],
            author_name=customizations['author_name'],
            email=customizations['email'],
            streamlit_main=customizations['streamlit_main'],
            model_file=customizations['model_file'],
            custom_description=custom_description
        )
        
        return readme_content
    
    def save_customized_readme(self, content):
        """Save the customized README"""
        readme_path = self.project_root / "README.md"
        
        # Backup existing README if it exists
        if readme_path.exists():
            backup_path = self.project_root / f"README_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
            readme_path.rename(backup_path)
            print(f"📄 Existing README backed up to: {backup_path}")
        
        # Save new README
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Customized README saved to: {readme_path}")
        return readme_path
    
    def generate_additional_files(self, customizations):
        """Generate additional helpful files"""
        print("\n📦 Generating additional files...")
        
        # Create a simple LICENSE file
        license_content = f"""MIT License

Copyright (c) {datetime.now().year} {customizations['author_name']}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""
        
        license_path = self.project_root / "LICENSE"
        if not license_path.exists():
            with open(license_path, 'w') as f:
                f.write(license_content)
            print(f"📄 LICENSE file created")
        
        # Create .gitignore if it doesn't exist
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
edufruit_env/

# Data
data/raw/
*.zip
*.tar.gz

# Models (optional - comment out if you want to version models)
# models/*.h5

# Outputs
outputs/
*.log

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Streamlit
.streamlit/

# Jupyter
.ipynb_checkpoints/"""
        
        gitignore_path = self.project_root / ".gitignore"
        if not gitignore_path.exists():
            with open(gitignore_path, 'w') as f:
                f.write(gitignore_content)
            print(f"📄 .gitignore file created")
    
    def print_next_steps(self, customizations):
        """Print next steps for the user"""
        print("\n" + "="*60)
        print("🎉 README CUSTOMIZATION COMPLETE!")
        print("="*60)
        
        print(f"\n✅ Files created/updated:")
        print(f"   📄 README.md - Your customized project README")
        print(f"   📄 LICENSE - MIT License with your name")
        print(f"   📄 .gitignore - Standard Python/ML gitignore")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Review and edit README.md as needed")
        print(f"   2. Add screenshots of your Streamlit app")
        print(f"   3. Update performance metrics with your actual results")
        print(f"   4. Test your installation instructions")
        print(f"   5. Commit and push to GitHub:")
        
        print(f"\n💻 Git commands:")
        print(f"   git add .")
        print(f"   git commit -m 'Add comprehensive project documentation'")
        print(f"   git push origin main")
        
        if customizations['github_username'] != 'your-username':
            repo_url = f"https://github.com/{customizations['github_username']}/{customizations['repo_name']}"
            print(f"\n🌐 Your project will be available at:")
            print(f"   {repo_url}")

def main():
    """Main customization function"""
    print("📝" * 20)
    print("📝 EDUFRUIT README CUSTOMIZER")
    print("📝" * 20)
    
    customizer = ReadmeCustomizer()
    
    # Gather project info
    project_info = customizer.gather_project_info()
    
    # Interactive customization
    customizations = customizer.interactive_customization()
    
    # Generate customized README
    readme_content = customizer.customize_readme(customizations)
    
    # Save README
    customizer.save_customized_readme(readme_content)
    
    # Generate additional files
    customizer.generate_additional_files(customizations)
    
    # Print next steps
    customizer.print_next_steps(customizations)

if __name__ == "__main__":
    main()