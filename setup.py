"""
SheSafe Setup Script
This script helps set up the application environment
"""
import os
import sys
import subprocess

def create_env_file():
    """Create .env file from template"""
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("📄 Creating .env file from template...")
            # For Unix-like systems
            if sys.platform != 'win32':
                os.system('cp .env.example .env')
            else:
                os.system('copy .env.example .env')
            print("✅ .env file created. Please edit it with your credentials.")
        else:
            print("❌ .env.example not found")
    else:
        print("✅ .env file already exists")

def check_python_version():
    """Check if Python version is adequate"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def install_dependencies():
    """Install required packages"""
    print("\n📦 Installing dependencies...")
    print("This may take a few minutes as ML models need to be downloaded...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        sys.exit(1)

def create_directories():
    """Create necessary directories"""
    dirs = ['data', 'logs', 'frontend/static/maps']
    for directory in dirs:
        os.makedirs(directory, exist_ok=True)
    print("✅ Directories created")

def main():
    print("🛡️  SheSafe - Women Safety Application Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Ask user if they want to install dependencies
    response = input("\n📦 Install dependencies now? (y/n): ").lower()
    if response == 'y':
        install_dependencies()
    else:
        print("\n⚠️  Skipping dependency installation.")
        print("   Run 'pip install -r requirements.txt' when ready.")
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\n📝 Next steps:")
    print("   1. Edit .env file with your Twilio credentials (optional)")
    print("   2. Run the application: cd backend && python app.py")
    print("   3. Open http://localhost:5000 in your browser")
    print("\n🆘 For help, check README.md")

if __name__ == "__main__":
    main()

