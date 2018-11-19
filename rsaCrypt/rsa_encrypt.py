import rsa

if __name__ == "__main__":
    with open("public_key.pem") as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode("utf-8"))

    content = "43fefda5eef0b55366668ab718c9c81a"
    bytes_text = rsa.encrypt(content.encode("utf-8"), pubkey)

    hex_text = bytes_text.hex()
    print(hex_text)