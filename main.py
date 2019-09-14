import sys
import threading
from tabulate import tabulate
from crypto.Cipher import AES

from typing import List, Tuple

from src import app

class XSafeKeystore(object):
    __keys: List
    __block_size: int

    _curr_wk: int
    _iv: str

    def __init__(self, block_size: int):
        self.__keys = []
        self._curr_wk = 0
        self.__block_size = block_size
        self._iv = 'fev9C$8H1!KPP5@2'

    def safe_write(self, data: bytes, b_size: int, loc: str) -> bool:
        _keys = self.handle_keys(data)

        print(tabulate(_keys, headers=['idx', 'offset', 'length'], tablefmt='orgtbl'))

        for key in _keys:
            with open(f"{loc}/block_{key[0]}.block", "wb") as f:
                _rx = data[key[0]*self.__block_size : key[0]*self.__block_size + key[2]]
                _rx_iv = self.aes_bytes(_rx)
                f.write(_rx_iv)
                f.close()

        return True

    def handle_keys(self, data: bytes) -> List:
        _idx = len(self.__keys)

        """ check previous blocks size: open(block - 1), len(f.read()) < self.__block_size: write to previous block first"""
        _blocks = []

        _curr_block_len = 0
        _blocks.append([0, 0, 0])
        for i in range(0, len(data)):
            _curr_block_len += 1
            if _curr_block_len > self.__block_size:
                _idx += 1
                _curr_block_len = 0
                _blocks.append([_idx, 0, _curr_block_len])
            else:
                _blocks[-1][2] = _curr_block_len

        return _blocks

    def xor_bytes(self, bytes_a: bytes, bytes_b: bytes) -> bytes:
        chunk = []
        for b1, b2 in zip(bytes_a, bytes_b):
            chunk.append(bytes([b1 ^ b2]))

        return b''.join(chunk)

    def aes_bytes(self, bytes_data: bytes) -> str:
        chunk = []
        for data in zip(bytes_data):
            chunk.append(bytes(data))

        data_joined = b''.join(chunk)
        cipher = AES.new(self._iv)

        _cr = False
        while _cr is False:
            if len(data_joined) % 16 == 0:
                _cr = True
            else:
                _cr = False
                data_joined += b'\00'
        data_encrypted = cipher.encrypt(data_joined)
        return data_encrypted


class Storage(object):
    __block_size: int
    __block_loc: str

    __keystore: XSafeKeystore

    _length: int

    def __init__(self, block_size: int):
        self.__block_size = block_size
        self.__block_loc = "/Users/jacob/Desktop/boat_bored/data_store/blocks"
        self.__keystore = XSafeKeystore(self.__block_size)

        self._length = 0

    def write(self, data: bytes) -> bool:
        self.__keystore.safe_write(data, self.__block_size, self.__block_loc)


def do_encrypt(file_in: str, n_bytes: int) -> None:
    storage = Storage(int(n_bytes))
    storage.write(open(file_in, 'rb').read())

def do_server() -> None:
    app.app.run()

if __name__ == "__main__":
    encrypt_thread = threading.Thread(target=do_encrypt, args=(sys.argv[1], sys.argv[2],))
    server_thread = threading.Thread(target=do_server, args=())

    encrypt_thread.start()
    server_thread.start()
    encrypt_thread.join()
    server_thread.join()
