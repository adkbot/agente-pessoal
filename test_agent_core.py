
import asyncio
import os
from dotenv import load_dotenv
from agent_core import AgentCore

# Carregar variáveis de ambiente
load_dotenv()

async def main():
    print("🤖 Iniciando Teste do AgentCore (Headless)...")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ ERRO: GEMINI_API_KEY não encontrada.")
        return

    # Callback simples para printar texto
    def on_text(text):
        print(f"[AGENT] {text}")

    def on_status(status):
        print(f"[STATUS] {status}")

    def on_skill_log(log):
        print(f"[SKILL] {log}")

    try:
        agent = AgentCore(api_key=api_key, on_text=on_text, on_status=on_status, on_skill_log=on_skill_log)
        
        # Iniciar conexão (vai rodar por 10 segundos e parar)
        print("⏳ Conectando ao Gemini Live API...")
        
        from audio_capture import AudioCapture
        # from screen_capture import ScreenCapture

        audio = AudioCapture()
        
        # Criar task para parar depois de 10s
        async def stop_later():
            await asyncio.sleep(15)
            print("🛑 Parando teste...")
            agent.stop()
            audio.stop()

        async with asyncio.TaskGroup() as tg:
            tg.create_task(agent.run_with_reconnect())
            tg.create_task(audio.stream_mic(agent.audio_input_queue))
            tg.create_task(audio.play_audio(agent.audio_output_queue))
            tg.create_task(stop_later())
            
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        # Se for ExceptionGroup (Python 3.11+)
        if hasattr(e, 'exceptions'):
             for sub in e.exceptions:
                 print(f"  - Sub-erro: {sub}")

if __name__ == "__main__":
    asyncio.run(main())
