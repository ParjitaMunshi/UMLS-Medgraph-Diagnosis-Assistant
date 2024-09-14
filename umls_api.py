# This script will handle all interactions with the UMLS API, including authentication and data retrieval.

import requests

class UMLS_API:
    def __init__(self, api_key):
        self.api_key = api_key
        self.tgt_url = 'https://utslogin.nlm.nih.gov/cas/v1/tickets'
        self.service_url = 'https://uts-ws.nlm.nih.gov/rest'
        self.tgt = self.get_tgt()

    def get_tgt(self):
        """Authenticate using API key and get a Ticket Granting Ticket (TGT)"""
        response = requests.post(self.tgt_url, data={'apikey': self.api_key})
        if response.status_code == 201:
            return response.headers['location']
        else:
            raise Exception(f"Failed to get TGT: {response.status_code}")

    def get_service_ticket(self):
        """Use TGT to get a Service Ticket for each request"""
        response = requests.post(self.tgt, data={'service': self.service_url})
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to get Service Ticket: {response.status_code}")

    def search_term(self, search_term):
        """Search UMLS for a given medical term"""
        service_ticket = self.get_service_ticket()
        url = f"{self.service_url}/search/current?string={search_term}&ticket={service_ticket}"
        response = requests.get(url).json()
        return response

    def get_concept_by_cui(self, cui):
        """Retrieve details of a UMLS concept by its CUI"""
        service_ticket = self.get_service_ticket()
        url = f"{self.service_url}/content/current/CUI/{cui}?ticket={service_ticket}"
        response = requests.get(url).json()
        return response

# Example usage
if __name__ == '__main__':
    api_key = '398ddd89-e2d1-45ed-9581-cefd9ae10a40'
    umls_api = UMLS_API(api_key)

    # Example: Search for a medical term
    search_results = umls_api.search_term("diabetes")
    print(search_results)

    # Example: Get details of a concept by its CUI
    concept_details = umls_api.get_concept_by_cui("C0011849")  # Example CUI for "diabetes mellitus"
    print(concept_details)
