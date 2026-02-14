#!/usr/bin/env python3
"""
Launcher simplificado para ADK Agent GUI.
Deixa a própria GUI gerenciar o ciclo de vida e threads do agente.
"""
import os
import sys
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Importar componentes
try:
    from gui import AgentGUI
except ImportError:
    # Adicionar diretório atual ao path se necessário
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from gui import AgentGUI

def main():
    """Inicia a GUI e aciona a conexão automática."""
    print("🚀 Iniciando ADK Agent GUI (Modo Simplificado)...")
    
    # Verificar API Key
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ ERRO: GEMINI_API_KEY não encontrada no .env")
        return

    # Instanciar a GUI
    app = AgentGUI()
    
    # Configurar auto-start seguro (agendado para logo após o loop iniciar)
    # REMOVIDO: Usuário prefere conexão manual
    # print("✅ Agendando conexão automática...")
    # app.root.after(1000, lambda: app.start_agent())
    
    # Iniciar loop principal (Bloqueante)
    try:
        app.run()
    except KeyboardInterrupt:
        print("⏹️ Encerrado pelo usuário via terminal")
    finally:
        print("👋 Bye!")

if __name__ == "__main__":
    main()
