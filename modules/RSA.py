import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


class RSA:
    def __init__(self):
        self.keys_folder_path = os.path.join('RSA', 'key_folder')
        self.private_key_path = os.path.join(self.keys_folder_path, 'private_key.pem')
        self.public_key_path = os.path.join(self.keys_folder_path, 'public_key.pem')
        if not os.path.exists(self.keys_folder_path):
            os.makedirs(self.keys_folder_path)

    def generate_key_pair(self):
        # Генеруємо ключову пару RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

        # Отримуємо публічний ключ з приватного
        public_key = private_key.public_key()

        # Серіалізуємо та зберігаємо приватний ключ у файл
        with open(self.private_key_path, 'wb') as private_key_file:
            private_key_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            private_key_file.write(private_key_pem)

        # Серіалізуємо та зберігаємо публічний ключ у файл
        with open(self.public_key_path, 'wb') as public_key_file:
            public_key_pem = public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            public_key_file.write(public_key_pem)

        # print("Ключова пара створена та збережена у файлах 'private_key.pem' та 'public_key.pem'.")

    def encrypt_message(self, message, public_key_file):
        # Завантажуємо публічний ключ з файлу
        with open(public_key_file, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )

        # Шифруємо повідомлення
        if not isinstance(message, bytes):
            message = message.encode('utf-8')
        ciphertext = public_key.encrypt(message,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

        return ciphertext

    def decrypt_message(self, ciphertext, private_key_file):
        # Завантажуємо приватний ключ з файлу
        with open(private_key_file, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        # Розшифровуємо повідомлення
        decrypted_message = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_message.decode('utf-8')

    def encrypt_file(self, input_file_path, output_file_path, public_key_file):
        with open(public_key_file, 'rb') as key_file:
            public_key = serialization.load_pem_public_key(key_file.read(), backend=default_backend())

        with open(input_file_path, 'rb') as file:
            plaintext = file.read()

        ciphertext = b""
        chunk_size = 128  # 2048 bits key - 11 bytes overhead for padding

        try:
            for i in range(0, len(plaintext), chunk_size):
                chunk = plaintext[i:i + chunk_size]
                encrypted_chunk = public_key.encrypt(
                    chunk,
                    padding.OAEP(
                        mgf=padding.MGF1(algorithm=hashes.SHA256()),
                        algorithm=hashes.SHA256(),
                        label=None
                    )
                )
                ciphertext += encrypted_chunk
        except Exception as e:
            print(f"Encryption failed: {e}")
            raise

        with open(output_file_path, 'wb') as encrypted_file:
            encrypted_file.write(ciphertext)

    def decrypt_file(self, input_file_path, output_file_path, private_key_file):
        with open(private_key_file, 'rb') as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )

        with open(input_file_path, 'rb') as file:
            ciphertext = file.read()

        plaintext = b""
        chunk_size = 256  # 2048 bits key

        for i in range(0, len(ciphertext), chunk_size):
            chunk = ciphertext[i:i + chunk_size]
            decrypted_chunk = private_key.decrypt(
                chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            plaintext += decrypted_chunk

        with open(output_file_path, 'wb') as decrypted_file:
            decrypted_file.write(plaintext)
