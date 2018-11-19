import rsa

if __name__ == "__main__":
    pubkey, prikey = rsa.newkeys(1024)

    with open("public_key.pem", "w+") as f:
        f.write(pubkey.save_pkcs1().decode("utf-8"))

    with open("private_key.pem", "w+") as f:
        f.write(prikey.save_pkcs1().decode("utf-8"))
