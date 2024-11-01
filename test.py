import unittest
import os
from unittest.mock import patch, MagicMock
from main import handle_error, get_poppler_path, check_overwrite, prepare_directories, convert_pdf_to_images

class TestPDFConversionFunctions(unittest.TestCase):

    def test_handle_error_with_exception(self):
        with patch('builtins.print') as mock_print:
            handle_error("Test error", Exception("Exception message"))
            mock_print.assert_called_with("\nTest error: Exception message")
    
    def test_handle_error_without_exception(self):
        with patch('builtins.print') as mock_print:
            handle_error("Test error")
            mock_print.assert_called_with("\nTest error")

    @patch("os.path.exists", return_value=True)
    def test_get_poppler_path_exists(self, mock_exists):
        path = get_poppler_path()
        expected_path = os.path.join(os.path.dirname(__file__), "poppler", "Library/bin")
        self.assertEqual(path, expected_path)
        mock_exists.assert_called_once()  # Asegurarse de que se llame a exists

    @patch("os.path.exists", return_value=False)
    def test_get_poppler_path_not_exists(self, mock_exists):
        with self.assertRaises(FileNotFoundError):
            get_poppler_path()
        mock_exists.assert_called_once()  # Asegurarse de que se llame a exists

    @patch("os.path.exists", return_value=True)
    @patch("builtins.input", return_value="s")
    def test_check_overwrite_yes(self, mock_input, mock_exists):
        self.assertTrue(check_overwrite("output/test.cbr"))
        mock_exists.assert_called_once()  # Asegurarse de que se llame a exists
        mock_input.assert_called_once()  # Asegurarse de que se llame a input

    @patch("os.path.exists", return_value=True)
    @patch("builtins.input", return_value="n")
    def test_check_overwrite_no(self, mock_input, mock_exists):
        self.assertFalse(check_overwrite("output/test.cbr"))
        mock_exists.assert_called_once()  # Asegurarse de que se llame a exists
        mock_input.assert_called_once()  # Asegurarse de que se llame a input

    @patch("os.makedirs")
    def test_prepare_directories(self, mock_makedirs):
        prepare_directories("output", "temp_dir")
        mock_makedirs.assert_any_call("output", exist_ok=True)
        mock_makedirs.assert_any_call("temp_dir", exist_ok=True)

    @patch("main.get_poppler_path", return_value="poppler_path")
    @patch("pdf2image.convert_from_path")
    def test_convert_pdf_to_images(self, mock_convert, mock_get_poppler):
        # Simulamos la creación de imágenes
        mock_image_1 = MagicMock()
        mock_image_2 = MagicMock()
        mock_convert.return_value = [mock_image_1, mock_image_2]

        images = convert_pdf_to_images("test.pdf", 300)
        
        mock_convert.assert_called_once_with("test.pdf", dpi=300, poppler_path="poppler_path", fmt='jpeg')
        self.assertEqual(len(images), 2)  # Simula que generó 2 imágenes

if __name__ == "__main__":
    unittest.main()
