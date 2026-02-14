"""
Módulo de captura e reprodução de áudio.
Captura do microfone em 16-bit PCM 16kHz mono.
Reproduz áudio de resposta a 24kHz.
"""

import asyncio
import pyaudio


class AudioCapture:
    """Gerencia entrada e saída de áudio com PyAudio."""

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    SEND_SAMPLE_RATE = 16000
    RECEIVE_SAMPLE_RATE = 24000
    CHUNK_SIZE = 1024

    def __init__(self):
        self.pya = pyaudio.PyAudio()
        self.mic_stream = None
        self.speaker_stream = None
        self.running = False
        self.mic_muted = False

    def _get_first_input_device(self):
        """Busca o primeiro dispositivo de entrada válido."""
        for i in range(self.pya.get_device_count()):
            try:
                info = self.pya.get_device_info_by_index(i)
                if info.get('maxInputChannels') > 0:
                    print(f"ℹ️ [AudioCapture] Usando microfone: {info.get('name')} (Index {i})")
                    return i
            except Exception:
                continue
        return None

    def _get_first_output_device(self):
        """Busca o primeiro dispositivo de saída válido."""
        for i in range(self.pya.get_device_count()):
            try:
                info = self.pya.get_device_info_by_index(i)
                if info.get('maxOutputChannels') > 0:
                    print(f"ℹ️ [AudioCapture] Usando alto-falante: {info.get('name')} (Index {i})")
                    return i
            except Exception:
                continue
        return None

    def _open_mic(self):
        """Abre o stream do microfone (tentativa simples)."""
        try:
            with open("startup_debug.log", "a") as f: f.write("DEBUG: Entrando em _open_mic\n")
            # Tentar abrir sem especificar index (usa default do OS)
            self.mic_stream = self.pya.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.SEND_SAMPLE_RATE,
                input=True,
                frames_per_buffer=self.CHUNK_SIZE,
            )
            print("ℹ️ [AudioCapture] Microfone aberto (Default OS)")
            return
        except Exception as e:
            print(f"⚠️ [AudioCapture] Erro ao abrir default: {e}. Tentando busca manual...")

        # Fallback manual
        device_index = self._get_first_input_device()
        if device_index is None:
            raise Exception("Nenhum microfone encontrado!")
            
        self.mic_stream = self.pya.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.SEND_SAMPLE_RATE,
            input=True,
            input_device_index=device_index,
            frames_per_buffer=self.CHUNK_SIZE,
        )
        print(f"ℹ️ [AudioCapture] Microfone aberto (Index {device_index})")

    def _open_speaker(self):
        """Abre o stream do alto-falante (tentativa simples)."""
        try:
            self.speaker_stream = self.pya.open(
                format=self.FORMAT,
                channels=self.CHANNELS,
                rate=self.RECEIVE_SAMPLE_RATE,
                output=True,
            )
            print("ℹ️ [AudioCapture] Alto-falante aberto (Default OS)")
            return
        except Exception as e:
            print(f"⚠️ [AudioCapture] Erro ao abrir speaker default: {e}. Tentando fallback...")

        device_index = self._get_first_output_device()
        kwargs = {
            "format": self.FORMAT,
            "channels": self.CHANNELS,
            "rate": self.RECEIVE_SAMPLE_RATE,
            "output": True
        }
        
        if device_index is not None:
             kwargs["output_device_index"] = device_index
            
        self.speaker_stream = self.pya.open(**kwargs)

    async def stream_mic(self, queue: asyncio.Queue):
        print("DEBUG: Iniciando stream_mic")
        """Loop assíncrono que captura áudio do microfone e coloca na fila."""
        self.running = True
        try:
            self._open_mic()
        except Exception as e:
            print(f"❌ [AudioCapture] Erro fatal ao abrir microfone: {e}")
            return

        while self.running:
            try:
                data = await asyncio.to_thread(
                    self.mic_stream.read, self.CHUNK_SIZE, exception_on_overflow=False
                )
                # print(f"[DEBUG] Mic data read: {len(data)} bytes")
                if not self.mic_muted:
                    msg = {"data": data, "mime_type": "audio/pcm"}
                    if queue.full():
                        try:
                            queue.get_nowait()
                        except asyncio.QueueEmpty:
                            pass
                    await queue.put(msg)
            except Exception as e:
                print(f"[AudioCapture] Erro leitura mic: {e}")
                await asyncio.sleep(0.1)



    def _log_to_file(self, msg):
        try:
            with open("audio_debug.log", "a", encoding='utf-8') as f:
                f.write(f"{msg}\n")
        except:
            pass

    async def play_audio(self, queue: asyncio.Queue):
        self._log_to_file("DEBUG: Iniciando play_audio loop")
        """Loop assíncrono que reproduz áudio da fila no alto-falante."""
        try:
            self._open_speaker()
            self._log_to_file("DEBUG: Speaker aberto com sucesso")
        except Exception as e:
            msg = f"❌ [AudioCapture] Erro fatal ao abrir auto-falante: {e}"
            print(msg)
            self._log_to_file(msg)
            return

        while True:
            try:
                self._log_to_file(f"DEBUG: Aguardando fila... (Tamanho: {queue.qsize()})")
                audio_data = await queue.get()
                self._log_to_file("DEBUG: Item retirado da fila")
                if audio_data is None:
                    self._log_to_file("DEBUG: Recebido sinal de parada (None)")
                    break
                
                size = len(audio_data)
                self._log_to_file(f"DEBUG: Escrevendo {size} bytes no speaker")
                
                # Tentar escrita direta para teste (bloqueante, mas elimina thread overhead)
                try:
                   self.speaker_stream.write(audio_data)
                except Exception as write_err:
                   self._log_to_file(f"ERRO WRITE: {write_err}")

            except Exception as e:
                print(f"[AudioCapture] Erro escrita speaker: {e}")
                self._log_to_file(f"ERRO LOOP: {e}")

    def toggle_mic(self):
        """Liga/desliga o microfone."""
        self.mic_muted = not self.mic_muted
        return self.mic_muted

    def stop(self):
        """Fecha todos os streams de áudio."""
        self.running = False
        if self.mic_stream:
            try:
                self.mic_stream.stop_stream()
                self.mic_stream.close()
            except Exception:
                pass
        if self.speaker_stream:
            try:
                self.speaker_stream.stop_stream()
                self.speaker_stream.close()
            except Exception:
                pass
        self.pya.terminate()
