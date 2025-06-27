#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EduFruit Complete Project Assessment Script
Analyzes everything: structure, environment, models, data, scripts functionality
"""

import os
import sys
import json
import subprocess
import importlib
import platform
from pathlib import Path
from datetime import datetime
import ast
import re

class EduFruitProjectAssessment:
    def __init__(self, project_root="."):
        """Initialize comprehensive project assessment"""
        self.project_root = Path(project_root).absolute()
        self.assessment = {
            'timestamp': datetime.now().isoformat(),
            'project_root': str(self.project_root),
            'assessment_sections': []
        }
        
        print("🔍" * 30)
        print("🔍 EDUFRUIT COMPLETE PROJECT ASSESSMENT")
        print("🔍" * 30)
        print(f"📁 Project root: {self.project_root}")
        
    def assess_file_structure(self):
        """Analyze complete file and directory structure"""
        print("\n📁 ASSESSING FILE STRUCTURE")
        print("="*50)
        
        structure = {}
        total_files = 0
        total_size = 0
        file_types = {}
        
        # Walk through all directories
        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden directories and cache
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            rel_path = os.path.relpath(root, self.project_root)
            if rel_path == ".":
                rel_path = "ROOT"
            
            dir_files = []
            dir_size = 0
            
            for file in files:
                if file.startswith('.'):
                    continue
                    
                file_path = os.path.join(root, file)
                try:
                    file_size = os.path.getsize(file_path)
                    file_ext = Path(file).suffix.lower()
                    
                    dir_files.append({
                        'name': file,
                        'size': file_size,
                        'size_mb': file_size / (1024 * 1024),
                        'extension': file_ext
                    })
                    
                    dir_size += file_size
                    total_size += file_size
                    total_files += 1
                    
                    # Count file types
                    if file_ext:
                        file_types[file_ext] = file_types.get(file_ext, 0) + 1
                    else:
                        file_types['no_extension'] = file_types.get('no_extension', 0) + 1
                        
                except (OSError, FileNotFoundError):
                    continue
            
            if dir_files:  # Only include directories with files
                structure[rel_path] = {
                    'file_count': len(dir_files),
                    'total_size_mb': dir_size / (1024 * 1024),
                    'files': dir_files
                }
        
        # Print summary
        print(f"📊 PROJECT OVERVIEW:")
        print(f"   Total files: {total_files:,}")
        print(f"   Total size: {total_size / (1024 * 1024):.2f} MB")
        print(f"   Directories with files: {len(structure)}")
        
        print(f"\n📂 DIRECTORY BREAKDOWN:")
        sorted_dirs = sorted(structure.items(), key=lambda x: x[1]['total_size_mb'], reverse=True)
        for dir_name, info in sorted_dirs[:15]:  # Top 15 directories
            print(f"   {dir_name}: {info['file_count']} files, {info['total_size_mb']:.2f} MB")
        
        print(f"\n📄 FILE TYPES:")
        sorted_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)
        for ext, count in sorted_types[:10]:  # Top 10 file types
            ext_display = ext if ext else "no extension"
            print(f"   {ext_display}: {count} files")
        
        self.assessment['file_structure'] = {
            'summary': {
                'total_files': total_files,
                'total_size_mb': total_size / (1024 * 1024),
                'directory_count': len(structure)
            },
            'structure': structure,
            'file_types': file_types
        }
        
        return structure
    
    def assess_python_scripts(self):
        """Analyze all Python scripts and their functionality"""
        print("\n🐍 ASSESSING PYTHON SCRIPTS")
        print("="*50)
        
        python_files = []
        
        # Find all Python files
        for root, dirs, files in os.walk(self.project_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.project_root)
                    python_files.append(rel_path)
        
        script_analysis = {}
        
        for script_path in python_files:
            full_path = self.project_root / script_path
            print(f"📝 Analyzing: {script_path}")
            
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Parse the script
                try:
                    tree = ast.parse(content)
                    
                    # Extract information
                    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                    imports = []
                    
                    for node in ast.walk(tree):
                        if isinstance(node, ast.Import):
                            imports.extend([alias.name for alias in node.names])
                        elif isinstance(node, ast.ImportFrom):
                            module = node.module or ""
                            imports.extend([f"{module}.{alias.name}" for alias in node.names])
                    
                    # Check for main execution
                    has_main = '__main__' in content
                    
                    # Get docstring
                    docstring = ast.get_docstring(tree) if tree.body else None
                    
                    script_info = {
                        'size_kb': full_path.stat().st_size / 1024,
                        'lines': len(content.splitlines()),
                        'functions': functions,
                        'classes': classes,
                        'imports': imports,
                        'has_main': has_main,
                        'docstring': docstring,
                        'executable': has_main
                    }
                    
                    print(f"   ✅ {len(functions)} functions, {len(classes)} classes, {len(imports)} imports")
                    
                except SyntaxError as e:
                    script_info = {
                        'error': f'Syntax error: {e}',
                        'size_kb': full_path.stat().st_size / 1024
                    }
                    print(f"   ❌ Syntax error: {e}")
                
            except Exception as e:
                script_info = {
                    'error': f'Read error: {e}',
                    'size_kb': 0
                }
                print(f"   ❌ Error reading file: {e}")
            
            script_analysis[str(script_path)] = script_info
        
        # Summary
        executable_scripts = [path for path, info in script_analysis.items() 
                            if info.get('executable', False)]
        total_functions = sum(len(info.get('functions', [])) for info in script_analysis.values())
        total_classes = sum(len(info.get('classes', [])) for info in script_analysis.values())
        
        print(f"\n📊 PYTHON SCRIPTS SUMMARY:")
        print(f"   Total Python files: {len(python_files)}")
        print(f"   Executable scripts: {len(executable_scripts)}")
        print(f"   Total functions: {total_functions}")
        print(f"   Total classes: {total_classes}")
        
        if executable_scripts:
            print(f"\n🚀 EXECUTABLE SCRIPTS:")
            for script in executable_scripts:
                print(f"   📜 {script}")
        
        self.assessment['python_scripts'] = {
            'summary': {
                'total_files': len(python_files),
                'executable_count': len(executable_scripts),
                'total_functions': total_functions,
                'total_classes': total_classes
            },
            'scripts': script_analysis,
            'executable_scripts': executable_scripts
        }
        
        return script_analysis
    
    def assess_environment(self):
        """Assess Python environment and dependencies"""
        print("\n🐍 ASSESSING ENVIRONMENT")
        print("="*50)
        
        # Basic Python info
        python_info = {
            'version': sys.version,
            'executable': sys.executable,
            'platform': platform.platform(),
            'architecture': platform.architecture()
        }
        
        # Virtual environment check
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        
        env_info = {
            'in_virtual_env': in_venv,
            'virtual_env_path': os.environ.get('VIRTUAL_ENV', 'Not detected')
        }
        
        print(f"🐍 Python: {sys.version.split()[0]}")
        print(f"🔧 Platform: {platform.platform()}")
        print(f"📁 Executable: {sys.executable}")
        print(f"🏠 Virtual Env: {'Yes' if in_venv else 'No'}")
        
        # Get installed packages
        try:
            result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], 
                                  capture_output=True, text=True, check=True)
            packages = json.loads(result.stdout)
            package_dict = {pkg['name'].lower(): pkg['version'] for pkg in packages}
            
            print(f"📦 Installed packages: {len(packages)}")
            
        except Exception as e:
            print(f"❌ Error getting packages: {e}")
            package_dict = {}
        
        # Check key dependencies for EduFruit
        key_dependencies = {
            'tensorflow': 'Deep learning framework',
            'streamlit': 'Web app framework', 
            'opencv-python': 'Computer vision',
            'pillow': 'Image processing',
            'numpy': 'Numerical computing',
            'pandas': 'Data manipulation',
            'matplotlib': 'Plotting',
            'seaborn': 'Statistical plots',
            'scikit-learn': 'ML utilities'
        }
        
        dependency_status = {}
        missing_deps = []
        
        print(f"\n🔍 KEY DEPENDENCIES:")
        for dep, description in key_dependencies.items():
            found = False
            version = None
            
            # Check variations of package names
            for pkg_name, pkg_version in package_dict.items():
                if dep.lower().replace('-', '') in pkg_name.replace('-', ''):
                    found = True
                    version = pkg_version
                    break
            
            dependency_status[dep] = {
                'installed': found,
                'version': version,
                'description': description
            }
            
            if found:
                print(f"   ✅ {dep}: {version}")
            else:
                print(f"   ❌ {dep}: NOT FOUND")
                missing_deps.append(dep)
        
        self.assessment['environment'] = {
            'python_info': python_info,
            'virtual_env': env_info,
            'packages': package_dict,
            'key_dependencies': dependency_status,
            'missing_dependencies': missing_deps
        }
        
        return dependency_status
    
    def assess_data_structure(self):
        """Assess data directories and content"""
        print("\n📊 ASSESSING DATA STRUCTURE")
        print("="*50)
        
        data_assessment = {}
        
        # Look for data directories
        data_patterns = ['data', 'dataset', 'images']
        found_data_dirs = []
        
        for root, dirs, files in os.walk(self.project_root):
            for dir_name in dirs:
                if any(pattern in dir_name.lower() for pattern in data_patterns):
                    data_dir = Path(root) / dir_name
                    rel_path = data_dir.relative_to(self.project_root)
                    found_data_dirs.append(rel_path)
        
        print(f"📁 Found data directories: {len(found_data_dirs)}")
        
        for data_dir in found_data_dirs:
            full_path = self.project_root / data_dir
            print(f"\n📂 Analyzing: {data_dir}")
            
            # Count files and subdirectories
            total_files = 0
            total_size = 0
            subdirs = []
            file_types = {}
            
            for root, dirs, files in os.walk(full_path):
                # Count subdirectories at first level
                if root == str(full_path):
                    subdirs = dirs.copy()
                
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        file_size = os.path.getsize(file_path)
                        total_size += file_size
                        total_files += 1
                        
                        ext = Path(file).suffix.lower()
                        file_types[ext] = file_types.get(ext, 0) + 1
                        
                    except (OSError, FileNotFoundError):
                        continue
            
            data_info = {
                'total_files': total_files,
                'total_size_mb': total_size / (1024 * 1024),
                'subdirectories': subdirs,
                'file_types': file_types
            }
            
            print(f"   📄 Files: {total_files:,}")
            print(f"   💾 Size: {total_size / (1024 * 1024):.2f} MB")
            print(f"   📁 Subdirs: {subdirs}")
            
            # Check if it looks like ML dataset
            has_train = any('train' in subdir.lower() for subdir in subdirs)
            has_test = any('test' in subdir.lower() for subdir in subdirs)
            has_images = '.jpg' in file_types or '.png' in file_types
            
            if has_train and has_test and has_images:
                print(f"   🎯 Looks like ML dataset (Train/Test structure)")
                data_info['dataset_type'] = 'ML_dataset'
            elif has_images:
                print(f"   🖼️ Contains images")
                data_info['dataset_type'] = 'image_collection'
            
            data_assessment[str(data_dir)] = data_info
        
        self.assessment['data_structure'] = data_assessment
        return data_assessment
    
    def assess_models(self):
        """Assess model files and structure"""
        print("\n🧠 ASSESSING MODELS")
        print("="*50)
        
        model_files = []
        model_extensions = ['.h5', '.pkl', '.joblib', '.pt', '.pth', '.onnx']
        
        # Find model files
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if any(file.lower().endswith(ext) for ext in model_extensions):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.project_root)
                    
                    file_info = {
                        'path': str(rel_path),
                        'size_mb': file_path.stat().st_size / (1024 * 1024),
                        'extension': file_path.suffix,
                        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    }
                    
                    model_files.append(file_info)
        
        print(f"🧠 Found model files: {len(model_files)}")
        
        for model in model_files:
            print(f"   📁 {model['path']}")
            print(f"      Size: {model['size_mb']:.2f} MB")
            print(f"      Modified: {model['modified']}")
            
            # Try to get more info for TensorFlow models
            if model['extension'] == '.h5':
                try:
                    import tensorflow as tf
                    model_path = self.project_root / model['path']
                    
                    # Load model info without full loading
                    print(f"      🔍 TensorFlow model detected")
                    
                except Exception as e:
                    print(f"      ⚠️ Could not analyze TF model: {e}")
        
        self.assessment['models'] = {
            'count': len(model_files),
            'files': model_files
        }
        
        return model_files
    
    def assess_streamlit_app(self):
        """Assess Streamlit application structure"""
        print("\n🌐 ASSESSING STREAMLIT APP")
        print("="*50)
        
        streamlit_files = []
        app_structure = {}
        
        # Look for Streamlit files
        for root, dirs, files in os.walk(self.project_root):
            for file in files:
                if file.endswith('.py'):
                    file_path = Path(root) / file
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Check if it's a Streamlit app
                        if 'streamlit' in content.lower() or 'import st' in content:
                            rel_path = file_path.relative_to(self.project_root)
                            
                            # Analyze Streamlit features
                            features = []
                            if 'st.file_uploader' in content:
                                features.append('file_upload')
                            if 'st.camera_input' in content:
                                features.append('camera_input')
                            if 'st.selectbox' in content or 'st.radio' in content:
                                features.append('user_input')
                            if 'st.image' in content:
                                features.append('image_display')
                            if 'st.write' in content or 'st.markdown' in content:
                                features.append('text_output')
                            
                            streamlit_info = {
                                'path': str(rel_path),
                                'size_kb': file_path.stat().st_size / 1024,
                                'features': features,
                                'lines': len(content.splitlines())
                            }
                            
                            streamlit_files.append(streamlit_info)
                            
                    except Exception as e:
                        continue
        
        print(f"🌐 Found Streamlit files: {len(streamlit_files)}")
        
        for app_file in streamlit_files:
            print(f"   📱 {app_file['path']}")
            print(f"      Size: {app_file['size_kb']:.1f} KB")
            print(f"      Features: {', '.join(app_file['features']) if app_file['features'] else 'Basic'}")
        
        # Look for streamlit config
        config_files = []
        for config_name in ['.streamlit/config.toml', 'streamlit_config.toml']:
            config_path = self.project_root / config_name
            if config_path.exists():
                config_files.append(str(config_path.relative_to(self.project_root)))
        
        if config_files:
            print(f"⚙️ Config files: {config_files}")
        
        self.assessment['streamlit_app'] = {
            'app_files': streamlit_files,
            'config_files': config_files,
            'has_app': len(streamlit_files) > 0
        }
        
        return streamlit_files
    
    def assess_documentation(self):
        """Assess documentation and README files"""
        print("\n📖 ASSESSING DOCUMENTATION")
        print("="*50)
        
        doc_files = []
        doc_extensions = ['.md', '.txt', '.rst', '.pdf']
        
        # Find documentation files
        for root, dirs, files in os.walk(self.project_root):
            # Skip deep nested directories
            depth = len(Path(root).relative_to(self.project_root).parts)
            if depth > 3:
                continue
                
            for file in files:
                if any(file.lower().endswith(ext) for ext in doc_extensions):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.project_root)
                    
                    doc_info = {
                        'path': str(rel_path),
                        'size_kb': file_path.stat().st_size / 1024,
                        'type': 'README' if 'readme' in file.lower() else 'documentation'
                    }
                    
                    doc_files.append(doc_info)
        
        print(f"📖 Found documentation files: {len(doc_files)}")
        
        readme_files = [doc for doc in doc_files if doc['type'] == 'README']
        other_docs = [doc for doc in doc_files if doc['type'] != 'README']
        
        if readme_files:
            print(f"📝 README files:")
            for readme in readme_files:
                print(f"   📄 {readme['path']} ({readme['size_kb']:.1f} KB)")
        else:
            print(f"⚠️ No README file found")
        
        if other_docs:
            print(f"📚 Other documentation:")
            for doc in other_docs:
                print(f"   📄 {doc['path']} ({doc['size_kb']:.1f} KB)")
        
        self.assessment['documentation'] = {
            'total_files': len(doc_files),
            'readme_files': readme_files,
            'other_docs': other_docs,
            'has_readme': len(readme_files) > 0
        }
        
        return doc_files
    
    def assess_requirements_files(self):
        """Assess requirements and dependency files"""
        print("\n📦 ASSESSING REQUIREMENTS FILES")
        print("="*50)
        
        req_patterns = [
            'requirements.txt',
            'requirements*.txt', 
            'environment.yml',
            'Pipfile',
            'pyproject.toml',
            'setup.py'
        ]
        
        found_files = []
        
        for pattern in req_patterns:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file():
                    rel_path = file_path.relative_to(self.project_root)
                    
                    file_info = {
                        'path': str(rel_path),
                        'size_kb': file_path.stat().st_size / 1024,
                        'type': self._classify_req_file(file_path.name)
                    }
                    
                    # Try to count dependencies
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        if file_path.name.startswith('requirements'):
                            deps = [line.strip() for line in content.splitlines() 
                                   if line.strip() and not line.startswith('#')]
                            file_info['dependency_count'] = len(deps)
                        
                    except Exception:
                        file_info['dependency_count'] = 'unknown'
                    
                    found_files.append(file_info)
        
        print(f"📦 Found dependency files: {len(found_files)}")
        
        for req_file in found_files:
            print(f"   📄 {req_file['path']} ({req_file['type']})")
            if 'dependency_count' in req_file:
                print(f"      Dependencies: {req_file['dependency_count']}")
        
        if not found_files:
            print("⚠️ No requirements files found - consider creating requirements.txt")
        
        self.assessment['requirements'] = {
            'files': found_files,
            'has_requirements': len(found_files) > 0
        }
        
        return found_files
    
    def _classify_req_file(self, filename):
        """Classify requirement file type"""
        if filename.startswith('requirements'):
            return 'pip_requirements'
        elif filename == 'environment.yml':
            return 'conda_environment'
        elif filename == 'Pipfile':
            return 'pipenv'
        elif filename == 'pyproject.toml':
            return 'poetry'
        elif filename == 'setup.py':
            return 'setuptools'
        else:
            return 'unknown'
    
    def generate_summary_report(self):
        """Generate comprehensive summary report"""
        print("\n" + "="*80)
        print("📊 PROJECT ASSESSMENT SUMMARY")
        print("="*80)
        
        # File structure summary
        if 'file_structure' in self.assessment:
            fs = self.assessment['file_structure']['summary']
            print(f"\n📁 FILE STRUCTURE:")
            print(f"   Total files: {fs['total_files']:,}")
            print(f"   Total size: {fs['total_size_mb']:.2f} MB")
            print(f"   Directories: {fs['directory_count']}")
        
        # Python scripts summary
        if 'python_scripts' in self.assessment:
            ps = self.assessment['python_scripts']['summary']
            print(f"\n🐍 PYTHON SCRIPTS:")
            print(f"   Python files: {ps['total_files']}")
            print(f"   Executable scripts: {ps['executable_count']}")
            print(f"   Functions: {ps['total_functions']}")
            print(f"   Classes: {ps['total_classes']}")
        
        # Environment summary
        if 'environment' in self.assessment:
            env = self.assessment['environment']
            missing = len(env['missing_dependencies'])
            total_deps = len(env['key_dependencies'])
            print(f"\n🔧 ENVIRONMENT:")
            print(f"   Virtual environment: {'Yes' if env['virtual_env']['in_virtual_env'] else 'No'}")
            print(f"   Key dependencies: {total_deps - missing}/{total_deps} installed")
            if missing > 0:
                print(f"   Missing: {', '.join(env['missing_dependencies'])}")
        
        # Data summary
        if 'data_structure' in self.assessment:
            data_dirs = len(self.assessment['data_structure'])
            print(f"\n📊 DATA:")
            print(f"   Data directories: {data_dirs}")
            
            total_data_size = sum(info['total_size_mb'] for info in self.assessment['data_structure'].values())
            print(f"   Total data size: {total_data_size:.2f} MB")
        
        # Models summary
        if 'models' in self.assessment:
            models = self.assessment['models']
            print(f"\n🧠 MODELS:")
            print(f"   Model files: {models['count']}")
            if models['files']:
                total_model_size = sum(m['size_mb'] for m in models['files'])
                print(f"   Total model size: {total_model_size:.2f} MB")
        
        # Streamlit summary
        if 'streamlit_app' in self.assessment:
            st_app = self.assessment['streamlit_app']
            print(f"\n🌐 STREAMLIT APP:")
            print(f"   Has Streamlit app: {'Yes' if st_app['has_app'] else 'No'}")
            print(f"   App files: {len(st_app['app_files'])}")
        
        # Documentation summary
        if 'documentation' in self.assessment:
            docs = self.assessment['documentation']
            print(f"\n📖 DOCUMENTATION:")
            print(f"   Has README: {'Yes' if docs['has_readme'] else 'No'}")
            print(f"   Documentation files: {docs['total_files']}")
        
        # Requirements summary
        if 'requirements' in self.assessment:
            reqs = self.assessment['requirements']
            print(f"\n📦 REQUIREMENTS:")
            print(f"   Has requirements files: {'Yes' if reqs['has_requirements'] else 'No'}")
            print(f"   Dependency files: {len(reqs['files'])}")
        
        print("\n" + "="*80)
    
    def save_full_report(self):
        """Save complete assessment to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.project_root / f"project_assessment_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(self.assessment, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Full assessment saved to: {report_file}")
        return report_file
    
    def run_complete_assessment(self):
        """Run all assessment modules"""
        print("🚀 Running complete project assessment...")
        
        # Run all assessments
        self.assess_file_structure()
        self.assess_python_scripts()
        self.assess_environment()
        self.assess_data_structure()
        self.assess_models()
        self.assess_streamlit_app()
        self.assess_documentation()
        self.assess_requirements_files()
        
        # Generate summary
        self.generate_summary_report()
        
        # Save report
        report_file = self.save_full_report()
        
        print(f"\n✅ Complete assessment finished!")
        print(f"📄 Detailed report: {report_file}")
        
        return self.assessment

def main():
    """Main assessment function"""
    print("🔍" * 30)
    print("🔍 EDUFRUIT PROJECT COMPLETE ASSESSMENT")
    print("🔍" * 30)
    
    assessor = EduFruitProjectAssessment()
    assessment = assessor.run_complete_assessment()
    
    print("\n💡 Use this assessment to:")
    print("   📝 Write an accurate README file")
    print("   🔧 Fix missing dependencies")
    print("   📁 Organize project structure")
    print("   🧹 Clean up unnecessary files")
    print("   📦 Create proper requirements.txt")
    print("   🚀 Prepare for deployment")

if __name__ == "__main__":
    main()