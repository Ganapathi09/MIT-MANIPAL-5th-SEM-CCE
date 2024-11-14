import os
import json
import time
from Crypto.Util import number
from datetime import datetime, timedelta

class RabinKeyManager:
    def __init__(self):
        self.keys = {}
        self.log_file = 'key_management_log.json'
        self.key_expiry_duration = timedelta(days=365)  # 12 months

    def generate_key_pair(self, bit_length=1024):
        p = self._generate_prime(bit_length // 2)
        q = self._generate_prime(bit_length // 2)
        n = p * q
        private_key = (p, q)
        public_key = n
        return public_key, private_key

    def _generate_prime(self, bit_length):
        return number.getPrime(bit_length)

    def request_keys(self, facility_name):
        if facility_name in self.keys:
            return self.keys[facility_name]['public'], self.keys[facility_name]['private']
        
        public_key, private_key = self.generate_key_pair()
        self.keys[facility_name] = {
            'public': public_key,
            'private': private_key,
            'expiry': datetime.now() + self.key_expiry_duration
        }
        self._log_operation('Key Generation', facility_name)
        return public_key, private_key

    def revoke_keys(self, facility_name):
        if facility_name in self.keys:
            del self.keys[facility_name]
            self._log_operation('Key Revocation', facility_name)

    def renew_keys(self):
        for facility in list(self.keys.keys()):
            if datetime.now() >= self.keys[facility]['expiry']:
                print(f"Renewing keys for {facility}")
                public_key, private_key = self.generate_key_pair()
                self.keys[facility] = {
                    'public': public_key,
                    'private': private_key,
                    'expiry': datetime.now() + self.key_expiry_duration
                }
                self._log_operation('Key Renewal', facility)

    def _log_operation(self, operation_type, facility_name):
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'operation': operation_type,
            'facility': facility_name
        }
        with open(self.log_file, 'a') as log:
            log.write(json.dumps(log_entry) + '\n')

# Example usage
if __name__ == "__main__":
    key_manager = RabinKeyManager()
    
    # Request keys for a hospital
    hospital_public, hospital_private = key_manager.request_keys("Hospital A")
    print(f"Hospital A Public Key: {hospital_public}")

    # Revoke keys for a hospital
    key_manager.revoke_keys("Hospital A")

    # Renew keys periodically (could be scheduled in a real application)
    key_manager.renew_keys()