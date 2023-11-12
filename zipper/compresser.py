import os
import shutil

from struct import pack
from pathlib import Path

from configs.file_configs import FileConfiguration


class LZWCompresser:
    def __init__(self):
        self._encode_dict = {}
        self._last_value_in_encode_dict = 128
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

        compress_content = self._encode(compress_content)
        self._save_zipper_file(compress_content, destiny / destiny_filename)
        self._check_if_file_was_compressed(destiny / destiny_filename, filepath)
        return ""

    def _save_zipper_file(self, content_zipped: list[int], path: Path):
        with open(path, "wb") as zipper_file:
            for content in content_zipped:
                zipper_file.write(pack(">H", content))

    def _check_if_file_was_compressed(
        self, compressed_filepath: Path, raw_filepath: Path
    ):
        sizeof_compressed_file = os.path.getsize(compressed_filepath)
        sizeof_raw_file = os.path.getsize(raw_filepath)

        if sizeof_compressed_file > sizeof_raw_file:
            compressed_filepath.unlink()
            
            shutil.copy(
                str(raw_filepath),
                str(compressed_filepath)
            )

    def _init_encode_dict(self):
        self._encode_dict = {chr(i): i for i in range(1, 129)}

    def _encode(self, text: str) -> list[int]:
        characters = ""
        text_encoded = []
        for character in text:
            text_comb = characters + character
            if text_comb in self._encode_dict:
                characters = text_comb
                continue
            text_encoded.append(self._encode_dict[characters])
            if len(self._encode_dict) <= self._max_of_bytes:
                self._last_value_in_encode_dict += 1
                self._encode_dict[text_comb] = self._last_value_in_encode_dict
            characters = character
        if characters in self._encode_dict:
            text_encoded.append(self._encode_dict[characters])
        return text_encoded
