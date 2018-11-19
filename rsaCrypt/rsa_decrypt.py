import rsa

if __name__ == "__main__":
    text = "dd06b583cc83369f3ee7143ae21d4f8ece2f0a19fa24b63be4b6ac1d479b534117d65399acfeca064eeb5ddac744c5adcfe9eda967a65ff09dd7d50288cec3b5ad685f2330db22a57555eb3b99b7cc5a951c86e9be02a97db5dfd9de80365c4ad28e6b8eb1f46fe953eb483c7dc3de3ca488326bbccc29af3a57ba598ab2057f"
    with open("private_key.pem") as f:
        prikey = rsa.PrivateKey.load_pkcs1(f.read().encode("utf-8"))
    bytes_text = bytes.fromhex(text)

    content = rsa.decrypt(bytes_text, prikey).decode("utf-8")
    print(content)
