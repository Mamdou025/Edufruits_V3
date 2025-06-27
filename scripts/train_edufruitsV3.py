#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Entraînement EduFruit V3 - Version de production
Copie de votre classe EduFruisV3Fixed avec améliorations
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Conv2D, MaxPooling2D, Dropout, Flatten, Dense, 
    BatchNormalization, GlobalAveragePooling2D
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.callbacks import (
    ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TensorBoard
)
from tensorflow.keras.regularizers import l2
import numpy as np
import matplotlib.pyplot as plt
import os
import shutil
from datetime import datetime
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
import json


class EduFruitTrainer:
    def __init__(self):
        """Initialiser EduFruit V3"""
        self.classes = ['Pomme', 'Banane', 'Avocat', 'Concombre', 'Citron']
        self.num_classes = len(self.classes)
        self.img_size = (100, 100)
        self.history = None
        
        # Mapping des classes (de votre code original)
        self.class_mappings_v3 = {
            'Pomme': [
                'Apple Red 1',
                'Apple Golden 2', 
                'Apple Braeburn 1',
                'Apple Granny Smith 1'
            ],
            'Banane': [
                'Banana 1',
                'Banana 3', 
                'Banana 4',
                'Banana Lady Finger 1'
            ],
            'Avocat': [
                'Avocado 1',
                'Avocado Black 1',
                'Avocado Green 1',
                'Avocado ripe 1'
            ],
            'Concombre': [
                'Cucumber 11',
                'Cucumber 1',
                'Cucumber 4',
                'Cucumber 3'
            ],
            'Citron': [
                'Lemon 1',
                'Lemon Meyer 1'
            ]
        }
        
        # Créer les dossiers nécessaires
        os.makedirs('models', exist_ok=True)
        os.makedirs('outputs/logs', exist_ok=True)
        os.makedirs('outputs/plots', exist_ok=True)
        os.makedirs('data/processed', exist_ok=True)
        
        print("🚀 EduFruit V3 Trainer initialisé")
        print(f"✅ Classes finales: {self.classes}")

    def create_unified_dataset(self, source_dir="data/raw/fruits-360", target_dir="data/processed/edufruit_dataset"):
        """Créer le dataset unifié en regroupant les variétés par classe"""
        
        print("\n🔄 CRÉATION DU DATASET UNIFIÉ")
        print("="*50)
        
        # Vérifier que les données sources existent
        if not os.path.exists(source_dir):
            raise FileNotFoundError(f"Données sources non trouvées: {source_dir}")
        
        # Nettoyer le dossier cible
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        
        os.makedirs(f"{target_dir}/Training", exist_ok=True)
        os.makedirs(f"{target_dir}/Test", exist_ok=True)
        
        stats = {}
        
        for split in ['Training', 'Test']:
            print(f"\n📁 Traitement {split}:")
            split_stats = {}
            
            for class_name, source_folders in self.class_mappings_v3.items():
                # Créer le dossier de classe unifié
                target_class_dir = os.path.join(target_dir, split, class_name)
                os.makedirs(target_class_dir, exist_ok=True)
                
                total_images = 0
                print(f"   🍎 {class_name}:")
                
                for source_folder in source_folders:
                    source_path = os.path.join(source_dir, split, source_folder)
                    
                    if os.path.exists(source_path):
                        # Copier toutes les images de ce dossier vers le dossier unifié
                        images = [f for f in os.listdir(source_path) if f.endswith('.jpg')]
                        
                        for image_file in images:
                            source_image = os.path.join(source_path, image_file)
                            # Renommer pour éviter les conflits
                            new_name = f"{source_folder}_{image_file}"
                            target_image = os.path.join(target_class_dir, new_name)
                            shutil.copy2(source_image, target_image)
                            total_images += 1
                        
                        print(f"      ✅ {source_folder}: {len(images)} images")
                    else:
                        print(f"      ❌ {source_folder}: Non trouvé")
                
                split_stats[class_name] = total_images
                print(f"      📊 Total {class_name}: {total_images} images")
            
            stats[split] = split_stats
        
        print(f"\n✅ Dataset unifié créé dans: {target_dir}")
        return stats

    def create_model(self):
        """Créer le modèle CNN EduFruit"""
        
        model = Sequential([
            # Bloc 1
            Conv2D(32, (3, 3), activation='relu', input_shape=(100, 100, 3), 
                   kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Bloc 2
            Conv2D(64, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Bloc 3
            Conv2D(128, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Bloc 4
            Conv2D(256, (3, 3), activation='relu', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Dropout(0.25),
            
            # Global Average Pooling
            GlobalAveragePooling2D(),
            
            # Couches denses
            Dense(512, activation='relu', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Dropout(0.5),
            
            Dense(256, activation='relu', kernel_regularizer=l2(0.001)),
            BatchNormalization(),
            Dropout(0.5),
            
            # Sortie pour 5 classes
            Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        self.model = model
        print("✅ Modèle CNN créé")
        return model

    def create_data_generators(self):
        """Créer les générateurs de données avec augmentation"""
        
        train_datagen = ImageDataGenerator(
            rescale=1./255,
            rotation_range=40,
            width_shift_range=0.3,
            height_shift_range=0.3,
            shear_range=0.3,
            zoom_range=0.3,
            horizontal_flip=True,
            vertical_flip=True,
            brightness_range=[0.4, 1.6],
            channel_shift_range=0.2,
            fill_mode='nearest'
        )
        
        val_datagen = ImageDataGenerator(rescale=1./255)
        
        return train_datagen, val_datagen

    def calculate_class_weights(self):
        """Calculer les poids de classe pour corriger le déséquilibre"""
        
        # Estimation basée sur votre analyse
        real_counts = {
            0: 1968,  # Pomme
            1: 1427,  # Banane  
            2: 2627,  # Avocat
            3: 856,   # Concombre
            4: 982    # Citron
        }
        
        # Calculer les poids (inverse de la fréquence)
        max_count = max(real_counts.values())
        class_weights = {}
        
        for class_idx, count in real_counts.items():
            weight = max_count / count
            class_weights[class_idx] = weight
        
        print("⚖️  Poids de classe calculés:")
        for i, class_name in enumerate(self.classes):
            print(f"   {class_name}: {class_weights[i]:.2f}")
        
        return class_weights

    def train_model(self, data_dir="data/processed/edufruit_dataset", epochs=50, batch_size=32):
        """Entraîner le modèle"""
        
        print("\n🚀 DÉBUT DE L'ENTRAÎNEMENT")
        print("="*60)
        
        # Vérifier que le dataset unifié existe
        if not os.path.exists(data_dir):
            print("📁 Dataset unifié non trouvé, création en cours...")
            self.create_unified_dataset()
        
        # Créer le modèle
        if not hasattr(self, 'model'):
            self.create_model()
        
        # Générateurs
        train_datagen, val_datagen = self.create_data_generators()
        
        # Flow generators
        train_generator = train_datagen.flow_from_directory(
            os.path.join(data_dir, "Training"),
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            classes=self.classes,
            shuffle=True
        )
        
        validation_generator = val_datagen.flow_from_directory(
            os.path.join(data_dir, "Test"),
            target_size=self.img_size,
            batch_size=batch_size,
            class_mode='categorical',
            classes=self.classes,
            shuffle=True
        )
        
        # Vérifier les dimensions
        print(f"📊 Train: {train_generator.samples} échantillons, {train_generator.num_classes} classes")
        print(f"📊 Val: {validation_generator.samples} échantillons, {validation_generator.num_classes} classes")
        
        # Poids de classe
        class_weights = self.calculate_class_weights()
        
        # Callbacks
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        callbacks = [
            ModelCheckpoint(
                f'models/edufruit_best_{timestamp}.h5',
                monitor='val_accuracy',
                save_best_only=True,
                verbose=1
            ),
            EarlyStopping(
                monitor='val_accuracy',
                patience=15,
                restore_best_weights=True,
                verbose=1
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=7,
                min_lr=1e-7,
                verbose=1
            ),
            TensorBoard(
                log_dir=f'outputs/logs/tensorboard_{timestamp}',
                histogram_freq=1
            )
        ]
        
        print(f"\n🔥 Entraînement ({epochs} epochs)...")
        
        # Entraînement
        self.history = self.model.fit(
            train_generator,
            steps_per_epoch=train_generator.samples // batch_size,
            epochs=epochs,
            validation_data=validation_generator,
            validation_steps=validation_generator.samples // batch_size,
            callbacks=callbacks,
            class_weight=class_weights,
            verbose=1
        )
        
        # Sauvegarder le modèle final
        final_model_path = f'models/edufruit_final_{timestamp}.h5'
        self.model.save(final_model_path)
        
        print(f"\n🎉 ENTRAÎNEMENT TERMINÉ!")
        print(f"💾 Modèle sauvegardé: {final_model_path}")
        
        return self.history

    def plot_training_history(self):
        """Générer les graphiques d'entraînement"""
        
        if self.history is None:
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('EduFruit - Historique d\'entraînement', fontsize=16)
        
        # Accuracy
        axes[0, 0].plot(self.history.history['accuracy'], label='Train')
        axes[0, 0].plot(self.history.history['val_accuracy'], label='Validation')
        axes[0, 0].set_title('Accuracy')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Loss
        axes[0, 1].plot(self.history.history['loss'], label='Train')
        axes[0, 1].plot(self.history.history['val_loss'], label='Validation')
        axes[0, 1].set_title('Loss')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Gap Train-Val
        train_acc = np.array(self.history.history['accuracy'])
        val_acc = np.array(self.history.history['val_accuracy'])
        axes[1, 0].plot(train_acc - val_acc, color='red')
        axes[1, 0].set_title('Overfitting Detection')
        axes[1, 0].grid(True)
        
        # Métriques finales
        final_acc = self.history.history['val_accuracy'][-1]
        axes[1, 1].text(0.5, 0.5, f'Accuracy Finale\n{final_acc:.1%}', 
                       ha='center', va='center', fontsize=20,
                       transform=axes[1, 1].transAxes)
        axes[1, 1].set_title('Performance Finale')
        
        plt.tight_layout()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        plt.savefig(f'outputs/plots/training_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()


def main():
    """Fonction principale"""
    
    print("🍎" * 20)
    print("🍎 EDUFRUIT V3 - ENTRAÎNEMENT")
    print("🍎" * 20)
    
    # Créer l'instance
    trainer = EduFruitTrainer()
    
    # Choix rapide
    print("\n🎯 Options d'entraînement:")
    print("1. Test rapide (5 epochs)")
    print("2. Entraînement court (15 epochs)")
    print("3. Entraînement complet (50 epochs)")
    
    choice = input("\nChoisissez (1/2/3): ").strip()
    
    if choice == "1":
        epochs = 5
        print("🧪 Mode test rapide")
    elif choice == "2":
        epochs = 15
        print("⚡ Mode entraînement court")
    else:
        epochs = 50
        print("🚀 Mode entraînement complet")
    
    # Lancer l'entraînement
    try:
        history = trainer.train_model(epochs=epochs, batch_size=32)
        trainer.plot_training_history()
        
        print("\n🎉 SUCCÈS!")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()