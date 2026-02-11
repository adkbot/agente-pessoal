"""
Security Module - HMAC Message Signing
Provides message authentication for remote commands
"""
import hmac
import hashlib
import os


# Load secret key from environment or use default
SECRET_KEY = os.getenv("ADK_SECRET", "CHANGE_THIS_SECRET_IN_PRODUCTION")


def sign_message(message: str) -> str:
    """
    Sign a message using HMAC-SHA256
    
    Args:
        message: Message to sign
        
    Returns:
        str: Hexadecimal signature
    """
    return hmac.new(
        SECRET_KEY.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()


def verify_signature(message: str, signature: str) -> bool:
    """
    Verify HMAC signature of a message
    
    Args:
        message: Original message
        signature: Signature to verify
        
    Returns:
        bool: True if valid, False otherwise
    """
    expected = sign_message(message)
    return hmac.compare_digest(expected, signature)


def create_signed_payload(data: dict) -> dict:
    """
    Create a signed payload
    
    Args:
        data: Data to sign
        
    Returns:
        dict: Data with signature
    """
    import json
    message = json.dumps(data, sort_keys=True)
    signature = sign_message(message)
    
    return {
        "data": data,
        "signature": signature
    }


def verify_signed_payload(payload: dict) -> tuple:
    """
    Verify a signed payload
    
    Args:
        payload: Payload with signature
        
    Returns:
        tuple: (is_valid: bool, data: dict or None)
    """
    import json
    
    data = payload.get("data")
    signature = payload.get("signature")
    
    if not data or not signature:
        return False, None
    
    message = json.dumps(data, sort_keys=True)
    is_valid = verify_signature(message, signature)
    
    return is_valid, data if is_valid else None
