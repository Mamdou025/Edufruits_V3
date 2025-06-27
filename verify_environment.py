#!/usr/bin/env python3
"""
EduFruit Environment Verification Script
Run this to verify your environment is set up correctly
"""

import sys
import importlib
import subprocess

def check_python_version():
    """Check Python version"""
    print("🐍 Python Version Check:")
    print(f"   Current: {sys.version.split()[0]}")
    
    major, minor = sys.version_info[:2]
    if major >= 3 and minor >= 8:
        print("   ✅ Python version is compatible")
        return True
    else:
        print("   ❌ Python 3.8+ required")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed and importable"""
    if import_name is None:
        import_name = package_name
    
    try:
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', 'Unknown')
        print(f"   ✅ {package_name}: {version}")
        return True
    except ImportError:
        print(f"   ❌ {package_name}: NOT INSTALLED")
        return False

def main():
    """Main verification function"""
    print("🔧" * 20)
    print("🔧 EDUFRUIT ENVIRONMENT VERIFICATION")
    print("🔧" * 20)
    
    all_good = True
    
    # Check Python version
    all_good &= check_python_version()
    
    # Check core packages
    print("\n📦 Package Check:")
    packages = [
        ('tensorflow', 'tensorflow'),
        ('streamlit', 'streamlit'),
        ('opencv-python', 'cv2'),
        ('pillow', 'PIL'),
        ('numpy', 'numpy'),
        ('pandas', 'pandas'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('scikit-learn', 'sklearn'),
        ('psutil', 'psutil')
    ]
    
    for package_name, import_name in packages:
        all_good &= check_package(package_name, import_name)
    
    # Test basic functionality
    print("\n🧪 Functionality Tests:")
    
    try:
        import tensorflow as tf
        # Simple TensorFlow test
        tf.constant([1, 2, 3])
        print("   ✅ TensorFlow: Basic operations work")
    except Exception as e:
        print(f"   ❌ TensorFlow: Error - {e}")
        all_good = False
    
    try:
        import cv2
        import numpy as np
        # Simple OpenCV test
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.resize(img, (50, 50))
        print("   ✅ OpenCV: Image operations work")
    except Exception as e:
        print(f"   ❌ OpenCV: Error - {e}")
        all_good = False
    
    try:
        import streamlit as st
        print("   ✅ Streamlit: Import successful")
    except Exception as e:
        print(f"   ❌ Streamlit: Error - {e}")
        all_good = False
    
    # Final result
    print("\n" + "="*50)
    if all_good:
        print("🎉 ENVIRONMENT VERIFICATION PASSED!")
        print("✅ Your environment is ready for EduFruit!")
    else:
        print("❌ ENVIRONMENT VERIFICATION FAILED!")
        print("⚠️ Please install missing packages and try again")
        print("💡 Run: pip install -r requirements.txt")
    print("="*50)

if __name__ == "__main__":
    main()
