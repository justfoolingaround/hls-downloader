from Cryptodome.Cipher import AES


def default_initialisation_vector(initial=1):

    while 1:
        yield initial.to_bytes(16, "big")
        initial += 1


default_iv = default_initialisation_vector()


def decrypt_aes(key, data, iv=None):
    if iv is None:
        iv = next(default_iv)
    return AES.new(key, AES.MODE_CBC, iv).decrypt(data)


DECRYPTERS = {
    "AES-128": decrypt_aes,
}
