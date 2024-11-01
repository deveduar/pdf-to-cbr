import unittest
import os
from unittest.mock import patch, MagicMock
from main import get_poppler_path, convert_pdf_to_jpeg

class TestPDFConversion(unittest.TestCase):

    @patch("os.path.exists", return_value=True)
    def test_get_poppler_path_relative(self, mock_exists):
        # Probamos que la ruta relativa de Poppler se obtiene correctamente
        expected_path = os.path.join(os.path.dirname(__file__), "poppler", "bin")
        path = get_poppler_path()
        self.assertEqual(path, expected_path)

    @patch("main.convert_from_path")
    @patch("os.makedirs")
    @patch("os.path.exists", return_value=True)
    def test_convert_pdf_to_jpeg(self, mock_exists, mock_makedirs, mock_convert):
        mock_convert.return_value = [MagicMock() for _ in range(5)]
        
        pdf_path = "test.pdf"
        output_dir = "output"
        dpi = 100
        quality = 50

        try:
            convert_pdf_to_jpeg(pdf_path, output_dir, dpi, quality)
        except FileNotFoundError:
            self.fail("convert_pdf_to_jpeg lanzó FileNotFoundError inesperadamente.")

    @patch("main.convert_from_path", side_effect=FileNotFoundError)
    def test_convert_pdf_to_jpeg_file_not_found(self, mock_convert):
        with self.assertRaises(FileNotFoundError):
            convert_pdf_to_jpeg("nonexistent.pdf", "output")

if __name__ == '__main__':
    unittest.main()
