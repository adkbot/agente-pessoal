"""
Permission Guard - Security Permission System
Manages authorization for critical system operations
"""
from enum import Enum
import json
import os


class PermissionLevel(Enum):
    """Permission levels for system operations"""
    SYSTEM_ACCESS = "system_access"
    BROWSER_AUTOMATION = "browser_automation"
    TRADE_EXECUTION = "trade_execution"
    FILE_MODIFICATION = "file_modification"
    API_CALL = "api_call"


class PermissionGuard:
    """
    Guards critical operations with permission checks
    First-time operations require explicit user confirmation
    """
    
    def __init__(self, config_file="config_permissions.json"):
        self.config_file = config_file
        self.permissions = self._load_permissions()
    
    def _load_permissions(self) -> dict:
        """Load permissions from config file"""
        if not os.path.exists(self.config_file):
            # Create default config with all permissions disabled
            default = {p.value: False for p in PermissionLevel}
            with open(self.config_file, "w") as f:
                json.dump(default, f, indent=4)
            print("🔐 Created new permissions config")
            return default
        
        with open(self.config_file, "r") as f:
            return json.load(f)
    
    def check(self, permission: PermissionLevel) -> bool:
        """
        Check if permission is granted
        If not previously granted, prompts user for confirmation
        
        Args:
            permission: Permission level to check
            
        Returns:
            bool: True if allowed, False if denied
        """
        allowed = self.permissions.get(permission.value, False)
        
        if not allowed:
            print(f"\n⚠️ Permissão necessária: {permission.value}")
            print(f"Descrição: {self._get_permission_description(permission)}")
            confirm = input("Autorizar execução? (yes/no): ")
            
            if confirm.lower() in ['yes', 'y', 'sim', 's']:
                # Grant permission permanently
                self.permissions[permission.value] = True
                with open(self.config_file, "w") as f:
                    json.dump(self.permissions, f, indent=4)
                print(f"✅ Permissão {permission.value} concedida")
                return True
            else:
                print(f"❌ Permissão {permission.value} negada")
                return False
        
        return True
    
    def _get_permission_description(self, permission: PermissionLevel) -> str:
        """Get human-readable description of permission"""
        descriptions = {
            PermissionLevel.SYSTEM_ACCESS: "Acesso ao sistema operacional",
            PermissionLevel.BROWSER_AUTOMATION: "Controle do navegador e automação web",
            PermissionLevel.TRADE_EXECUTION: "Execução de ordens de trading",
            PermissionLevel.FILE_MODIFICATION: "Modificação de arquivos no disco",
            PermissionLevel.API_CALL: "Chamadas para APIs externas"
        }
        return descriptions.get(permission, "Operação do sistema")
    
    def revoke(self, permission: PermissionLevel):
        """Revoke a previously granted permission"""
        self.permissions[permission.value] = False
        with open(self.config_file, "w") as f:
            json.dump(self.permissions, f, indent=4)
        print(f"🔒 Permissão {permission.value} revogada")
    
    def get_status(self) -> dict:
        """Get current permission status"""
        return self.permissions.copy()
