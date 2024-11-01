import unittest
from unittest.mock import patch, MagicMock
import os
import shutil
from main import get_poppler_path, convert_pdf_to_jpeg

class TestPDFConversion(unittest.TestCase):

    @patch("os.path.exists")
    def test_get_poppler_path_exists(self, mock_exists):
        mock_exists.return_value = True
        expected_path = os.path.join(os.path.dirname(__file__), "poppler", "Library/bin")
        path = get_poppler_path()
        self.assertEqual(path, expected_path)

    @patch("os.path.exists", side_effect=lambda path: path != "nonexistent.pdf")
    def test_convert_pdf_to_jpeg_file_not_found(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            convert_pdf_to_jpeg("nonexistent.pdf", "output")

    @patch("os.makedirs")
    @patch("os.path.exists", side_effect=lambda path: path == "output/test.cbr")
    @patch("os.remove")
    @patch("pdf2image.convert_from_path")
    @patch("os.listdir", return_value=["image1.jpg", "image2.jpg"])
    @patch("zipfile.ZipFile")
    @patch("shutil.rmtree")
    def test_convert_pdf_to_jpeg_overwrite(self, mock_rmtree, mock_zipfile, mock_listdir, mock_convert, mock_remove, mock_exists, mock_makedirs):
        mock_convert.return_value = [MagicMock(), MagicMock()]  # Simula que se generaron 2 imágenes
        pdf_path = "test.pdf"
        output_dir = "output"

        # Patching `input` para forzar la respuesta sin interacción
        with patch('builtins.input', return_value='s'):
            convert_pdf_to_jpeg(pdf_path, output_dir)

        # Verifica que se llamó a os.remove para eliminar el CBR existente
        mock_remove.assert_called_once_with("output/test.cbr")
        # Verifica que se crea el ZIP
        mock_zipfile.assert_called_once()

    @patch("os.makedirs")
    @patch("pdf2image.convert_from_path")
    @patch("zipfile.ZipFile")
    @patch("os.listdir", return_value=["image1.jpg", "image2.jpg"])
    def test_convert_pdf_to_jpeg_success(self, mock_listdir, mock_zipfile, mock_convert, mock_makedirs):
        mock_convert.return_value = [MagicMock(), MagicMock()]  # Simula que se generaron 2 imágenes
        pdf_path = "test.pdf"
        output_dir = "output"

        convert_pdf_to_jpeg(pdf_path, output_dir)

        # Verifica que se llamó a convert_from_path con los argumentos correctos
        mock_convert.assert_called_once_with(pdf_path, dpi=300, poppler_path=get_poppler_path(), fmt='jpeg')
        # Verifica que se crea el ZIP
        mock_zipfile.assert_called_once()

if __name__ == '__main__':
    unittest.main()
