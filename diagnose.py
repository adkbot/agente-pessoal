
import asyncio
import sys
import os

print("🔍 Iniciando Diagnóstico de Hardware...")

async def test_audio():
    print("\n🎤 Testando Microfone (AudioCapture)...")
    try:
        from audio_capture import AudioCapture
        audio = AudioCapture()
        audio._open_mic()
        print("✅ Microfone aberto com sucesso!")
        audio.stop()
    except Exception as e:
        print(f"❌ Falha no Microfone: {e}")
        import traceback
        traceback.print_exc()

async def test_screen():
    print("\n🖥️ Testando Captura de Tela (ScreenCapture)...")
    try:
        from screen_capture import ScreenCapture
        screen = ScreenCapture()
        frame = screen.capture_frame()
        if frame and len(frame) > 100:
            print("✅ Captura de tela realizada com sucesso!")
        else:
            print("⚠️ Captura retornou dados vazios ou inválidos.")
    except Exception as e:
        print(f"❌ Falha na Captura de Tela: {e}")
        import traceback
        traceback.print_exc()

async def main():
    await test_audio()
    await test_screen()
    print("\nDiagnóstico concluído.")

if __name__ == "__main__":
    asyncio.run(main())
