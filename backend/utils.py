import requests
import json
from config import Config

class OSINTCollector:
    def __init__(self):
        self.hibp_key = Config.HIBP_API_KEY
        self.emailrep_key = Config.EMAILREP_API_KEY
        self.abstract_key = Config.ABSTRACT_API_KEY

    def check_email(self, email):
        """Check email breaches and reputation via public APIs."""
        result = {}
        # HaveIBeenPwned
        if self.hibp_key:
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {'hibp-api-key': self.hibp_key}
            try:
                resp = requests.get(url, headers=headers)
                if resp.status_code == 200:
                    result['breaches'] = resp.json()
                elif resp.status_code == 404:
                    result['breaches'] = []
                else:
                    result['breaches_error'] = f"HTTP {resp.status_code}"
            except Exception as e:
                result['breaches_error'] = str(e)
        else:
            result['breaches'] = "API key missing"

        # EmailRep.io
        if self.emailrep_key:
            url = f"https://emailrep.io/{email}"
            headers = {'Key': self.emailrep_key, 'User-Agent': 'OSINT-Fusion'}
            try:
                resp = requests.get(url, headers=headers)
                if resp.status_code == 200:
                    result['reputation'] = resp.json()
                else:
                    result['reputation_error'] = f"HTTP {resp.status_code}"
            except Exception as e:
                result['reputation_error'] = str(e)
        else:
            result['reputation'] = "API key missing"

        return result

    def check_phone(self, phone):
        """Validate phone number and get carrier/location via AbstractAPI."""
        result = {}
        if self.abstract_key:
            url = f"https://phonevalidation.abstractapi.com/v1/?api_key={self.abstract_key}&phone={phone}"
            try:
                resp = requests.get(url)
                if resp.status_code == 200:
                    result['phone_info'] = resp.json()
                else:
                    result['phone_error'] = f"HTTP {resp.status_code}"
            except Exception as e:
                result['phone_error'] = str(e)
        else:
            result['phone_info'] = "API key missing"
        return result

    def check_username(self, username):
        """Search username across social media (simulated with placeholder)."""
        # In a real tool, you'd integrate with services like WhatsMyName or Sherlock.
        # For ethical reasons, we return a placeholder.
        return {
            'message': 'Username search is simulated. In production, integrate with Sherlock or similar.',
            'note': 'This tool only demonstrates the architecture. No actual scraping occurs.'
        }
