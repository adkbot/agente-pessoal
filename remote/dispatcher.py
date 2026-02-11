"""
Dispatcher - Command Routing and Execution
Routes remote commands to appropriate system modules
"""
from remote.permission_guard import PermissionGuard, PermissionLevel
from remote.protocol import Protocol
from typing import Dict, Any


class Dispatcher:
    """
    Dispatches remote commands to the AntiGravity system
    Enforces permission checks before execution
    """
    
    def __init__(self, adk_system):
        self.adk = adk_system
        self.guard = PermissionGuard()
    
    def handle(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle incoming command
        
        Args:
            data: Command data dictionary
            
        Returns:
            dict: Response message
        """
        try:
            message_type = data.get("type")
            
            # Handle ping/pong
            if message_type == "ping":
                return Protocol.create_pong()
            
            # Handle status request
            if message_type == "status":
                status = self._get_system_status()
                return Protocol.create_status(status)
            
            # Handle command execution
            if message_type == "command":
                return self._execute_command(data)
            
            return Protocol.create_response(
                status="error",
                error="Unknown message type"
            )
            
        except Exception as e:
            return Protocol.create_response(
                status="error",
                error=str(e)
            )
    
    def _execute_command(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a command with permission check"""
        command = data.get("command")
        permission = data.get("permission")
        params = data.get("params", {})
        
        if not command:
            return Protocol.create_response(
                status="error",
                error="No command provided"
            )
        
        # Check permission if specified
        if permission:
            try:
                perm_level = PermissionLevel(permission)
                if not self.guard.check(perm_level):
                    return Protocol.create_response(
                        status="denied",
                        error=f"Permission {permission} not granted"
                    )
            except ValueError:
                return Protocol.create_response(
                    status="error",
                    error=f"Invalid permission level: {permission}"
                )
        
        # Execute command through ADK system
        try:
            result = self.adk.process_input(command)
            return Protocol.create_response(
                status="success",
                result=result
            )
        except Exception as e:
            return Protocol.create_response(
                status="error",
                error=f"Command execution failed: {str(e)}"
            )
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            # Get status from various system components
            return {
                "active": True,
                "mode": self.adk.config['system']['mode'],
                "risk_per_trade": self.adk.config['risk']['max_risk_per_trade'],
                "permissions": self.guard.get_status(),
                "timestamp": Protocol.create_status({})['timestamp']
            }
        except:
            return {
                "active": True,
                "status": "operational"
            }
