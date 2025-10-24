# Placeholder file
"""
NewsTrace Model Download Script
Download spaCy and NLTK models
"""

import sys
import subprocess


def download_spacy_model():
    """Download spaCy model"""
    print("📥 Downloading spaCy model...")
    try:
        subprocess.run([
            sys.executable, '-m', 'spacy', 'download', 'en_core_web_sm'
        ], check=True)
        print("✅ spaCy model downloaded")
        return True
    except Exception as e:
        print(f"❌ Failed to download spaCy model: {e}")
        return False


def download_nltk_data():
    """Download NLTK data"""
    print("📥 Downloading NLTK data...")
    try:
        import nltk
        
        packages = ['punkt', 'stopwords', 'wordnet', 'averaged_perceptron_tagger']
        
        for package in packages:
            print(f"  Downloading {package}...")
            nltk.download(package, quiet=True)
        
        print("✅ NLTK data downloaded")
        return True
    except Exception as e:
        print(f"❌ Failed to download NLTK data: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("📦 NewsTrace Model Download")
    print("=" * 60)
    print()
    
    success = True
    
    # Download spaCy model
    if not download_spacy_model():
        success = False
    
    print()
    
    # Download NLTK data
    if not download_nltk_data():
        success = False
    
    print()
    
    if success:
        print("✅ All models downloaded successfully!")
    else:
        print("⚠️  Some downloads failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
