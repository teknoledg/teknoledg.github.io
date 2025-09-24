#!/usr/bin/env python3
"""
Encryption utilities for QR code security
Implements AES encryption for certificate data
"""

import base64
import json
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
import secrets

class CertificateEncryption:
    def __init__(self, password=None):
        """
        Initialize encryption with password or generate new key
        """
        if password:
            self.key = self._derive_key(password)
        else:
            # Generate a new key (for development)
            self.key = Fernet.generate_key()
        
        self.cipher = Fernet(self.key)
    
    def _derive_key(self, password: str) -> bytes:
        """
        Derive encryption key from password using PBKDF2
        """
        # Use a fixed salt for consistency (in production, store salt separately)
        salt = b'teknoledg_cert_salt_2024'
        
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key
    
    def encrypt_certificate_data(self, certificate_data: dict) -> str:
        """
        Encrypt certificate data for QR code
        """
        try:
            # Convert certificate data to JSON
            json_data = json.dumps(certificate_data, separators=(',', ':'))
            
            # Encrypt the data
            encrypted_data = self.cipher.encrypt(json_data.encode())
            
            # Encode to base64 for QR code
            encoded_data = base64.urlsafe_b64encode(encrypted_data).decode()
            
            return encoded_data
            
        except Exception as e:
            raise Exception(f"Encryption failed: {str(e)}")
    
    def decrypt_certificate_data(self, encrypted_data: str) -> dict:
        """
        Decrypt certificate data from QR code
        """
        try:
            # Decode from base64
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            
            # Decrypt the data
            decrypted_data = self.cipher.decrypt(encrypted_bytes)
            
            # Parse JSON
            certificate_data = json.loads(decrypted_data.decode())
            
            return certificate_data
            
        except Exception as e:
            raise Exception(f"Decryption failed: {str(e)}")
    
    def generate_secure_qr_data(self, certificate_number: str, certificate_data: dict) -> str:
        """
        Generate secure QR code data with encryption
        """
        # Add timestamp and nonce for additional security
        secure_data = {
            'cert_number': certificate_number,
            'data': certificate_data,
            'timestamp': int(os.time()),
            'nonce': secrets.token_hex(16)
        }
        
        # Encrypt the complete data
        encrypted_data = self.encrypt_certificate_data(secure_data)
        
        # Add prefix for identification
        return f"SEC_CERT:{encrypted_data}"
    
    def parse_secure_qr_data(self, qr_data: str) -> dict:
        """
        Parse and decrypt secure QR code data
        """
        if not qr_data.startswith("SEC_CERT:"):
            raise Exception("Invalid QR code format")
        
        # Extract encrypted data
        encrypted_data = qr_data[9:]  # Remove "SEC_CERT:" prefix
        
        # Decrypt the data
        decrypted_data = self.decrypt_certificate_data(encrypted_data)
        
        return decrypted_data
    
    def verify_certificate_integrity(self, decrypted_data: dict, expected_cert_number: str) -> bool:
        """
        Verify certificate integrity and authenticity
        """
        try:
            # Check if certificate number matches
            if decrypted_data.get('cert_number') != expected_cert_number:
                return False
            
            # Check timestamp (optional - certificates shouldn't be too old)
            timestamp = decrypted_data.get('timestamp', 0)
            current_time = int(os.time())
            
            # Allow certificates up to 1 year old
            if current_time - timestamp > 31536000:  # 1 year in seconds
                return False
            
            return True
            
        except Exception:
            return False

# Global encryption instance
# In production, use a secure password from environment variables
ENCRYPTION_PASSWORD = os.getenv('CERTIFICATE_ENCRYPTION_PASSWORD', 'teknoledg_secure_2024')
encryption = CertificateEncryption(ENCRYPTION_PASSWORD)

def encrypt_certificate_for_qr(certificate_data: dict) -> str:
    """
    Encrypt certificate data for QR code generation
    """
    return encryption.generate_secure_qr_data(
        certificate_data.get('certificate_number', ''),
        certificate_data
    )

def decrypt_qr_certificate(qr_data: str) -> dict:
    """
    Decrypt certificate data from QR code
    """
    return encryption.parse_secure_qr_data(qr_data)

def verify_qr_certificate(qr_data: str, expected_cert_number: str) -> tuple:
    """
    Verify QR code certificate and return (is_valid, certificate_data)
    """
    try:
        decrypted_data = decrypt_qr_certificate(qr_data)
        
        if encryption.verify_certificate_integrity(decrypted_data, expected_cert_number):
            return True, decrypted_data.get('data', {})
        else:
            return False, None
            
    except Exception as e:
        return False, None
