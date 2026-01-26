"""
# `file`

This command gives information on a specific file given as argument
```txt
Opions:
    -m, --metadata              Extracts the metadata of the file if possible.  
    -k key, --keys key          Used combined with `-m`, allows to specify a key (can be used multiple times)
```
"""
from flux.core.interfaces.commands import (
    CommandInterface,
    Parser
)
from typing import Optional, Union
import os
import chardet
from PIL import Image
import mimetypes
import magic
from pydub.utils import mediainfo
from pathlib import Path
import pypdf

# from PIL.ExifTags import TAGS

class Command(CommandInterface):
    def init(self):
        self.parser = Parser(prog="file", description="Gives information on a specific file given as an argument")
        self.parser.add_argument("PATH", help="The path of the file.")
        self.parser.add_argument("-m", "--metadata", help="Extracts metadata from the file if possible.", action="store_true")
        self.parser.add_argument("-k", "--keys", help="Used combined with `-m`, allows filtering keys (can be used multiple times)", action="append")

    def run(self):
        self.errors.value = self.args.PATH


        if not os.path.exists(self.args.PATH):
            self.error(self.errors.file_not_found())
            return

        self.args.PATH = Path(self.args.PATH)

        if self.args.metadata:
            info = self.get_metadata(self.args.PATH, self.args.keys)
        else:
            try:
                info = self.file_info(self.args.PATH)
            except PermissionError:
                self.error(self.errors.permission_denied())
                return

        if info is None:
            self.parser.exit_execution = True
            return

        self.print(info + "\n")

    def file_info(self, filepath: Union[str, Path]) -> str:
        """
        Gets file information
        """
        mime_type, _ = mimetypes.guess_type(str(filepath))

        file_type = ""
        if os.path.islink(filepath):
            file_type += "symbolic link to "
        elif os.path.isfile(filepath):
            file_type += "regular file"
        elif os.path.isdir(filepath):
            file_type += "directory"
        else:
            file_type += "unknown"

        try:
            file_size = os.path.getsize(filepath)
        except OSError as e:
            self.error(f"Error getting file size: {e}")
            return

        return f"{filepath}: {file_type}{f', {mime_type}' if mime_type else ''}, {oct(os.stat(filepath).st_mode)[-3:]}, {file_size} bytes"

    def get_metadata(self, path, keys: list = []) -> Optional[str]:
        """
        Retrieve metadata from a file

        ### Supported Types
        - Images (JPEG, TIFF, PNG, GIF, BMP, WebP, etc.)
        - PDF (.pdf)
        - Microsoft Office documents (.docx, .xlsx, .pptx)
        - Audio files (MP3, WAV, FLAC, etc.)
        - Executables (PE, ELF, etc.)
        """
        mime_type, _ = mimetypes.guess_type(str(path))
        file_extension = path.suffix.lower()

        if mime_type is not None:
            mime_type = mime_type.lower()

        if mime_type == "image/jpeg" or file_extension in {".jpg", ".jpeg"}:
            # Extract metadata from JPEG images
            return self.extract_metadata_from_image(path, keys)
        elif mime_type == "image/tiff" or file_extension in {".tif", ".tiff"}:
            # Extract metadata from TIFF images
            return self.extract_metadata_from_image(path, keys)
        elif mime_type == "image/png" or file_extension == ".png":
            # Extract metadata from PNG images
            return self.extract_metadata_from_image(path, keys)
        elif mime_type == "image/gif" or file_extension == ".gif":
            # Extract metadata from GIF images
            return self.extract_metadata_from_image(path, keys)
        elif mime_type == "image/bmp" or file_extension == ".bmp":
            # Extract metadata from BMP images
            return self.extract_metadata_from_image(path, keys)
        elif mime_type == "image/webp" or file_extension == ".webp":
            # Extract metadata from WebP images
            return self.extract_metadata_from_image(path, keys)
        elif mime_type == "application/pdf" or file_extension == ".pdf":
            # Extract metadata from PDF files
            return self.extract_metadata_from_pdf(path, keys)
        elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or file_extension == ".docx":
            # Extract metadata from DOCX files
            return self.extract_metadata_from_office_document(path, keys)
        elif mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or file_extension == ".xlsx":
            # Extract metadata from XLSX files
            return self.extract_metadata_from_office_document(path, keys)
        elif mime_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation" or file_extension == ".pptx":
            # Extract metadata from PPTX files
            return self.extract_metadata_from_office_document(path, keys)
        elif mime_type and mime_type.startswith("audio/") or file_extension in {".mp3", ".wav", ".flac"}:
            # Extract metadata from audio files
            return self.extract_metadata_from_audio(path, keys)
        elif magic.Magic().from_file(str(path)).startswith("PE32") or magic.Magic().from_file(str(path)).startswith("PE64"):
            # Extract metadata from PE (Windows executable) files
            return self.extract_metadata_from_executable(path, keys)
        elif magic.Magic().from_file(str(path)).startswith("ELF"):
            # Extract metadata from ELF (Linux executable) files
            return self.extract_metadata_from_executable(path, keys)
        else:
            self.error(f"Metadata extraction not supported for this type of file: {path.name}")
            return None

    def extract_metadata_from_image(self, path, keys: list = []) -> str:
        """
        Extract metadata from an image file
        """
        try:
            image = Image.open(path)
            metadata = image.info
            if keys:
                filtered_metadata = {k: v for k, v in metadata.items() if k in keys}
                results = [f"{j}: {image.info[j]}" for _, j in enumerate(filtered_metadata)]
            else:
                keys = image.info.keys()
                results = [f"{j}: {image.info[j]}" for _, j in enumerate(keys)]
            return "\n".join(results)
        except Exception as e:
            self.error(f"Error extracting metadata from image: {e}")
            return None


    def extract_metadata_from_pdf(self, path, keys: list = []) -> str:
        """
        Extract metadata from a PDF file
        """
        try:
            with open(path, 'rb') as pdf_file:
                pdf_reader = pypdf.PdfReader(pdf_file)
                metadata = {}
                
                for m in pdf_reader.metadata.keys():
                    m: str
                    metadata[m.removeprefix('/')] = pdf_reader.metadata[m]
                    
                if keys:
                    filtered_metadata = {k: v for k, v in metadata.items() if k in keys}
                    results = [f"{key}: {value}" for key, value in filtered_metadata.items()]
                else:
                    results = [f"{key}: {value}" for key, value in metadata.items()]
                return "\n".join(results)
        except Exception as e:
            self.error(f"Error extracting metadata from PDF: {e}")
            return None

    def extract_metadata_from_office_document(self, path, keys: list = []) -> str:
        """
        Extract metadata from Microsoft Office documents (DOCX, XLSX, PPTX)
        """
        try:
            with open(path, 'rb') as office_file:
                # You can use appropriate libraries to extract metadata from different office document types.
                # For example, for DOCX files, you can use python-docx library.
                # For XLSX files, you can use openpyxl.
                # For PPTX files, you can use python-pptx.
                # Implement the specific extraction logic for each type here.
                # For simplicity, we'll just read the binary data and display some info.
                binary_data = office_file.read()
                file_size = len(binary_data)
                encoding = chardet.detect(binary_data)['encoding'] or 'unknown encoding'
                return f"{path}: Office Document, {file_size} bytes, Encoding: {encoding}"
        except Exception as e:
            self.error(f"Error extracting metadata from Office document: {e}")
            return None


    def extract_metadata_from_audio(self, path, keys: list = []) -> str:
        """
        Extract metadata from audio files (MP3, WAV, FLAC, etc.)
        """
        try:
            audio_info = mediainfo(path)
            if keys:
                filtered_metadata = {k: audio_info[k] for k in keys if k in audio_info}
                results = [f"{key}: {value}" for key, value in filtered_metadata.items()]
            else:
                results = [f"{key}: {value}" for key, value in audio_info.items()]
            return "\n".join(results)
        except Exception as e:
            self.error(f"Error extracting metadata from audio file: {e}")
            return None
        
    def extract_metadata_from_executable(self, path, keys: list = []) -> str:
        """
        Extract metadata from executable files (PE, ELF, etc.)
        """
        try:
            # You can implement specific logic for extracting metadata from different executable formats.
            # For example, for PE (Windows) executables, you can use pefile library.
            # For ELF (Linux) executables, you can use pyelftools.
            # Implement the specific extraction logic for each type here.
            # For simplicity, we'll just read the binary data and display some info.
            binary_data = open(path, 'rb').read()
            file_size = len(binary_data)
            return f"{path}: Executable, {file_size} bytes"
        except Exception as e:
            self.error(f"Error extracting metadata from executable file: {e}")
            return None
