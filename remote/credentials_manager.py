"""
Credentials Manager - Secure Credential Storage
Manages API keys and credentials for multiple brokers
"""
import json
import os
from cryptography.fernet import Fernet
from typing import Dict, Optional


class CredentialsManager:
    """
    Manages encrypted credentials for trading platforms
    Supports: Binance, Bybit, MT5, TradingView
    """
    
    def __init__(self, credentials_file="credentials.enc"):
        self.credentials_file = credentials_file
        self.key_file = ".cred_key"
        self.cipher = self._load_or_create_cipher()
        self.credentials = self._load_credentials()
    
    def _load_or_create_cipher(self) -> Fernet:
        """Load or create encryption key"""
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(key)
            print("🔐 Created new encryption key")
        
        return Fernet(key)
    
    def _load_credentials(self) -> Dict:
        """Load and decrypt credentials"""
        if not os.path.exists(self.credentials_file):
            return {}
        
        try:
            with open(self.credentials_file, "rb") as f:
                encrypted = f.read()
            
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted)
        except:
            print("⚠️ Failed to load credentials")
            return {}
    
    def _save_credentials(self):
        """Encrypt and save credentials"""
        data = json.dumps(self.credentials)
        encrypted = self.cipher.encrypt(data.encode())
        
        with open(self.credentials_file, "wb") as f:
            f.write(encrypted)
    
    def set_binance(self, api_key: str, api_secret: str):
        """Set Binance credentials"""
        self.credentials["binance"] = {
            "api_key": api_key,
            "api_secret": api_secret
        }
        self._save_credentials()
        print("✅ Binance credentials saved")
    
    def set_bybit(self, api_key: str, api_secret: str):
        """Set Bybit credentials"""
        self.credentials["bybit"] = {
            "api_key": api_key,
            "api_secret": api_secret
        }
        self._save_credentials()
        print("✅ Bybit credentials saved")
    
    def set_mt5(self, account: str, password: str, server: str):
        """Set MT5 credentials"""
        self.credentials["mt5"] = {
            "account": account,
            "password": password,
            "server": server
        }
        self._save_credentials()
        print("✅ MT5 credentials saved")
    
    def set_tradingview(self, username: str, password: str):
        """Set TradingView credentials"""
        self.credentials["tradingview"] = {
            "username": username,
            "password": password
        }
        self._save_credentials()
        print("✅ TradingView credentials saved")
    
    def get(self, platform: str) -> Optional[Dict]:
        """
        Get credentials for a platform
        
        Args:
            platform: binance, bybit, mt5, tradingview
            
        Returns:
            dict or None: Credentials if exist
        """
        return self.credentials.get(platform)
    
    def has(self, platform: str) -> bool:
        """Check if credentials exist for platform"""
        return platform in self.credentials
    
    def remove(self, platform: str):
        """Remove credentials for a platform"""
        if platform in self.credentials:
            del self.credentials[platform]
            self._save_credentials()
            print(f"🗑️ {platform} credentials removed")
    
    def list_platforms(self) -> list:
        """List platforms with stored credentials"""
        return list(self.credentials.keys())
    
    def export_to_env(self):
        """Export credentials to environment variables"""
        if "binance" in self.credentials:
            os.environ["BINANCE_API_KEY"] = self.credentials["binance"]["api_key"]
            os.environ["BINANCE_API_SECRET"] = self.credentials["binance"]["api_secret"]
        
        if "bybit" in self.credentials:
            os.environ["BYBIT_API_KEY"] = self.credentials["bybit"]["api_key"]
            os.environ["BYBIT_API_SECRET"] = self.credentials["bybit"]["api_secret"]
        
        if "mt5" in self.credentials:
            os.environ["MT5_ACCOUNT"] = self.credentials["mt5"]["account"]
            os.environ["MT5_PASSWORD"] = self.credentials["mt5"]["password"]
            os.environ["MT5_SERVER"] = self.credentials["mt5"]["server"]
        
        print("✅ Credentials exported to environment")
