import os

from compresser import LZWCompresser
from decompresser import LZWDecompresser
from pathlib import Path


if __name__ == "__main__":
  compresser = LZWCompresser()
  decompresser = LZWDecompresser()

  c = compresser.compress(
    os.path.abspath(Path(".") / "example.txt")
  )

  d = decompresser.decompress(
    os.path.abspath(Path(".") / "example.marcelo")
  )

  print(c)
