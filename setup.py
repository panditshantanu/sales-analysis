"""
Setup Script for Sales Data Analysis Project
Run this script to install packages and generate sample data.
"""

import subprocess
import sys
import os

def install_packages():
    """Install required Python packages."""
    print("📦 Installing required packages...")
    
    packages = [
        'pandas>=2.1.0',
        'numpy>=1.24.0', 
        'matplotlib>=3.7.0',
        'seaborn>=0.12.0',
        'plotly>=5.15.0',
        'jupyter>=1.0.0',
        'openpyxl>=3.1.0',
        'faker>=19.0.0'
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
        except subprocess.CalledProcessError as e:
            print(f"❌ Error installing {package}: {e}")
            return False
    
    print("✅ All packages installed successfully!")
    return True

def generate_sample_data():
    """Generate sample sales data."""
    print("🎲 Generating sample sales data...")
    
    try:
        current_dir = os.path.dirname(__file__)
        data_dir_name = 'data'
        data_dir_full_path = os.path.join(current_dir,data_dir_name)

        if not os.path.exists(data_dir_full_path):
            os.makedirs(data_dir_full_path)
        
        sys.path.append(current_dir)

        from data.sample_data_generator import main as generate_data
        generate_data()
        print("✅ Sample data generated successfully!")
        return True
    except Exception as e:
        print(f"❌ Error generating data: {e}")
        print("💡 You can run 'python data/sample_data_generator.py' manually")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up Sales Data Analysis Project")
    print("="*50)
    
    # Install packages
    if not install_packages():
        print("❌ Package installation failed. Please install manually.")
        return
    
    # Generate sample data
    if not generate_sample_data():
        print("❌ Data generation failed. Please run manually.")
        return
    
    print("\n✨ Setup complete!")
    print("📁 Your project is ready to use!")
    print("\n🚀 Next steps:")
    print("1. Open 'notebooks/01_data_exploration.ipynb' in Jupyter")
    print("2. Run all cells to start your analysis journey")
    print("3. Try the practice exercises")
    print("4. Explore other notebooks for advanced topics")
    
    print("\n💡 To start Jupyter:")
    print("   jupyter notebook notebooks/")

if __name__ == "__main__":
    main()
