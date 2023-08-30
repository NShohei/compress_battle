# BEGIN: xz4d5f8g9hj3
import os
import unittest
from rle import RLE
import shutil


class TestRLE(unittest.TestCase):
    def setUp(self):
        self.rle = RLE(10)

    def test_compress_decompress(self):
        self.rle.compress(
            "tests\\test_files\\sangetsuki.txt", "tests\\test_files\\sangetsuki.txt.rl"
        )
        self.rle.decompress(
            "tests\\test_files\\sangetsuki.txt.rl",
            "tests\\test_files\\sangetsuki.txt.rl.txt",
        )
        with open("tests\\test_files\\sangetsuki.txt", "rb") as f1, open(
            "tests\\test_files\\sangetsuki.txt.rl.txt", "rb"
        ) as f2:
            original_data = f1.read()
            decompressed_data = f2.read()

        self.assertEqual(original_data, decompressed_data)

    # def test_decode(self):
    #     test_data = bytes("4A4B4C4あ", encoding="utf-8")
    #     self.assertEqual(
    #         self.rle.decode_rle(test_data), bytes("AAAABBBBCCCCああああ", encoding="utf-8")
    #     )

    # def test_encode(self):
    #     test_data = bytes("AAAABBBBCCCCああああ", encoding="utf-8")
    #     self.assertEqual(
    #         self.rle.encode_rle(test_data), bytes("4A4B4C4あ", encoding="utf-8")
    #     )


if __name__ == "__main__":
    unittest.main()
# END: xz4d5f8g9hj3
