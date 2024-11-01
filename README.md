# PDF to CBR Converter 🖼️📄

## Description
A Python script to convert PDF files to CBR (Comic Book RAR) format, perfect for digital comic and manga readers.

## Prerequisites
- Python 3.7+ 
- [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows?tab=readme-ov-file)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/pdf-to-cbr.git
cd pdf-to-cbr
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download and Install Poppler:
   - Download Poppler binaries for Windows
   - Extract contents into the project folder

## Usage

### Basic Usage
```bash
python main.py "path/to/file.pdf"
```

### Advanced Options
```bash
python main.py "path/to/file.pdf" --output-dir images --dpi 300 --quality 95
```

#### Parameters
- `path/to/file.pdf`: Path to the PDF file to convert
- `--output-dir`: Output directory for images (default: `output`)
- `--dpi`: Image resolution (default: 300)
- `--quality`: JPEG compression quality (default: 95, range 1-100)

## Examples

### Convert PDF with default settings
```bash
python main.py "D:/Manga/chapter1.pdf"
```

### Convert with custom configuration
```bash
python main.py "D:/Manga/chapter2.pdf" --output-dir my_images --dpi 600 --quality 90
```

## Roadmap
- [x] Convert to ZIP and CBR
- [ ] Fix 600 DPI quality issues
- [ ] User-friendly web interface
- [ ] Loading improvements and color enhancements
- [ ] Support for filenames and paths with special characters

## Troubleshooting
- Ensure Poppler is correctly installed and added to system PATH
- Check Python version compatibility
- Verify input PDF file integrity

## Contributing
Contributions are welcome! Please:
- Open an issue to discuss proposed changes
- Create a pull request with detailed description
- Follow project coding standards

