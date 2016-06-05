import os
from Crypto.PublicKey import RSA
import binascii

pastebot_private_key_string = open(os.path.join("../pastebot.net", "private.key"), "rb").read()
pastebot_public_key_string = open(os.path.join("../pastebot.net", "public.key"), "rb").read()

pastebot_private_key = RSA.importKey(pastebot_private_key_string)
pastebot_public_key = RSA.importKey(pastebot_public_key_string)


def decrypt_valuables(f):
    # decrypt contents of file using pastebot private key

    f = open(os.path.join("../pastebot.net", fn), "rb").read()

    decrypted = pastebot_private_key.decrypt(f).decode()

    print(decrypted)


if __name__ == "__main__":
    fn = input("Which file in pastebot.net does the botnet master want to view? ")

    if not os.path.exists(os.path.join("../pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)

    f = open(os.path.join("../pastebot.net", fn), "rb").read()

    decrypt_valuables(f)
