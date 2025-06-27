#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EduFruit Project Recommendations Generator
Provides actionable recommendations based on project assessment
"""

import json
import sys
from pathlib import Path
from datetime import datetime

class ProjectRecommendations:
    def __init__(self, assessment_file=None):
        """Initialize with assessment data"""
        self.assessment = None
        self.recommendations = []
        
        if assessment_file:
            self.load_assessment(assessment_file)
        
        print("💡 EduFruit Project Recommendations Generator")
    
    def load_assessment(self, assessment_file):
        """Load assessment data from JSON file"""
        try:
            with open(assessment_file, 'r', encoding='utf-8') as f:
                self.assessment = json.load(f)
            print(f"✅ Loaded assessment from: {assessment_file}")
        except Exception as e:
            print(f"❌ Error loading assessment: {e}")
            return False
        return True
    
    def find_latest_assessment(self):
        """Find the most recent assessment file"""
        project_root = Path(".")
        assessment_files = list(project_root.glob("project_assessment_*.json"))
        
        if not assessment_files:
            print("❌ No assessment files found. Run the assessment script first.")
            return None
        
        latest_file = max(assessment_files, key=lambda f: f.stat().st_mtime)
        print(f"📄 Using latest assessment: {latest_file}")
        return latest_file
    
    def generate_environment_recommendations(self):
        """Generate environment-related recommendations"""
        if 'environment' not in self.assessment:
            return
        
        env = self.assessment['environment']
        
        # Virtual environment check
        if not env['virtual_env']['in_virtual_env']:
            self.recommendations.append({
                'category': 'Environment',
                'priority': 'HIGH',
                'issue': 'Not running in virtual environment',
                'recommendation': 'Create and use a virtual environment',
                'commands': [
                    'python -m venv edufruit_env',
                    'edufruit_env\\Scripts\\activate  # Windows',
                    'source edufruit_env/bin/activate  # Linux/Mac'
                ]
            })
        
        # Missing dependencies
        missing_deps = env.get('missing_dependencies', [])
        if missing_deps:
            self.recommendations.append({
                'category': 'Environment',
                'priority': 'HIGH',
                'issue': f'Missing key dependencies: {", ".join(missing_deps)}',
                'recommendation': 'Install missing dependencies',
                'commands': [f'pip install {" ".join(missing_deps)}']
            })
    
    def generate_structure_recommendations(self):
        """Generate file structure recommendations"""
        if 'file_structure' not in self.assessment:
            return
        
        structure = self.assessment['file_structure']['structure']
        
        # Check for essential directories
        essential_dirs = ['models', 'data', 'streamlit_app']
        missing_dirs = []
        
        for essential in essential_dirs:
            found = any(essential in path.lower() for path in structure.keys())
            if not found:
                missing_dirs.append(essential)
        
        if missing_dirs:
            self.recommendations.append({
                'category': 'Structure',
                'priority': 'MEDIUM',
                'issue': f'Missing recommended directories: {", ".join(missing_dirs)}',
                'recommendation': 'Create standard project structure',
                'commands': [f'mkdir {dir_name}' for dir_name in missing_dirs]
            })
        
        # Check for large files in root
        if 'ROOT' in structure:
            large_files = [f for f in structure['ROOT']['files'] if f['size_mb'] > 50]
            if large_files:
                file_names = [f['name'] for f in large_files]
                self.recommendations.append({
                    'category': 'Structure',
                    'priority': 'MEDIUM',
                    'issue': f'Large files in root directory: {", ".join(file_names)}',
                    'recommendation': 'Move large files to appropriate subdirectories',
                    'commands': ['# Move files manually to data/ or models/ directories']
                })
    
    def generate_documentation_recommendations(self):
        """Generate documentation recommendations"""
        if 'documentation' not in self.assessment:
            return
        
        docs = self.assessment['documentation']
        
        # README check
        if not docs['has_readme']:
            self.recommendations.append({
                'category': 'Documentation',
                'priority': 'HIGH',
                'issue': 'No README file found',
                'recommendation': 'Create a comprehensive README.md file',
                'commands': ['# Create README.md with project description, setup instructions, and usage']
            })
        
        # Setup instructions
        readme_files = docs.get('readme_files', [])
        if readme_files:
            # Check if README is too small (likely incomplete)
            small_readme = [r for r in readme_files if r['size_kb'] < 2]
            if small_readme:
                self.recommendations.append({
                    'category': 'Documentation',
                    'priority': 'MEDIUM',
                    'issue': 'README file appears incomplete (too small)',
                    'recommendation': 'Expand README with detailed setup and usage instructions',
                    'commands': ['# Add sections: Description, Installation, Usage, Examples']
                })
    
    def generate_requirements_recommendations(self):
        """Generate requirements file recommendations"""
        if 'requirements' not in self.assessment:
            return
        
        reqs = self.assessment['requirements']
        
        # Requirements file check
        if not reqs['has_requirements']:
            self.recommendations.append({
                'category': 'Dependencies',
                'priority': 'HIGH',
                'issue': 'No requirements.txt file found',
                'recommendation': 'Create requirements.txt for reproducible environment',
                'commands': [
                    'pip freeze > requirements.txt',
                    '# Or create manually with only essential packages'
                ]
            })
        else:
            # Check if we have multiple requirement files
            req_files = reqs['files']
            if len(req_files) > 2:
                self.recommendations.append({
                    'category': 'Dependencies',
                    'priority': 'LOW',
                    'issue': 'Multiple requirements files found',
                    'recommendation': 'Consider consolidating to requirements.txt and optional requirements_dev.txt',
                    'commands': ['# Merge similar requirement files']
                })
    
    def generate_streamlit_recommendations(self):
        """Generate Streamlit app recommendations"""
        if 'streamlit_app' not in self.assessment:
            return
        
        st_app = self.assessment['streamlit_app']
        
        if st_app['has_app']:
            app_files = st_app['app_files']
            
            # Check for basic features
            all_features = set()
            for app_file in app_files:
                all_features.update(app_file.get('features', []))
            
            missing_features = []
            recommended_features = ['file_upload', 'image_display', 'user_input']
            
            for feature in recommended_features:
                if feature not in all_features:
                    missing_features.append(feature)
            
            if missing_features:
                feature_map = {
                    'file_upload': 'st.file_uploader() for image uploads',
                    'image_display': 'st.image() for showing results',
                    'user_input': 'st.selectbox() or st.radio() for user choices'
                }
                
                suggestions = [feature_map.get(f, f) for f in missing_features]
                
                self.recommendations.append({
                    'category': 'Streamlit',
                    'priority': 'MEDIUM',
                    'issue': f'Missing common Streamlit features: {", ".join(missing_features)}',
                    'recommendation': f'Consider adding: {", ".join(suggestions)}',
                    'commands': ['# Add features to improve user experience']
                })
        else:
            # No Streamlit app found
            if 'models' in self.assessment and self.assessment['models']['count'] > 0:
                self.recommendations.append({
                    'category': 'Streamlit',
                    'priority': 'MEDIUM',
                    'issue': 'ML model found but no Streamlit app',
                    'recommendation': 'Create Streamlit app for model demonstration',
                    'commands': [
                        'mkdir streamlit_app',
                        '# Create main.py with model loading and prediction interface'
                    ]
                })
    
    def generate_model_recommendations(self):
        """Generate model-related recommendations"""
        if 'models' not in self.assessment:
            return
        
        models = self.assessment['models']
        
        if models['count'] == 0:
            # Check if we have training scripts but no models
            if 'python_scripts' in self.assessment:
                scripts = self.assessment['python_scripts']['scripts']
                train_scripts = [path for path, info in scripts.items() 
                               if 'train' in path.lower() and info.get('executable', False)]
                
                if train_scripts:
                    self.recommendations.append({
                        'category': 'Models',
                        'priority': 'MEDIUM',
                        'issue': 'Training scripts found but no model files',
                        'recommendation': 'Run training script to generate model',
                        'commands': [f'python {train_scripts[0]}']
                    })
        else:
            # Check model file sizes
            large_models = [m for m in models['files'] if m['size_mb'] > 100]
            if large_models:
                self.recommendations.append({
                    'category': 'Models',
                    'priority': 'LOW',
                    'issue': f'Large model files detected (>{100}MB)',
                    'recommendation': 'Consider model compression or using Git LFS for version control',
                    'commands': [
                        'git lfs track "*.h5"',
                        '# Or implement model quantization'
                    ]
                })
    
    def generate_data_recommendations(self):
        """Generate data-related recommendations"""
        if 'data_structure' not in self.assessment:
            return
        
        data_dirs = self.assessment['data_structure']
        
        # Check for very large data directories
        large_data_dirs = []
        for dir_path, info in data_dirs.items():
            if info['total_size_mb'] > 500:  # 500MB threshold
                large_data_dirs.append((dir_path, info['total_size_mb']))
        
        if large_data_dirs:
            dir_info = [f"{path} ({size:.0f}MB)" for path, size in large_data_dirs]
            self.recommendations.append({
                'category': 'Data',
                'priority': 'MEDIUM',
                'issue': f'Large data directories: {", ".join(dir_info)}',
                'recommendation': 'Consider data cleanup, compression, or .gitignore',
                'commands': [
                    'python clean.py  # If data cleanup script exists',
                    '# Add large data directories to .gitignore'
                ]
            })
        
        # Check for proper train/test split structure
        ml_datasets = []
        for dir_path, info in data_dirs.items():
            if info.get('dataset_type') == 'ML_dataset':
                ml_datasets.append(dir_path)
        
        if not ml_datasets and any('train' in str(path).lower() for path in data_dirs.keys()):
            self.recommendations.append({
                'category': 'Data',
                'priority': 'LOW',
                'issue': 'Data structure could be better organized',
                'recommendation': 'Ensure clear Train/Test/Validation directory structure',
                'commands': ['# Organize data into Train/ and Test/ subdirectories']
            })
    
    def generate_all_recommendations(self):
        """Generate all recommendations"""
        if not self.assessment:
            print("❌ No assessment data available")
            return
        
        print("🔍 Analyzing project and generating recommendations...")
        
        # Generate recommendations by category
        self.generate_environment_recommendations()
        self.generate_structure_recommendations()
        self.generate_documentation_recommendations()
        self.generate_requirements_recommendations()
        self.generate_streamlit_recommendations()
        self.generate_model_recommendations()
        self.generate_data_recommendations()
        
        return self.recommendations
    
    def print_recommendations(self):
        """Print formatted recommendations"""
        if not self.recommendations:
            print("✅ No specific recommendations - your project looks good!")
            return
        
        print(f"\n📋 PROJECT RECOMMENDATIONS ({len(self.recommendations)} items)")
        print("="*80)
        
        # Group by priority
        high_priority = [r for r in self.recommendations if r['priority'] == 'HIGH']
        medium_priority = [r for r in self.recommendations if r['priority'] == 'MEDIUM']
        low_priority = [r for r in self.recommendations if r['priority'] == 'LOW']
        
        for priority, recs in [('HIGH PRIORITY', high_priority), 
                              ('MEDIUM PRIORITY', medium_priority), 
                              ('LOW PRIORITY', low_priority)]:
            if not recs:
                continue
                
            print(f"\n🚨 {priority} ({len(recs)} items)")
            print("-" * 50)
            
            for i, rec in enumerate(recs, 1):
                print(f"\n{i}. [{rec['category']}] {rec['issue']}")
                print(f"   💡 {rec['recommendation']}")
                
                if rec.get('commands'):
                    print(f"   🔧 Commands:")
                    for cmd in rec['commands']:
                        print(f"      {cmd}")
    
    def save_recommendations(self):
        """Save recommendations to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        rec_file = Path(f"project_recommendations_{timestamp}.json")
        
        output = {
            'timestamp': datetime.now().isoformat(),
            'total_recommendations': len(self.recommendations),
            'recommendations': self.recommendations
        }
        
        with open(rec_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Recommendations saved to: {rec_file}")
        return rec_file
    
    def create_action_plan(self):
        """Create a step-by-step action plan"""
        if not self.recommendations:
            return
        
        print(f"\n📋 ACTION PLAN")
        print("="*50)
        
        # Sort by priority
        priority_order = {'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        sorted_recs = sorted(self.recommendations, 
                           key=lambda x: priority_order.get(x['priority'], 4))
        
        print("Follow these steps in order:\n")
        
        for i, rec in enumerate(sorted_recs, 1):
            priority_emoji = {'HIGH': '🚨', 'MEDIUM': '⚠️', 'LOW': '💡'}
            emoji = priority_emoji.get(rec['priority'], '📝')
            
            print(f"Step {i}: {emoji} [{rec['category']}] {rec['issue']}")
            print(f"   Action: {rec['recommendation']}")
            
            if rec.get('commands'):
                print(f"   Commands to run:")
                for cmd in rec['commands']:
                    if not cmd.startswith('#'):
                        print(f"      $ {cmd}")
            print()

def main():
    """Main function"""
    print("💡" * 20)
    print("💡 EDUFRUIT PROJECT RECOMMENDATIONS")
    print("💡" * 20)
    
    # Initialize recommendations generator
    generator = ProjectRecommendations()
    
    # Try to find and load latest assessment
    assessment_file = generator.find_latest_assessment()
    if not assessment_file:
        print("\n❌ No assessment file found!")
        print("💡 Run the project assessment script first:")
        print("   python assess_project.py")
        return
    
    # Load assessment
    if not generator.load_assessment(assessment_file):
        return
    
    # Generate recommendations
    recommendations = generator.generate_all_recommendations()
    
    # Print results
    generator.print_recommendations()
    generator.create_action_plan()
    
    # Save recommendations
    generator.save_recommendations()
    
    print("\n✅ Recommendations generated successfully!")
    print("💡 Use the action plan above to improve your project")

if __name__ == "__main__":
    main()