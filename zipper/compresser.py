import os
import shutil

from struct import pack
from pathlib import Path

from configs.file_configs import FileConfiguration


class LZWCompresser:
    """Class responsible of compress process

    Attributes:
        _encode_dict: dictionary with encode caracters and sequencies and yours values
        _last_value_in_encode_dict: value to save last value of a key on _encode_dict
        _max_of_bytes: max of size that my _encode_dictionary can be has
    """
    def __init__(self):
        self._encode_dict = {}
        self._last_value_in_encode_dict = FileConfiguration.ENCODE_CHARACTER_RANGE
        self._max_of_bytes = 65535

        self._init_encode_dict()

    def compress(self, filepath: Path | str, destiny: Path | str = "") -> str:
        """This function is responsible to compress file

        Parameters:
          filepath: path to file that will be compress
          destiny: where compress file will be save

        Returns:
          filepath of compressed file
        """
        if not isinstance(filepath, Path):
            filepath = Path(filepath)

        if not destiny:
            destiny = filepath.cwd()

        if not isinstance(destiny, Path):
            destiny = Path(destiny)

        compress_content = ""
        with open(filepath, "r") as file:
            for line in file:
                compress_content += line

        destiny_filename = f"{filepath.stem}{FileConfiguration.FILE_EXTENTION}"
        destiny = destiny / destiny_filename

        compress_content = self._encode(compress_content)
        self._save_zipper_file(compress_content, destiny)
        self._check_if_file_was_compressed(destiny, filepath)
        return str(destiny)

    def _save_zipper_file(self, content_zipped: list[int], path: Path):
        """Save compressed file as binary file

        Parameters:
            content_zipped: encoded content of file
            path: path to save compressed file
        """
        with open(path, "wb") as zipper_file:
            for content in content_zipped:
                zipper_file.write(pack(">H", content))

    def _check_if_file_was_compressed(
        self, compressed_filepath: Path, raw_filepath: Path
    ):
        """Check if compress file has size smaller than original file and only override
        the compressed file with raw file with content if compressed file is bigger than
        raw file

        Parameters:
            compressed_filepath: path of compressed file
            raw_filepath: path to raw file
        """
        sizeof_compressed_file = os.path.getsize(compressed_filepath)
        sizeof_raw_file = os.path.getsize(raw_filepath)

        if sizeof_compressed_file > sizeof_raw_file:
            compressed_filepath.unlink()

            shutil.copy(str(raw_filepath), str(compressed_filepath))

    def _init_encode_dict(self):
        """Initialize dictionary with basic encode"""
        self._encode_dict = {
            chr(i): i for i in range(FileConfiguration.ENCODE_CHARACTER_RANGE)
        }

    def _encode(self, text: str) -> list[int]:
        """Encode text from file content based on dictionary

        Parameters:
            text: content of file to encode

        Returns:
            list content encoded of file
        """
        sequence_of_characters = ""
        text_encoded = []
        for character in text:
            text_comb = sequence_of_characters + character
            if text_comb in self._encode_dict:
                sequence_of_characters = text_comb
                continue
            text_encoded.append(self._encode_dict[sequence_of_characters])
            if len(self._encode_dict) <= self._max_of_bytes:
                self._encode_dict[text_comb] = self._last_value_in_encode_dict
                self._last_value_in_encode_dict += 1
            sequence_of_characters = character
        if sequence_of_characters in self._encode_dict:
            text_encoded.append(self._encode_dict[sequence_of_characters])
        return text_encoded
