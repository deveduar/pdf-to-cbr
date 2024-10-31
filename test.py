# test_imports.py
try:
    import os
    print("✓ os está disponible")
    
    from pdf2image import convert_from_path
    print("✓ pdf2image está instalado")
    
    from PIL import Image
    print("✓ Pillow está instalado")
    
    import argparse
    print("✓ argparse está disponible")
    
    from tqdm import tqdm
    print("✓ tqdm está instalado")
    
    print("\nTodas las librerías están instaladas correctamente!")
except ImportError as e:
    print(f"Error importando: {str(e)}")