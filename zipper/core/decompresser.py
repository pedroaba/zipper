from pathlib import Path
from struct import unpack

from configs.file_configs import FileConfiguration


class LZWDecompresser:
    def __init__(self) -> None:
        self._decode_dict = {}
        self._init_decode_dict()

    def decompress(
        self, compressed_filepath: Path | str, destiny: Path | str | None = None
    ):
        if not isinstance(compressed_filepath, Path):
            compressed_filepath = Path(compressed_filepath)

        if destiny is None:
            destiny = Path(compressed_filepath.parent)

        if not isinstance(destiny, Path):
            destiny = Path(destiny)

        destiny_filename = f"{compressed_filepath.stem}.txt"
        destiny = destiny / destiny_filename

        compressed_data = []
        with open(compressed_filepath, "rb") as compressed:
            while True:
                binary_data = compressed.read(
                    FileConfiguration.FILE_QUANTITY_BYTES_READ
                )
                if len(binary_data) != FileConfiguration.FILE_QUANTITY_BYTES_READ:
                    break

                (read_data,) = unpack(">H", binary_data)
                compressed_data.append(read_data)

        text_decoded = self._decode(compressed_data)

    def _decode(self, text_encoded: list):
        sequence_of_characters = ""
        next_encode_character = FileConfiguration.ENCODE_CHARACTER_RANGE
        text_decoded = ""
        for encode_character in text_encoded:
            if encode_character not in self._decode_dict:
                sequence_of_characters = sequence_of_characters = sequence_of_characters[0]
            text_decoded += self._decode_dict[encode_character]
            if not (len(sequence_of_characters) == 0):
                self._decode_dict[next_encode_character] = sequence_of_characters + self._decode_dict[encode_character][0]
                next_encode_character += 1
            sequence_of_characters = self._decode_dict[encode_character]
        return text_decoded

    def _init_decode_dict(self):
        self._decode_dict = {
            i: chr(i) for i in range(FileConfiguration.ENCODE_CHARACTER_RANGE)
        }
