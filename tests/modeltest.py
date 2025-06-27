#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EduFruit V3 Model Efficiency Tester - Fixed Version
"""

import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
import os
import time
import psutil
import json
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix
from datetime import datetime

class EduFruitTester:
    def __init__(self, model_path="../models/", data_dir="../data/processed/edufruit_dataset"):
        """Initialize the efficiency tester with your specific paths"""
        self.classes = ['Pomme', 'Banane', 'Avocat', 'Concombre', 'Citron']
        self.num_classes = len(self.classes)
        self.img_size = (100, 100)
        self.model_path = model_path
        self.data_dir = data_dir
        
        # Create output directories with correct paths
        os.makedirs("../outputs/efficiency_tests", exist_ok=True)
        os.makedirs("../outputs/efficiency_plots", exist_ok=True)
        
        print(f"🚀 EduFruit V3 Efficiency Tester initialized")
        print(f"🔍 Model: {os.path.abspath(model_path)}")
        print(f"📁 Data: {os.path.abspath(data_dir)}")
    
    def load_model_and_data(self):
        """Load the model and prepare test data"""
        print("\n🔍 Loading model and data...")
        
        # Verify model exists
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model not found at: {os.path.abspath(self.model_path)}")
        
        # Verify data exists
        if not os.path.exists(os.path.join(self.data_dir, "Test")):
            raise FileNotFoundError(f"Test data not found at: {os.path.abspath(self.data_dir)}")
        
        # Load the trained model
        self.model = load_model(self.model_path)
        print(f"✅ Model loaded from: {os.path.abspath(self.model_path)}")
        
        # Prepare test data generator
        test_datagen = ImageDataGenerator(rescale=1./255)
        
        self.test_generator = test_datagen.flow_from_directory(
            os.path.join(self.data_dir, "Test"),
            target_size=self.img_size,
            batch_size=32,
            class_mode='categorical',
            classes=self.classes,
            shuffle=False  # Important for correct evaluation
        )
        
        print(f"✅ Test data loaded: {self.test_generator.samples} samples")
        
        # Get true labels
        self.true_labels = self.test_generator.classes
        self.class_indices = self.test_generator.class_indices
        
        return self.model, self.test_generator
    
    def evaluate_model_performance(self):
        """Evaluate model performance metrics"""
        print("\n📊 Evaluating model performance...")
        
        # Standard evaluation
        evaluation = self.model.evaluate(self.test_generator, verbose=1)
        print(f"📈 Test Loss: {evaluation[0]:.4f}")
        print(f"📈 Test Accuracy: {evaluation[1]:.4f}")
        
        # Predictions for detailed metrics - FIXED: Added verbose=0
        predictions = self.model.predict(self.test_generator, verbose=0)
        self.predicted_labels = np.argmax(predictions, axis=1)
        
        # Classification report
        print("\n📝 Classification Report:")
        print(classification_report(
            self.true_labels, 
            self.predicted_labels, 
            target_names=self.classes
        ))
        
        # Confusion matrix
        self.plot_confusion_matrix()
        
        # Per-class accuracy
        self.calculate_per_class_accuracy()
        
        return evaluation
    
    def plot_confusion_matrix(self):
        """Generate and save confusion matrix"""
        cm = confusion_matrix(self.true_labels, self.predicted_labels)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=self.classes, 
                    yticklabels=self.classes)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"../outputs/efficiency_plots/confusion_matrix_{timestamp}.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"✅ Confusion matrix saved to {os.path.abspath(save_path)}")
    
    def calculate_per_class_accuracy(self):
        """Calculate and display per-class accuracy"""
        cm = confusion_matrix(self.true_labels, self.predicted_labels)
        per_class_accuracy = cm.diagonal() / cm.sum(axis=1)
        
        print("\n🎯 Per-Class Accuracy:")
        for i, class_name in enumerate(self.classes):
            print(f"   {class_name}: {per_class_accuracy[i]:.2%}")
        
        # Plot per-class accuracy
        plt.figure(figsize=(10, 6))
        plt.bar(self.classes, per_class_accuracy)
        plt.title('Per-Class Accuracy')
        plt.ylabel('Accuracy')
        plt.ylim(0, 1.1)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"../outputs/efficiency_plots/per_class_accuracy_{timestamp}.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"✅ Per-class accuracy plot saved to {os.path.abspath(save_path)}")
    
    def test_inference_speed(self, num_tests=100):
        """Test the model's inference speed - FIXED VERSION"""
        print(f"\n⏱️ Testing inference speed with {num_tests} samples...")
        
        # Get a batch of test images - FIXED: Better handling of data generator
        try:
            self.test_generator.reset()  # Reset generator to start
            test_images, test_labels = next(self.test_generator)
            
            # Ensure we have enough samples
            if len(test_images) < num_tests:
                print(f"⚠️ Only {len(test_images)} images available, using all of them")
                num_tests = len(test_images)
            
        except Exception as e:
            print(f"Error getting test images: {e}")
            return None
        
        # Warm-up - FIXED: Added verbose=0
        _ = self.model.predict(test_images[:1], verbose=0)
        
        # Time individual inferences - FIXED: Added verbose=0
        individual_times = []
        print("Running individual inference tests...")
        
        for i in range(min(num_tests, len(test_images))):
            start_time = time.time()
            _ = self.model.predict(test_images[i:i+1], verbose=0)  # FIXED: Added verbose=0
            end_time = time.time()
            individual_times.append(end_time - start_time)
            
            # Progress indicator (every 20 samples)
            if (i + 1) % 20 == 0:
                print(f"   Completed {i + 1}/{num_tests} individual tests")
        
        # Time batch inference - FIXED: Added verbose=0
        print("Running batch inference test...")
        batch_start = time.time()
        _ = self.model.predict(test_images[:num_tests], verbose=0)  # FIXED: Added verbose=0
        batch_end = time.time()
        batch_time = batch_end - batch_start
        
        # Calculate metrics
        avg_time = np.mean(individual_times)
        min_time = np.min(individual_times)
        max_time = np.max(individual_times)
        std_time = np.std(individual_times)
        fps = 1 / avg_time if avg_time > 0 else 0
        batch_fps = num_tests / batch_time if batch_time > 0 else 0
        
        print("\n⏱️ Inference Speed Results:")
        print(f"   Average time per image: {avg_time:.4f} seconds")
        print(f"   Fastest inference: {min_time:.4f} seconds")
        print(f"   Slowest inference: {max_time:.4f} seconds")
        print(f"   Standard deviation: {std_time:.4f} seconds")
        print(f"   Throughput: {fps:.2f} images/second")
        print(f"   Batch time ({num_tests} images): {batch_time:.4f} seconds")
        print(f"   Batch throughput: {batch_fps:.2f} images/second")
        
        # Plot inference times
        plt.figure(figsize=(10, 6))
        plt.plot(individual_times)
        plt.axhline(y=avg_time, color='r', linestyle='--', label=f'Average: {avg_time:.4f}s')
        plt.title('Individual Inference Times')
        plt.xlabel('Sample Number')
        plt.ylabel('Time (seconds)')
        plt.legend()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"../outputs/efficiency_plots/inference_times_{timestamp}.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"✅ Inference times plot saved to {os.path.abspath(save_path)}")
        
        return {
            'average_time': avg_time,
            'min_time': min_time,
            'max_time': max_time,
            'std_time': std_time,
            'fps': fps,
            'batch_time': batch_time,
            'batch_fps': batch_fps
        }
    
    def test_memory_usage(self, num_tests=100):
        """Test memory usage during inference - FIXED VERSION"""
        print(f"\n💾 Testing memory usage with {num_tests} samples...")
        
        # Get a batch of test images
        try:
            self.test_generator.reset()
            test_images, _ = next(self.test_generator)
            
            if len(test_images) < num_tests:
                print(f"⚠️ Only {len(test_images)} images available, using all of them")
                num_tests = len(test_images)
                
        except Exception as e:
            print(f"Error getting test images: {e}")
            return None
        
        # Measure baseline memory
        process = psutil.Process(os.getpid())
        baseline_mem = process.memory_info().rss / (1024 * 1024)  # in MB
        
        # Measure memory during inference - FIXED: Added verbose=0
        mem_usages = []
        for i in range(min(num_tests, len(test_images))):
            _ = self.model.predict(test_images[i:i+1], verbose=0)  # FIXED: Added verbose=0
            mem_usages.append(process.memory_info().rss / (1024 * 1024))
            
            if (i + 1) % 25 == 0:
                print(f"   Memory test progress: {i + 1}/{num_tests}")
        
        avg_mem = np.mean(mem_usages)
        max_mem = np.max(mem_usages)
        mem_increase = max_mem - baseline_mem
        
        print("\n💾 Memory Usage Results:")
        print(f"   Baseline memory: {baseline_mem:.2f} MB")
        print(f"   Average memory during inference: {avg_mem:.2f} MB")
        print(f"   Peak memory usage: {max_mem:.2f} MB")
        print(f"   Memory increase during inference: {mem_increase:.2f} MB")
        
        # Plot memory usage
        plt.figure(figsize=(10, 6))
        plt.plot(mem_usages)
        plt.axhline(y=baseline_mem, color='g', linestyle='--', label=f'Baseline: {baseline_mem:.2f}MB')
        plt.axhline(y=max_mem, color='r', linestyle='--', label=f'Peak: {max_mem:.2f}MB')
        plt.title('Memory Usage During Inference')
        plt.xlabel('Sample Number')
        plt.ylabel('Memory Usage (MB)')
        plt.legend()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"../outputs/efficiency_plots/memory_usage_{timestamp}.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"✅ Memory usage plot saved to {os.path.abspath(save_path)}")
        
        return {
            'baseline_memory': baseline_mem,
            'average_memory': avg_mem,
            'peak_memory': max_mem,
            'memory_increase': mem_increase
        }
    
    def test_model_robustness(self, noise_levels=[0.01, 0.05, 0.1, 0.2]):
        """Test model robustness to input noise - FIXED VERSION"""
        print("\n🧪 Testing model robustness to noise...")
        
        # Get test data
        try:
            self.test_generator.reset()
            test_images, test_labels = next(self.test_generator)
            num_samples = len(test_images)
            print(f"   Using {num_samples} samples for robustness testing")
            
        except Exception as e:
            print(f"Error getting test data: {e}")
            return None
        
        robustness_results = {}
        
        for noise_level in noise_levels:
            print(f"   Testing noise level: {noise_level:.2f}")
            
            # Add Gaussian noise
            noisy_images = test_images + np.random.normal(
                loc=0, 
                scale=noise_level, 
                size=test_images.shape
            )
            
            # Clip to valid range
            noisy_images = np.clip(noisy_images, 0, 1)
            
            # Evaluate - FIXED: Added verbose=0
            loss, acc = self.model.evaluate(noisy_images, test_labels, verbose=0)
            robustness_results[noise_level] = {
                'accuracy': acc,
                'loss': loss
            }
            
            print(f"      Noise level {noise_level:.2f}: Accuracy = {acc:.4f}, Loss = {loss:.4f}")
        
        # Plot robustness results
        noise_levels_list = list(robustness_results.keys())
        accuracies = [v['accuracy'] for v in robustness_results.values()]
        losses = [v['loss'] for v in robustness_results.values()]
        
        plt.figure(figsize=(12, 5))
        
        plt.subplot(1, 2, 1)
        plt.plot(noise_levels_list, accuracies, 'bo-')
        plt.title('Accuracy vs Noise Level')
        plt.xlabel('Noise Level')
        plt.ylabel('Accuracy')
        plt.grid(True, alpha=0.3)
        
        plt.subplot(1, 2, 2)
        plt.plot(noise_levels_list, losses, 'ro-')
        plt.title('Loss vs Noise Level')
        plt.xlabel('Noise Level')
        plt.ylabel('Loss')
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        save_path = f"../outputs/efficiency_plots/robustness_{timestamp}.png"
        plt.savefig(save_path, dpi=300)
        plt.close()
        print(f"✅ Robustness analysis saved to {os.path.abspath(save_path)}")
        
        return robustness_results
    
    def run_comprehensive_test(self):
        """Run all tests and save comprehensive report"""
        print("\n" + "="*60)
        print("🏁 STARTING COMPREHENSIVE MODEL EFFICIENCY TEST")
        print("="*60)
        
        # Load model and data
        self.load_model_and_data()
        
        # Initialize results dictionary
        results = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'model': os.path.basename(self.model_path),
            'test_samples': self.test_generator.samples,
            'classes': self.classes
        }
        
        # Run all tests with error handling
        try:
            print("\n🔍 Running performance evaluation...")
            results['performance'] = {
                'loss': None,
                'accuracy': None,
                'classification_report': None
            }
            perf_results = self.evaluate_model_performance()
            results['performance']['loss'] = float(perf_results[0])
            results['performance']['accuracy'] = float(perf_results[1])
            
            print("\n⏱️ Testing inference speed...")
            speed_results = self.test_inference_speed()
            if speed_results:
                results['inference_speed'] = speed_results
            else:
                print("⚠️ Inference speed test failed")
                results['inference_speed'] = "Test failed"
            
            print("\n💾 Testing memory usage...")
            memory_results = self.test_memory_usage()
            if memory_results:
                results['memory_usage'] = memory_results
            else:
                print("⚠️ Memory usage test failed")
                results['memory_usage'] = "Test failed"
            
            print("\n🧪 Testing robustness...")
            robustness_results = self.test_model_robustness()
            if robustness_results:
                results['robustness'] = robustness_results
            else:
                print("⚠️ Robustness test failed")
                results['robustness'] = "Test failed"
            
        except Exception as e:
            print(f"❌ Error during testing: {e}")
            results['error'] = str(e)
        
        # Save comprehensive report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = f'../outputs/efficiency_tests/full_report_{timestamp}.json'
        
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=4, default=str)  # Added default=str for serialization
        
        print("\n" + "="*60)
        print(f"🎉 COMPREHENSIVE TEST COMPLETED!")
        print(f"📄 Full report saved to: {os.path.abspath(report_path)}")
        print("="*60)
        
        return results


def main():
    """Main function"""
    print("🧪" * 20)
    print("🧪 EDUFRUIT V3 MODEL EFFICIENCY TESTER")
    print("🧪" * 20)
    
    # Initialize tester with your specific model
    tester = EduFruitTester(
        model_path="../models/edufruit_final_20250622_204602.h5",
        data_dir="../data/processed/edufruit_dataset"
    )
    
    # Run tests
    print("\nSelect test mode:")
    print("1. Quick test (performance only)")
    print("2. Standard test (performance + speed + memory)")
    print("3. Comprehensive test (all tests)")
    
    choice = input("\nChoose (1/2/3): ").strip()
    
    try:
        if choice == "1":
            tester.load_model_and_data()
            tester.evaluate_model_performance()
        elif choice == "2":
            tester.load_model_and_data()
            tester.evaluate_model_performance()
            tester.test_inference_speed()
            tester.test_memory_usage()
        else:
            tester.run_comprehensive_test()
        
        print("\n✅ Testing completed!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()