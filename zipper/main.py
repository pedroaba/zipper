import os

from compresser import LZWCompresser
from pathlib import Path


if __name__ == "__main__":
  compresser = LZWCompresser()

  c = compresser.compress(
    os.path.abspath(Path(".") / "example.txt")
  )

  print(c)
