
import pyaudio
import numpy as np
import time

def generate_tone():
    p = pyaudio.PyAudio()
    
    # Parâmetros iguais ao agente
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 24000
    
    print(f"Generating tone with: Rate={RATE}, Channels={CHANNELS}, Format=Int16")
    
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True)
                        
        print("Playing 440Hz tone for 3 seconds...")
        
        # Gerar onda senoidal
        duration = 3.0
        frequency = 440.0
        
        # Gerar samples
        samples = (np.sin(2*np.pi*np.arange(RATE*duration)*frequency/RATE)).astype(np.float32)
        # Converter para Int16
        audio_data = (samples * 32767).astype(np.int16).tobytes()
        
        stream.write(audio_data)
        
        print("Tone finished.")
        stream.stop_stream()
        stream.close()
    except Exception as e:
        print(f"Error playing tone: {e}")
    finally:
        p.terminate()

if __name__ == "__main__":
    try:
        import numpy
        generate_tone()
    except ImportError:
        print("Installing numpy...")
        import subprocess
        subprocess.check_call(["pip", "install", "numpy"])
        import numpy
        generate_tone()
