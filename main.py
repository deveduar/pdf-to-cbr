import os
from pdf2image import convert_from_path
from PIL import Image
import argparse
from tqdm import tqdm
import sys

def get_poppler_path():
    """Obtiene la ruta de Poppler basada en el sistema"""
    # Ajusta esta ruta según donde hayas instalado Poppler
    default_paths = [
        r"C:\Program Files\poppler-23.11.0\Library\bin",
        r"C:\Program Files\poppler\bin",
        r"C:\Poppler\bin",
        r"C:\poppler\Library\bin"
    ]
    
    # Buscar en las rutas predeterminadas
    for path in default_paths:
        if os.path.exists(path):
            return path
            
    # Si no se encuentra, pedir al usuario
    print("No se encontró Poppler en las rutas predeterminadas.")
    print("Por favor, introduce la ruta completa a la carpeta bin de Poppler:")
    user_path = input().strip()
    
    if os.path.exists(user_path):
        return user_path
    else:
        raise FileNotFoundError("No se pudo encontrar Poppler. Por favor, verifica la instalación.")

def convert_pdf_to_jpeg(pdf_path, output_dir, dpi=300, quality=95):
    """
    Convierte un archivo PDF a imágenes JPEG de alta calidad.
    """
    try:
        # Verificar que el archivo PDF existe
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")
            
        # Crear el directorio de salida si no existe
        os.makedirs(output_dir, exist_ok=True)
            
        # Obtener el nombre base del archivo
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        
        print(f"Convirtiendo {pdf_path}...")
        print("Este proceso puede tardar varios minutos dependiendo del tamaño del PDF...")
        
        # Obtener la ruta de Poppler
        poppler_path = get_poppler_path()
        print(f"Usando Poppler desde: {poppler_path}")
        
        # Convertir PDF a imágenes con timeout más largo
        images = convert_from_path(
            pdf_path,
            dpi=dpi,
            poppler_path=poppler_path,
            timeout=120,  # Aumentar timeout a 120 segundos
            fmt='jpeg',   # Especificar formato
            thread_count=4  # Usar múltiples hilos
        )
        
        print(f"PDF convertido. Procesando {len(images)} páginas...")
        
        # Guardar cada página como JPEG
        for i, image in enumerate(tqdm(images, desc="Guardando imágenes")):
            # Convertir a modo RGB si es necesario
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Nombre del archivo de salida
            output_file = os.path.join(output_dir, f"{pdf_name}_pagina_{i+1}.jpg")
            
            # Guardar la imagen con alta calidad
            image.save(
                output_file,
                'JPEG',
                quality=quality,
                optimize=True,
                progressive=True
            )
        
        print(f"\n¡Conversión completada!")
        print(f"Se han guardado {len(images)} páginas en: {os.path.abspath(output_dir)}")
        
    except KeyboardInterrupt:
        print("\nProceso interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError durante la conversión: {str(e)}")
        print("Asegúrate de que:")
        print("1. Poppler está instalado correctamente")
        print("2. La ruta de Poppler está en las variables de entorno o especificada correctamente")
        print("3. El archivo PDF no está corrupto o protegido")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Convertir PDF a JPEG de alta calidad')
    parser.add_argument('pdf_path', help='Ruta al archivo PDF')
    parser.add_argument('--output-dir', default='output', help='Directorio de salida')
    parser.add_argument('--dpi', type=int, default=300, help='Resolución (DPI)')
    parser.add_argument('--quality', type=int, default=95, help='Calidad JPEG (1-95)')
    
    args = parser.parse_args()
    
    convert_pdf_to_jpeg(args.pdf_path, args.output_dir, args.dpi, args.quality)

if __name__ == "__main__":
    main()