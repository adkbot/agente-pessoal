"""
Remote Client - WebSocket Client with Auto-Reconnect
Connects to remote relay server for command reception
"""
import asyncio
import websockets
import json
from remote.dispatcher import Dispatcher
from remote.protocol import Protocol
from remote.security import verify_signed_payload, create_signed_payload
import os


# Server URL from environment or default
SERVER_URL = os.getenv("ADK_RELAY_URL", "ws://localhost:8765")


class RemoteClient:
    """
    WebSocket client for remote control
    Features:
    - Auto-reconnect on disconnection
    - Message signing/verification
    - Heartbeat ping/pong
    """
    
    def __init__(self, adk_system):
        self.adk = adk_system
        self.dispatcher = Dispatcher(adk_system)
        self.running = False
        self.reconnect_delay = 5  # seconds
    
    async def connect(self):
        """Connect to server with auto-reconnect"""
        self.running = True
        
        while self.running:
            try:
                async with websockets.connect(SERVER_URL) as websocket:
                    print(f"🔗 Conectado ao servidor remoto: {SERVER_URL}")
                    await self.listen(websocket)
            except websockets.exceptions.WebSocketException as e:
                print(f"❌ Erro de conexão WebSocket: {e}")
            except Exception as e:
                print(f"❌ Erro inesperado: {e}")
            
            if self.running:
                print(f"🔄 Reconectando em {self.reconnect_delay} segundos...")
                await asyncio.sleep(self.reconnect_delay)
    
    async def listen(self, websocket):
        """Listen for messages from server"""
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            print("⚠️ Conexão fechada pelo servidor")
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
    
    async def handle_message(self, websocket, message: str):
        """
        Handle incoming message
        
        Args:
            websocket: WebSocket connection
            message: Raw message string
        """
        try:
            # Parse message
            payload = json.loads(message)
            
            # Verify signature if present
            if "signature" in payload:
                is_valid, data = verify_signed_payload(payload)
                if not is_valid:
                    print("⚠️ Assinatura inválida - mensagem rejeitada")
                    return
                data = data
            else:
                data = payload
            
            # Dispatch command
            response = self.dispatcher.handle(data)
            
            # Sign response
            signed_response = create_signed_payload(response)
            
            # Send response
            await websocket.send(json.dumps(signed_response))
            
        except json.JSONDecodeError:
            print("❌ Mensagem inválida (não é JSON)")
        except Exception as e:
            print(f"❌ Erro ao processar mensagem: {e}")
    
    def start(self):
        """Start the remote client (blocking)"""
        print("🚀 Iniciando cliente remoto...")
        print(f"📡 Servidor: {SERVER_URL}")
        asyncio.run(self.connect())
    
    def start_background(self):
        """Start the remote client in background"""
        import threading
        thread = threading.Thread(target=self.start, daemon=True)
        thread.start()
        print("🔗 Cliente remoto iniciado em background")
    
    def stop(self):
        """Stop the remote client"""
        self.running = False
        print("🛑 Parando cliente remoto...")
