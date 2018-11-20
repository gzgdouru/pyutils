import rsa

if __name__ == "__main__":
    text = "d8611e318276f59568de5d5c0956377d812844110d65c56f959545e98f3183a00ad59f569e51c2adcd103f9e3764152980c91bcdaa4d45e380730874eebfd5f0f42b78c7f5dc912cd7ce33fd553806d88a6765814d05ae29ed82e4fd7a28ed0633484ae2da4c39f4e4821f28f17192642fd184d32ba26f57349f1ff1146dbde4"
    with open("private_key.pem") as f:
        prikey = rsa.PrivateKey.load_pkcs1(f.read().encode("utf-8"))
    bytes_text = bytes.fromhex(text)

    content = rsa.decrypt(bytes_text, prikey).decode("utf-8")
    print(content)
