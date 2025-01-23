import requests
import os


class AmneziaAPI:
    def __init__(self):
        self.API_URL = os.environ.get('API_URL')

    def authenticate(self, password):
        url = f"{self.API_URL}/session"
        headers = {"content-type": "application/json"}
        payload = {"password": password, "remember": True}

        response = requests.post(url, headers=headers, json=payload)
        print(f"[AmneziaAPI.authenticate] Request: password={password}")
        print(f"[AmneziaAPI.authenticate] Response: status_code={response.status_code}")
        response.raise_for_status()

        # Extract cookies from the response
        return response.cookies

    def create_client(self, user_name, cookies):
        url = f"{self.API_URL}/wireguard/client"
        headers = {"content-type": "application/json"}
        payload = {"name": user_name, "expiredDate": ""}

        response = requests.post(url, headers=headers, json=payload, cookies=cookies)
        print(f"[AmneziaAPI.create_client] Request: name={user_name}")
        print(f"[AmneziaAPI.create_client] Response: status_code={response.status_code}")
        response.raise_for_status()

    def get_client_list(self, cookies):
        url = f"{self.API_URL}/wireguard/client"
        headers = {"content-type": "application/json"}

        response = requests.get(url, headers=headers, cookies=cookies)
        print(f"[AmneziaAPI.get_client_list] Request: cookies={cookies}")
        print(f"[AmneziaAPI.get_client_list] Response: status_code={response.status_code}")
        response.raise_for_status()

        # Parse and return the array of objects with 'id' and 'name'
        return [{"id": client["id"], "name": client["name"]} for client in response.json()]

    def download_configuration(self, client_id, cookies):
        url = f"{self.API_URL}/wireguard/client/{client_id}/configuration"

        response = requests.get(url, cookies=cookies)
        print(f"[AmneziaAPI.download_configuration] Request: client_id={client_id}, cookies={cookies}")
        print(f"[AmneziaAPI.download_configuration] Response: status_code={response.status_code}")
        response.raise_for_status()

        return response.content

    def download_qrcode(self, client_id, cookies):
        url = f"{self.API_URL}/wireguard/client/{client_id}/qrcode.svg"

        response = requests.get(url, cookies=cookies)
        print(f"[AmneziaAPI.download_qrcode] Request: client_id={client_id}, cookies={cookies}")
        print(f"[AmneziaAPI.download_qrcode] Response: status_code={response.status_code}")
        response.raise_for_status()

        return response.content
