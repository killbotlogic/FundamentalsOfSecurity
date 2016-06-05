import os
from Crypto.PublicKey import RSA

pastebot_private_key_string = open(os.path.join("../pastebot.net", "private.key"), "rb").read()
pastebot_public_key_string = open(os.path.join("../pastebot.net", "public.key"), "rb").read()

pastebot_private_key = RSA.importKey(pastebot_private_key_string)
pastebot_public_key = RSA.importKey(pastebot_public_key_string)


def sign_file(f):
    # Add Ceasar signature to first line of file. Signed with pastebot private key
    sign = pastebot_private_key.sign("Caesar".encode(), 'x')[0]

    return str(sign).encode() + b'\n' + f


if __name__ == "__main__":

    fn = input("Which file in pastebot.net should be signed? ")
    # fn = "hello"
    if not os.path.exists(os.path.join("../pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        os.exit(1)
    f = open(os.path.join("../pastebot.net", fn), "rb").read()

    signed_f = sign_file(f)
    signed_fn = os.path.join("../pastebot.net", fn + ".signed")
    out = open(signed_fn, "wb")
    out.write(signed_f)
    out.close()
    print("Signed file written to", signed_fn)
