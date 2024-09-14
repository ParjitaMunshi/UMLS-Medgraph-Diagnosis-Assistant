import requests

class AccessGUDID:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://accessgudid.nlm.nih.gov/api/v2'

    def get_device_snomed(self, di):
        """Fetch SNOMED information for a device by its DI (Device Identifier)"""
        url = f"{self.base_url}/devices/snomed?apiKey={self.api_key}&di={di}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching SNOMED data: {response.status_code} - {response.text}")

    def get_implantable_list(self, page=1, per_page=10):
        """Fetch a list of implantable devices"""
        url = f"{self.base_url}/devices/implantable/list.json?apiKey={self.api_key}&page={page}&per_page={per_page}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching implantable devices: {response.status_code} - {response.text}")

    def get_implantable_download(self):
        """Download implantable device list"""
        url = f"{self.base_url}/devices/implantable/download?apiKey={self.api_key}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error downloading implantable devices: {response.status_code} - {response.text}")

# Example usage
if __name__ == '__main__':
    api_key = '398ddd89-e2d1-45ed-9581-cefd9ae10a40'  # Replace with your UMLS API Key

    gudid = AccessGUDID(api_key)

    # Example: Fetch SNOMED information for a specific Device Identifier (DI)
    try:
        snomed_info = gudid.get_device_snomed("08717648200274")  # Example DI
        print(snomed_info)
    except Exception as e:
        print(e)

    # Example: Fetch implantable device list
    try:
        implantable_list = gudid.get_implantable_list(page=1, per_page=5)
        print(implantable_list)
    except Exception as e:
        print(e)

    # Example: Download implantable devices
    try:
        implantable_data = gudid.get_implantable_download()
        with open("implantable_devices.csv", "wb") as file:
            file.write(implantable_data)
        print("Implantable device data saved.")
    except Exception as e:
        print(e)
