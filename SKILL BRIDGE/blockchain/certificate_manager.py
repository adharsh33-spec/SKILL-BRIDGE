"""
Blockchain Integration for Digital Certificates
Generates and verifies blockchain-based digital certificates
"""

import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, Tuple

class BlockchainCertificateManager:
    """Manages digital certificates on blockchain"""
    
    def __init__(self, network='testnet', api_key=None):
        """
        Initialize blockchain manager
        
        Args:
            network: Blockchain network ('testnet' or 'mainnet')
            api_key: API key for blockchain service
        """
        self.network = network
        self.api_key = api_key
        self.certificates = {}  # In-memory storage for demo
        self.transaction_log = []
    
    def generate_certificate_hash(self, user_id: int, skill_name: str, 
                                  issuer: str, issue_date: str = None) -> str:
        """
        Generate unique hash for certificate
        
        Args:
            user_id: User ID
            skill_name: Skill name
            issuer: Certificate issuer
            issue_date: Issue date (defaults to current date)
        
        Returns:
            SHA-256 hash of certificate data
        """
        if issue_date is None:
            issue_date = datetime.now().isoformat()
        
        certificate_data = {
            'user_id': user_id,
            'skill_name': skill_name,
            'issuer': issuer,
            'issue_date': issue_date,
            'nonce': datetime.now().isoformat()
        }
        
        data_string = json.dumps(certificate_data, sort_keys=True)
        certificate_hash = hashlib.sha256(data_string.encode()).hexdigest()
        
        return certificate_hash
    
    def create_certificate(self, user_id: int, skill_name: str, issuer: str,
                          validity_days: int = 365) -> Dict:
        """
        Create and record a digital certificate
        
        Args:
            user_id: User ID
            skill_name: Skill name
            issuer: Certificate issuer
            validity_days: Certificate validity period
        
        Returns:
            Certificate details with blockchain info
        """
        issue_date = datetime.now()
        expiry_date = issue_date + timedelta(days=validity_days)
        
        certificate_hash = self.generate_certificate_hash(
            user_id, skill_name, issuer, issue_date.isoformat()
        )
        
        # Simulate blockchain address (in production, use actual blockchain)
        blockchain_address = f"0x{certificate_hash[:40]}"
        
        certificate = {
            'certificate_hash': certificate_hash,
            'blockchain_address': blockchain_address,
            'user_id': user_id,
            'skill_name': skill_name,
            'issuer': issuer,
            'issue_date': issue_date.isoformat(),
            'expiry_date': expiry_date.isoformat(),
            'validity_days': validity_days,
            'status': 'active',
            'verification_count': 0,
            'qr_code_url': self._generate_qr_code_url(certificate_hash)
        }
        
        # Store certificate
        self.certificates[certificate_hash] = certificate
        
        # Log transaction
        self._log_transaction('CREATE_CERTIFICATE', certificate_hash, {
            'user_id': user_id,
            'skill_name': skill_name
        })
        
        return certificate
    
    def verify_certificate(self, certificate_hash: str) -> Tuple[bool, Dict]:
        """
        Verify a certificate
        
        Args:
            certificate_hash: Certificate hash to verify
        
        Returns:
            Tuple of (is_valid, certificate_details)
        """
        if certificate_hash not in self.certificates:
            return False, {'error': 'Certificate not found'}
        
        certificate = self.certificates[certificate_hash]
        
        # Check expiry
        expiry_date = datetime.fromisoformat(certificate['expiry_date'])
        is_expired = datetime.now() > expiry_date
        
        # Update verification count
        certificate['verification_count'] += 1
        
        # Log transaction
        self._log_transaction('VERIFY_CERTIFICATE', certificate_hash, {
            'status': 'verified' if not is_expired else 'expired'
        })
        
        is_valid = not is_expired and certificate['status'] == 'active'
        
        return is_valid, certificate
    
    def revoke_certificate(self, certificate_hash: str, reason: str = None) -> bool:
        """
        Revoke a certificate
        
        Args:
            certificate_hash: Certificate hash to revoke
            reason: Reason for revocation
        
        Returns:
            Success status
        """
        if certificate_hash not in self.certificates:
            return False
        
        certificate = self.certificates[certificate_hash]
        certificate['status'] = 'revoked'
        
        # Log transaction
        self._log_transaction('REVOKE_CERTIFICATE', certificate_hash, {
            'reason': reason or 'Not specified'
        })
        
        return True
    
    def get_user_certificates(self, user_id: int) -> list:
        """Get all certificates for a user"""
        return [
            cert for cert in self.certificates.values()
            if cert['user_id'] == user_id
        ]
    
    def _generate_qr_code_url(self, certificate_hash: str) -> str:
        """Generate QR code URL for certificate"""
        # This would use a QR code generation service
        base_url = "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data="
        verification_url = f"https://skillbridge.com/verify/{certificate_hash}"
        return f"{base_url}{verification_url}"
    
    def _log_transaction(self, operation: str, certificate_hash: str, 
                        details: Dict) -> None:
        """Log blockchain transaction"""
        transaction = {
            'operation': operation,
            'certificate_hash': certificate_hash,
            'timestamp': datetime.now().isoformat(),
            'details': details,
            'network': self.network
        }
        self.transaction_log.append(transaction)
    
    def get_transaction_history(self, certificate_hash: str = None) -> list:
        """Get transaction history"""
        if certificate_hash:
            return [t for t in self.transaction_log 
                   if t['certificate_hash'] == certificate_hash]
        return self.transaction_log
    
    def export_certificate_json(self, certificate_hash: str) -> str:
        """Export certificate as JSON"""
        if certificate_hash not in self.certificates:
            return None
        
        certificate = self.certificates[certificate_hash]
        return json.dumps(certificate, indent=2)


# Global blockchain manager instance
blockchain_manager = BlockchainCertificateManager()
