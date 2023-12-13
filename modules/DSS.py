import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import base64


class DSS:
    def __init__(self):
        self.keys_folder_path = os.path.join('DSS', 'key_folder')
        self.private_key_path = os.path.join(self.keys_folder_path, 'dss_private_key.pem')
        self.public_key_path = os.path.join(self.keys_folder_path, 'dss_public_key.pem')
        if not os.path.exists(self.keys_folder_path):
            os.makedirs(self.keys_folder_path)

    def generate_key(self):
        private_key = dsa.generate_private_key(key_size=2048)
        public_key = private_key.public_key()

        with open(self.private_key_path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))

        with open(self.public_key_path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

    def load_private_key(self, prv_key_pth=os.path.join('DSS', 'key_folder', 'dss_private_key.pem')):
        with open(prv_key_pth, 'rb') as f:
            private_key = serialization.load_pem_private_key(
                f.read(),
                password=None
            )
        return private_key

    def load_public_key(self, pub_key_pth=os.path.join('DSS', 'key_folder', 'dss_public_key.pem')):
        with open(pub_key_pth, 'rb') as f:
            public_key = serialization.load_pem_public_key(
                f.read()
            )
        return public_key

    def sign_message(self, message, private_key):
        signature = private_key.sign(
            message.encode('utf-8'),
            hashes.SHA256()
        )
        return base64.b64encode(signature).decode('utf-8')

    def verify_signature(self, message, signature, public_key):
        try:
            public_key.verify(
                base64.b64decode(signature.encode('utf-8')),
                message.encode('utf-8'),
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(e)
            return False

    def sign_file(self, file_path, private_key, output_path=os.path.join('DSS', 'output', 'signature.bin')):
        with open(file_path, 'rb') as f:
            file_content = f.read()

        signature = private_key.sign(
            file_content,
            hashes.SHA256()
        )

        with open(output_path, 'wb') as f:
            f.write(signature)

    def verify_file(self, file_path, public_key, signature_path=os.path.join('DSS', 'output', 'signature.bin')):
        with open(file_path, 'rb') as f:
            file_content = f.read()

        with open(signature_path, 'rb') as f:
            signature = f.read()

        try:
            public_key.verify(
                signature,
                file_content,
                hashes.SHA256()
            )
            return True
        except Exception as e:
            print(e)
            return False
