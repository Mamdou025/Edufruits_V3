#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset Image Counter for EduFruit Project
Counts actual images in both raw and processed datasets
Place this file in your project root or tests folder
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple
import json
from datetime import datetime

class DatasetCounter:
    """Count images in EduFruit datasets"""
    
    def __init__(self, project_root: str = None):
        # Auto-detect project root if not provided
        if project_root is None:
            current_dir = Path(__file__).parent
            # Look for common project indicators
            for parent in [current_dir] + list(current_dir.parents):
                if (parent / "models").exists() or (parent / "data").exists():
                    project_root = str(parent)
                    break
            else:
                project_root = str(current_dir)
        
        self.project_root = Path(project_root)
        print(f"📁 Project root: {self.project_root}")
        
        # Define paths
        self.raw_data_path = self.project_root / "data" / "raw" / "fruits-360"
        self.processed_data_path = self.project_root / "data" / "processed" / "edufruit_dataset"
        
        # Expected class mappings from your config
        self.expected_class_mappings = {
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
        
        # Image extensions to count
        self.image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}
    
    def count_images_in_folder(self, folder_path: Path) -> int:
        """Count image files in a folder"""
        if not folder_path.exists():
            return 0
        
        count = 0
        for file in folder_path.iterdir():
            if file.is_file() and file.suffix.lower() in self.image_extensions:
                count += 1
        return count
    
    def analyze_raw_dataset(self) -> Dict[str, Dict[str, Dict[str, int]]]:
        """Analyze the raw fruits-360 dataset"""
        
        print("\n🔍 ANALYZING RAW DATASET (fruits-360)")
        print("=" * 60)
        
        if not self.raw_data_path.exists():
            print(f"❌ Raw dataset not found at: {self.raw_data_path}")
            return {}
        
        results = {}
        
        for split in ['Training', 'Test']:
            split_path = self.raw_data_path / split
            
            if not split_path.exists():
                print(f"❌ {split} folder not found: {split_path}")
                continue
            
            print(f"\n📂 {split} Set:")
            split_results = {}
            
            # Check each expected class mapping
            for class_name, source_folders in self.expected_class_mappings.items():
                print(f"\n   🎯 {class_name}:")
                class_total = 0
                folder_results = {}
                
                for source_folder in source_folders:
                    folder_path = split_path / source_folder
                    count = self.count_images_in_folder(folder_path)
                    folder_results[source_folder] = count
                    class_total += count
                    
                    status = "✅" if count > 0 else "❌"
                    print(f"      {status} {source_folder:25}: {count:4d} images")
                
                split_results[class_name] = {
                    'total': class_total,
                    'folders': folder_results
                }
                
                print(f"      📊 Total {class_name:15}: {class_total:4d} images")
            
            results[split] = split_results
        
        return results
    
    def analyze_processed_dataset(self) -> Dict[str, Dict[str, int]]:
        """Analyze the processed unified dataset"""
        
        print("\n🔍 ANALYZING PROCESSED DATASET (unified)")
        print("=" * 60)
        
        if not self.processed_data_path.exists():
            print(f"❌ Processed dataset not found at: {self.processed_data_path}")
            return {}
        
        results = {}
        
        for split in ['Training', 'Test']:
            split_path = self.processed_data_path / split
            
            if not split_path.exists():
                print(f"❌ {split} folder not found: {split_path}")
                continue
            
            print(f"\n📂 {split} Set:")
            split_results = {}
            
            # Find all class folders
            class_folders = [f for f in split_path.iterdir() if f.is_dir()]
            class_folders.sort()
            
            total_images = 0
            for class_folder in class_folders:
                count = self.count_images_in_folder(class_folder)
                split_results[class_folder.name] = count
                total_images += count
                
                percentage = (count / total_images * 100) if total_images > 0 else 0
                print(f"   📊 {class_folder.name:15}: {count:4d} images")
            
            # Calculate percentages after all counts are done
            print(f"\n   📈 Percentages in {split}:")
            for class_name, count in split_results.items():
                percentage = (count / total_images * 100) if total_images > 0 else 0
                print(f"      {class_name:15}: {percentage:5.1f}%")
            
            print(f"\n   🔢 Total {split:8}: {total_images:4d} images")
            results[split] = split_results
        
        return results
    
    def compare_expected_vs_actual(self, raw_results: Dict, processed_results: Dict):
        """Compare expected vs actual class distributions"""
        
        print("\n🔍 COMPARISON: EXPECTED vs ACTUAL")
        print("=" * 60)
        
        if not processed_results or 'Training' not in processed_results:
            print("❌ No processed data to compare")
            return
        
        expected_classes = list(self.expected_class_mappings.keys())
        actual_classes = list(processed_results['Training'].keys())
        
        print(f"\n📋 Expected classes: {expected_classes}")
        print(f"📋 Actual classes:   {actual_classes}")
        
        # Check for mismatches
        missing_classes = set(expected_classes) - set(actual_classes)
        extra_classes = set(actual_classes) - set(expected_classes)
        
        if missing_classes:
            print(f"\n❌ MISSING CLASSES: {list(missing_classes)}")
            for missing in missing_classes:
                print(f"   🔍 Expected '{missing}' but not found in processed dataset")
        
        if extra_classes:
            print(f"\n⚠️  EXTRA CLASSES: {list(extra_classes)}")
            for extra in extra_classes:
                print(f"   🔍 Found '{extra}' but not expected in configuration")
        
        if not missing_classes and not extra_classes:
            print(f"\n✅ CLASS NAMES MATCH PERFECTLY!")
        
        # Compare Training vs Test distribution
        if 'Test' in processed_results:
            print(f"\n📊 TRAINING vs TEST DISTRIBUTION:")
            train_data = processed_results['Training']
            test_data = processed_results['Test']
            
            for class_name in actual_classes:
                train_count = train_data.get(class_name, 0)
                test_count = test_data.get(class_name, 0)
                total = train_count + test_count
                
                if total > 0:
                    train_pct = train_count / total * 100
                    test_pct = test_count / total * 100
                    ratio = train_count / test_count if test_count > 0 else float('inf')
                    
                    print(f"   {class_name:15}: Train {train_count:4d} ({train_pct:5.1f}%) | Test {test_count:3d} ({test_pct:5.1f}%) | Ratio {ratio:.1f}:1")
    
    def generate_class_weights_code(self, processed_results: Dict):
        """Generate updated class weights code based on actual data"""
        
        if not processed_results or 'Training' not in processed_results:
            return
        
        print("\n🛠️  UPDATED CLASS WEIGHTS CODE")
        print("=" * 60)
        
        train_data = processed_results['Training']
        class_names = list(train_data.keys())
        
        print("```python")
        print("def calculate_class_weights(self):")
        print('    """Calculer les poids de classe pour corriger le déséquilibre"""')
        print("    ")
        print("    # Counts basés sur l'analyse réelle du dataset")
        print("    estimated_counts = {")
        
        for i, (class_name, count) in enumerate(train_data.items()):
            print(f"        {i}: {count:4d},  # {class_name}")
        
        print("    }")
        print("    ")
        print("    # Calculer les poids (inverse de la fréquence)")
        print("    max_count = max(estimated_counts.values())")
        print("    class_weights = {}")
        print("    ")
        print("    for class_idx, count in estimated_counts.items():")
        print("        weight = max_count / count")
        print("        class_weights[class_idx] = weight")
        print("    ")
        print("    return class_weights")
        print("```")
        
        # Calculate and show the actual weights
        counts = list(train_data.values())
        max_count = max(counts)
        
        print(f"\n📊 Calculated weights:")
        for i, (class_name, count) in enumerate(train_data.items()):
            weight = max_count / count if count > 0 else 0
            print(f"   {class_name:15}: {weight:.2f} (from {count:4d} images)")
    
    def save_analysis_report(self, raw_results: Dict, processed_results: Dict):
        """Save detailed analysis to JSON file"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = self.project_root / "outputs" / f"dataset_analysis_{timestamp}.json"
        
        # Create outputs directory if it doesn't exist
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        report = {
            'timestamp': timestamp,
            'project_root': str(self.project_root),
            'raw_dataset_path': str(self.raw_data_path),
            'processed_dataset_path': str(self.processed_data_path),
            'expected_class_mappings': self.expected_class_mappings,
            'raw_analysis': raw_results,
            'processed_analysis': processed_results
        }
        
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Detailed report saved: {report_path}")
        return report_path
    
    def run_full_analysis(self):
        """Run complete dataset analysis"""
        
        print("🍎" * 20)
        print("🍎 EDUFRUIT DATASET ANALYSIS")
        print("🍎" * 20)
        
        # Analyze raw dataset
        raw_results = self.analyze_raw_dataset()
        
        # Analyze processed dataset  
        processed_results = self.analyze_processed_dataset()
        
        # Compare expected vs actual
        self.compare_expected_vs_actual(raw_results, processed_results)
        
        # Generate updated class weights
        self.generate_class_weights_code(processed_results)
        
        # Save report
        report_path = self.save_analysis_report(raw_results, processed_results)
        
        print(f"\n🎉 ANALYSIS COMPLETE!")
        print(f"📊 Check the detailed report at: {report_path}")
        
        return raw_results, processed_results

def main():
    """Main function to run the analysis"""
    
    # Allow specifying project root as command line argument
    project_root = None
    if len(sys.argv) > 1:
        project_root = sys.argv[1]
    
    try:
        counter = DatasetCounter(project_root)
        raw_results, processed_results = counter.run_full_analysis()
        
        print(f"\n📋 SUMMARY:")
        
        if processed_results and 'Training' in processed_results:
            train_data = processed_results['Training']
            total_train = sum(train_data.values())
            print(f"   📊 Total training images: {total_train}")
            print(f"   📊 Number of classes: {len(train_data)}")
            print(f"   📊 Classes found: {list(train_data.keys())}")
            
            if total_train == 0:
                print(f"   ⚠️  No training images found - check your dataset!")
            elif len(train_data) != 5:
                print(f"   ⚠️  Expected 5 classes, found {len(train_data)}")
            else:
                print(f"   ✅ Dataset structure looks good!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()