import argparse
import logging
import os


class ByteIO:
    def __init__(self, name: str, mode: str):
        self.stream = open(name, mode)
        self.buff = bytearray(1)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return exc_type is None

    def getc(self):
        if self.stream.readinto(self.buff) == 0:
            return None
        return self.buff[0]

    def putc(self, x):
        self.buff[0] = x & 0xFF
        return self.stream.write(self.buff)

    def close(self):
        self.stream.close()


class RLE:
    MAX_LEN = 255

    def __init__(self, n: int):
        self.n = n

    def encode(self, fin: ByteIO, fout: ByteIO) -> None:
        c = fin.getc()
        while c is not None:
            num = 1
            while num < self.MAX_LEN + self.n:
                c1 = fin.getc()
                if c != c1:
                    break
                num += 1
            if num >= self.n:
                for _ in range(self.n):
                    fout.putc(c)
                fout.putc(num - self.n)
            else:
                for _ in range(num):
                    fout.putc(c)
            if num == self.MAX_LEN + self.n:
                c = fin.getc()
            else:
                c = c1

    def decode(self, fin: ByteIO, fout: ByteIO) -> None:
        c = fin.getc()
        while c is not None:
            num = 1
            while num < self.n:
                c1 = fin.getc()
                if c != c1:
                    break
                num += 1

            if num == self.n:
                num += fin.getc()
                c1 = fin.getc()
            for _ in range(num):
                fout.putc(c)
            c = c1

    # 符号化
    def compress(self, input_file: str, output_file: str) -> None:
        with ByteIO(input_file, "rb") as fin, ByteIO(output_file, "wb") as fout:
            self.encode(fin, fout)

    # 復号
    def decompress(self, input_file: str, output_file: str) -> None:
        with ByteIO(input_file, "rb") as fin, ByteIO(output_file, "wb") as fout:
            self.decode(fin, fout)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # オプション解析
    parser = argparse.ArgumentParser(description="ランレングス符号")
    parser.add_argument("input_file", help="入力ファイル")
    parser.add_argument("output_file", help="出力ファイル")
    parser.add_argument("-c", "--compress", action="store_true", help="符号化")
    parser.add_argument("-d", "--decompress", action="store_true", help="復号")
    args = parser.parse_args()
    print(
        f"input_file:{args.input_file}, output_file:{args.output_file}, compress:{args.compress}, decompress:{args.decompress}"
    )

    if args.compress and not args.decompress:
        rle = RLE(4)
        rle.compress(args.input_file, args.output_file)
        logging.log(
            logging.INFO,
            f"圧縮前：{os.path.getsize(args.input_file)}　圧縮後：{os.path.getsize(args.output_file)} 圧縮率：{os.path.getsize(args.output_file)/os.path.getsize(args.input_file)*100}%",
        )

    if args.decompress and not args.compress:
        rle = RLE(4)
        rle.decode(args.input_file, args.output_file)
