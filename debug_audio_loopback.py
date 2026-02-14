
import pyaudio
import time
import audioop

def loopback_test():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 24000  # Mesmo rate do agente

    p = pyaudio.PyAudio()

    print("--- Audio Loopback Test ---")
    print("Fale no microfone. Você deve ouvir sua voz de volta.")
    print("Pressione Ctrl+C para parar.\n")

    try:
        # Tentar abrir default
        input_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        output_stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
        
        print("🎤 Microfone Aberto!")
        print("🔊 Alto-falante Aberto!")
        print("Iniciando loopback...\n")

        while True:
            data = input_stream.read(CHUNK, exception_on_overflow=False)
            rms = audioop.rms(data, 2)  # Medir volume
            
            # Visualização simples de volume
            bars = "█" * int(rms / 300)
            print(f"\rVolume: {rms:05d} {bars[:50]}", end="")
            
            output_stream.write(data)

    except KeyboardInterrupt:
        print("\nParando...")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        p.terminate()

if __name__ == "__main__":
    loopback_test()
