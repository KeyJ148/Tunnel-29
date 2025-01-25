from amnezia import AmneziaAPI
import os
import io
import cairosvg
import re


class KeysGenerator:
    def __init__(self):
        self.AMNEZIA_PASSWORD = os.environ.get('AMNEZIA_PASSWORD')
        self.amnezia_api = AmneziaAPI()

    def generate_key(self, keyname_prefix):
        print(f"[ClientGenerator.generate] Start: keyname_prefix={keyname_prefix}")

        # Authenticate and get cookies
        cookies = self.amnezia_api.authenticate(self.AMNEZIA_PASSWORD)

        # Generate new key name
        client_all_keys = self.__get_client_all_keys(keyname_prefix, cookies)
        keyname = keyname_prefix + '-' + str(len(client_all_keys)+1)

        # Create new key and find its id
        self.amnezia_api.create_client(keyname, cookies)
        all_keys = self.amnezia_api.get_client_list(cookies)
        this_key = self.__find_key(all_keys, keyname)

        # Download conf and qr files
        return self.__download_key(this_key, cookies)

    def get_client_all_keys(self, keyname_prefix):
        print(f"[ClientGenerator.get_all_keys] Get keys: keyname_prefix={keyname_prefix}")

        # Authenticate and get cookies
        cookies = self.amnezia_api.authenticate(self.AMNEZIA_PASSWORD)

        # Get all keys and calculate number of client keys
        this_client_keys = self.__get_client_all_keys(keyname_prefix, cookies)

        returned_keys = []
        for key in this_client_keys:
            key = self.__download_key(key, cookies)
            returned_keys.append(key)

        return returned_keys

    def __get_client_all_keys(self, keyname_prefix, cookies):
        all_keys = self.amnezia_api.get_client_list(cookies)
        return self.__find_this_client_all_keys(all_keys, keyname_prefix)

    def __download_key(self, key, cookies):
        # Download and process configuration
        conf_content = self.amnezia_api.download_configuration(key["id"], cookies)
        conf_file = self.__convert_content_to_file(conf_content, key["name"] + '.conf')

        # Download and process QR
        qr_content = self.amnezia_api.download_qrcode(key["id"], cookies)
        qr_content = self.__convert_svg_to_png(qr_content)
        qr_file = self.__convert_content_to_file(qr_content, key["name"] + '.png')

        return {'conf': conf_file, 'qr': qr_file}

    @staticmethod
    def __find_this_client_all_keys(all_keys, keyname_prefix):
        # Regular expression to match the format user_name-0, user_name-1, ..., user_name-100
        pattern = re.compile(f"^{re.escape(keyname_prefix)}-(\d+)$")

        # Return all keys that match the pattern
        keys = [key for key in all_keys if pattern.match(key["name"])]
        if keys:
            print(f"[ClientGenerator.__find_this_client_all_keys] Found keys: keys={keys}")
        else:
            print(f"[ClientGenerator.__find_this_client_all_keys] Error while find keys: keys={keys}")

        return keys

    @staticmethod
    def __find_key(all_keys, keyname):
        this_key = next((key for key in all_keys if key["name"] == keyname), None)
        if this_key:
            print(f"[ClientGenerator.find_new_client] Found: this_key={this_key}")
        else:
            print(f"[ClientGenerator.find_new_client] Error while find: this_key={this_key}")

        return this_key

    @staticmethod
    def __convert_content_to_file(content, filename):
        file = io.BytesIO(content)
        file.name = filename
        return file

    @staticmethod
    def __convert_svg_to_png(svg_content):
        return cairosvg.svg2png(bytestring=svg_content)
