import base64
import gzip

def compress(strData:str) -> str:
    return base64.b64encode(gzip.compress(bytes(strData, "UTF-8"))).decode("UTF-8")

def decompress(strData:str) -> str:
    return gzip.decompress(base64.b64decode(strData)).decode("UTF-8")

def test_compress():
    plainText = "Hello, world!"
    assert(plainText == decompress(compress(plainText)))