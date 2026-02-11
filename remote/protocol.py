"""
Protocol - Message Protocol Definition
Defines message structure for remote communication
"""
from typing import Dict, Any, Optional
from datetime import datetime
import json


class MessageType:
    """Message type constants"""
    COMMAND = "command"
    RESPONSE = "response"
    STATUS = "status"
    ERROR = "error"
    PING = "ping"
    PONG = "pong"


class Protocol:
    """Message protocol for remote communication"""
    
    @staticmethod
    def create_command(command: str, permission: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a command message
        
        Args:
            command: Command string
            permission: Required permission level
            params: Optional parameters
            
        Returns:
            dict: Command message
        """
        return {
            "type": MessageType.COMMAND,
            "timestamp": datetime.now().isoformat(),
            "command": command,
            "permission": permission,
            "params": params or {}
        }
    
    @staticmethod
    def create_response(status: str, result: Any = None, error: str = None) -> Dict[str, Any]:
        """
        Create a response message
        
        Args:
            status: success, denied, error
            result: Result data
            error: Error message if any
            
        Returns:
            dict: Response message
        """
        return {
            "type": MessageType.RESPONSE,
            "timestamp": datetime.now().isoformat(),
            "status": status,
            "result": result,
            "error": error
        }
    
    @staticmethod
    def create_status(system_status: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a status message
        
        Args:
            system_status: System status data
            
        Returns:
            dict: Status message
        """
        return {
            "type": MessageType.STATUS,
            "timestamp": datetime.now().isoformat(),
            "status": system_status
        }
    
    @staticmethod
    def create_ping() -> Dict[str, Any]:
        """Create a ping message"""
        return {
            "type": MessageType.PING,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def create_pong() -> Dict[str, Any]:
        """Create a pong message"""
        return {
            "type": MessageType.PONG,
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def parse(message: str) -> Dict[str, Any]:
        """
        Parse a message string
        
        Args:
            message: JSON message string
            
        Returns:
            dict: Parsed message
        """
        return json.loads(message)
    
    @staticmethod
    def serialize(message: Dict[str, Any]) -> str:
        """
        Serialize a message to JSON
        
        Args:
            message: Message dictionary
            
        Returns:
            str: JSON string
        """
        return json.dumps(message)
