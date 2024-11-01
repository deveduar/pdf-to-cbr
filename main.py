import os
from pdf2image import convert_from_path
from PIL import Image
import argparse
from tqdm import tqdm
import sys
import time
import zipfile
import shutil

def handle_error(message, exception=None):
    """Maneja y muestra errores de forma centralizada."""
    if exception:
        print(f"\n{message}: {str(exception)}")
    else:
        print(f"\n{message}")

def get_poppler_path():
    """Obtiene la ruta de Poppler dentro del directorio del proyecto."""
    project_poppler_path = os.path.join(os.path.dirname(__file__), "poppler", "Library/bin")
    
    if os.path.exists(project_poppler_path):
        return project_poppler_path
    else:
        raise FileNotFoundError("No se pudo encontrar Poppler en el directorio del proyecto.")

def check_overwrite(cbr_path):
    """Confirma la sobrescritura si el archivo ya existe."""
    if os.path.exists(cbr_path):
        overwrite = input(f"El archivo '{cbr_path}' ya existe. ¿Deseas sobrescribirlo? (s/n): ").strip().lower()
        if overwrite != 's':
            print("Operación cancelada por el usuario.")
            return False
    return True

def prepare_directories(output_dir, temp_img_dir):
    """Crea directorios de salida y temporales si no existen."""
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(temp_img_dir, exist_ok=True)

def convert_pdf_to_images(pdf_path, dpi):
    """Convierte el PDF a una lista de imágenes."""
    poppler_path = get_poppler_path()  # Asegurarse de definir esta función
    print(f"Usando Poppler desde: {poppler_path}")
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path, fmt='jpeg')
    return images

def save_images_as_jpeg(images, temp_img_dir, pdf_name, quality):
    """Guarda cada imagen en el directorio temporal como archivo JPEG."""
    for i, image in enumerate(tqdm(images, desc="Guardando imágenes", unit="página")):
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(os.path.join(temp_img_dir, f"{pdf_name}_page_{i+1}.jpg"), 'JPEG', quality=quality)

def create_cbr(zip_path, cbr_path, temp_img_dir):
    """Crea un archivo ZIP con las imágenes y lo renombra a CBR."""
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for img_file in os.listdir(temp_img_dir):
            zipf.write(os.path.join(temp_img_dir, img_file), img_file)
    if os.path.exists(cbr_path):
        os.remove(cbr_path)
    os.rename(zip_path, cbr_path)

def convert_pdf_to_jpeg(pdf_path, output_dir, dpi=300, quality=95):
    """Convierte un archivo PDF a un archivo CBR que contiene las imágenes JPEG de cada página."""
    try:
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")

        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        cbr_path = os.path.join(output_dir, f"{pdf_name}.cbr")
        temp_img_dir = os.path.join(output_dir, f"{pdf_name}_temp")
        zip_path = os.path.join(output_dir, f"{pdf_name}.zip")

        # Confirmar sobrescritura si es necesario
        if not check_overwrite(cbr_path):
            return

        # Preparar directorios
        prepare_directories(output_dir, temp_img_dir)

        # Mostrar información de conversión
        print(f"\nIniciando conversión de: {pdf_path}")
        print(f"Resolución solicitada: {dpi} DPI")
        print(f"Calidad JPEG: {quality}")
        
        # Convertir PDF a imágenes
        start_time = time.time()
        images = convert_pdf_to_images(pdf_path, dpi)
        print(f"\nConversión completada en {time.time() - start_time:.1f} segundos")
        
        # Guardar imágenes como JPEG
        save_images_as_jpeg(images, temp_img_dir, pdf_name, quality)

        # Crear archivo CBR
        create_cbr(zip_path, cbr_path, temp_img_dir)
        
        # Eliminar archivos temporales
        shutil.rmtree(temp_img_dir)
        
        print(f"\n¡Conversión completada! Archivo CBR guardado en: {cbr_path}")
        
    except KeyboardInterrupt:
        handle_error("Proceso interrumpido por el usuario.")
        raise
    except FileNotFoundError as fnf_error:
        handle_error("Error de archivo", fnf_error)
    except Exception as e:
        handle_error("Error durante la conversión", e)

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
