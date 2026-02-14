"""
GUI Premium — Interface do Agente Pessoal ADK AGENT.
Dark theme com Tkinter, auto-falante, microfone, preview da tela e chat.
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import asyncio
import os
import sys
from PIL import Image, ImageTk
from dotenv import load_dotenv

# Importar core do agente
from agent_core import AgentCore
from audio_capture import AudioCapture
from screen_capture import ScreenCapture


class AgentGUI:
    """Interface gráfica premium para o agente multimodal."""

    # ═════════════════ CORES DO TEMA ═════════════════
    BG_DARK = "#0D1117"
    BG_CARD = "#161B22"
    BG_INPUT = "#21262D"
    BG_HOVER = "#30363D"
    TEXT_PRIMARY = "#E6EDF3"
    TEXT_SECONDARY = "#8B949E"
    ACCENT_BLUE = "#58A6FF"
    ACCENT_GREEN = "#3FB950"
    ACCENT_RED = "#F85149"
    ACCENT_PURPLE = "#BC8CFF"
    ACCENT_ORANGE = "#F0883E"
    BORDER = "#30363D"

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 ADK AGENT — Agente Pessoal Multimodal")
        self.root.configure(bg=self.BG_DARK)
        self.root.geometry("1100x750")
        self.root.minsize(900, 600)

        # Estado
        self.is_connected = False
        self.mic_muted = False
        self.screen_enabled = True
        self.preview_image = None
        
        # Referências para o backend
        self.agent_loop_thread = None
        self.agent = None
        self.audio = None
        self.screen = None
        self.stop_event = threading.Event()
        
        # Callbacks (definidos internamente agora)
        self.on_connect = self.start_agent
        self.on_disconnect = self.stop_agent
        self.on_toggle_mic = self.toggle_mic
        self.on_toggle_screen = self.toggle_screen
        self.on_send_text = self.send_text_to_agent
        
        self._setup_styles()
        self._build_ui()
        
        # Carregar variáveis de ambiente
        load_dotenv()
        
        # Iniciar loop de preview da câmera
        self.update_preview_loop()

        self.agent_loop = None  # Reference to the async loop in the backend thread
        
        # AUTO-START REMOVED

    def _setup_styles(self):
        """Configura estilos ttk."""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Dark.TFrame", background=self.BG_DARK)
        self.style.configure("Card.TFrame", background=self.BG_CARD)
        self.style.configure(
            "Dark.TLabel",
            background=self.BG_DARK,
            foreground=self.TEXT_PRIMARY,
            font=("Segoe UI", 10)
        )
        self.style.configure(
            "Title.TLabel",
            background=self.BG_DARK,
            foreground=self.ACCENT_BLUE,
            font=("Segoe UI", 18, "bold")
        )
        self.style.configure(
            "Subtitle.TLabel",
            background=self.BG_DARK,
            foreground=self.TEXT_SECONDARY,
            font=("Segoe UI", 9)
        )
        self.style.configure(
            "Card.TLabel",
            background=self.BG_CARD,
            foreground=self.TEXT_PRIMARY,
            font=("Segoe UI", 10)
        )

    def _build_ui(self):
        """Constrói a interface."""
        # ─── Header ────────────────────────────
        header_frame = tk.Frame(self.root, bg=self.BG_DARK, pady=10, padx=20)
        header_frame.pack(fill="x")

        tk.Label(
            header_frame, text="🤖 ADK AGENT",
            bg=self.BG_DARK, fg=self.ACCENT_BLUE,
            font=("Segoe UI", 22, "bold")
        ).pack(side="left")

        tk.Label(
            header_frame, text="  Agente Pessoal Multimodal — Gemini Live API",
            bg=self.BG_DARK, fg=self.TEXT_SECONDARY,
            font=("Segoe UI", 11)
        ).pack(side="left", padx=(5, 0))

        # Status indicator
        self.status_label = tk.Label(
            header_frame, text="⚫ Desconectado",
            bg=self.BG_DARK, fg=self.TEXT_SECONDARY,
            font=("Segoe UI", 10)
        )
        self.status_label.pack(side="right")

        # Separator
        tk.Frame(self.root, bg=self.BORDER, height=1).pack(fill="x")

        # ─── Main Container ────────────────────
        main_frame = tk.Frame(self.root, bg=self.BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Left Panel (Controls + Preview)
        left_panel = tk.Frame(main_frame, bg=self.BG_DARK, width=350)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        left_panel.pack_propagate(False)

        self._build_controls(left_panel)
        self._build_preview(left_panel)
        self._build_skills_log(left_panel)

        # Right Panel (Chat)
        right_panel = tk.Frame(main_frame, bg=self.BG_DARK)
        right_panel.pack(side="right", fill="both", expand=True)

        self._build_chat(right_panel)

    def _build_controls(self, parent):
        """Constrói painel de controles."""
        # Card frame
        card = tk.Frame(parent, bg=self.BG_CARD, bd=0, highlightthickness=1,
                       highlightbackground=self.BORDER, highlightcolor=self.BORDER)
        card.pack(fill="x", pady=(0, 10))

        inner = tk.Frame(card, bg=self.BG_CARD, padx=15, pady=12)
        inner.pack(fill="x")

        tk.Label(
            inner, text="⚡ Controles",
            bg=self.BG_CARD, fg=self.ACCENT_PURPLE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        # Botão Conectar/Desconectar
        btn_frame = tk.Frame(inner, bg=self.BG_CARD, pady=8)
        btn_frame.pack(fill="x")

        self.connect_btn = tk.Button(
            btn_frame, text="▶  INICIAR AGENTE",
            bg=self.ACCENT_GREEN, fg="#FFFFFF",
            font=("Segoe UI", 11, "bold"),
            activebackground="#2EA043", activeforeground="#FFFFFF",
            relief="flat", cursor="hand2", pady=8,
            command=self._toggle_connection
        )
        self.connect_btn.pack(fill="x")

        # Botões Mic e Tela
        toggle_frame = tk.Frame(inner, bg=self.BG_CARD, pady=4)
        toggle_frame.pack(fill="x")

        self.mic_btn = tk.Button(
            toggle_frame, text="🎤 Mic ON",
            bg=self.BG_INPUT, fg=self.ACCENT_GREEN,
            font=("Segoe UI", 10), relief="flat",
            cursor="hand2", pady=5,
            command=self._toggle_mic
        )
        self.mic_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))

        self.screen_btn = tk.Button(
            toggle_frame, text="🖥️ Tela ON",
            bg=self.BG_INPUT, fg=self.ACCENT_GREEN,
            font=("Segoe UI", 10), relief="flat",
            cursor="hand2", pady=5,
            command=self._toggle_screen
        )
        self.screen_btn.pack(side="right", fill="x", expand=True, padx=(4, 0))

    def _build_preview(self, parent):
        """Constrói preview da tela."""
        card = tk.Frame(parent, bg=self.BG_CARD, bd=0, highlightthickness=1,
                       highlightbackground=self.BORDER, highlightcolor=self.BORDER)
        card.pack(fill="x", pady=(0, 10))

        inner = tk.Frame(card, bg=self.BG_CARD, padx=15, pady=12)
        inner.pack(fill="x")

        tk.Label(
            inner, text="👁️ Visão do Agente",
            bg=self.BG_CARD, fg=self.ACCENT_ORANGE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        self.preview_canvas = tk.Canvas(
            inner, width=320, height=180,
            bg="#000000", highlightthickness=0
        )
        self.preview_canvas.pack()
        self.preview_canvas.create_text(
            160, 90, text="Aguardando conexão...",
            fill=self.TEXT_SECONDARY, font=("Segoe UI", 10)
        )

    def _build_skills_log(self, parent):
        """Constrói log de skills executadas."""
        card = tk.Frame(parent, bg=self.BG_CARD, bd=0, highlightthickness=1,
                       highlightbackground=self.BORDER, highlightcolor=self.BORDER)
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=self.BG_CARD, padx=15, pady=12)
        inner.pack(fill="both", expand=True)

        tk.Label(
            inner, text="🔧 Skills Executadas",
            bg=self.BG_CARD, fg=self.ACCENT_BLUE,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w", pady=(0, 8))

        self.skills_log = scrolledtext.ScrolledText(
            inner, width=35, height=8,
            bg="#0D1117", fg=self.TEXT_SECONDARY,
            font=("Cascadia Code", 8),
            relief="flat", insertbackground=self.TEXT_PRIMARY,
            selectbackground=self.ACCENT_BLUE,
            wrap="word", state="disabled"
        )
        self.skills_log.pack(fill="both", expand=True)

    def _build_chat(self, parent):
        """Constrói área de chat."""
        # Card frame
        card = tk.Frame(parent, bg=self.BG_CARD, bd=0, highlightthickness=1,
                       highlightbackground=self.BORDER, highlightcolor=self.BORDER)
        card.pack(fill="both", expand=True)

        inner = tk.Frame(card, bg=self.BG_CARD, padx=15, pady=12)
        inner.pack(fill="both", expand=True)

        # Header do chat
        chat_header = tk.Frame(inner, bg=self.BG_CARD)
        chat_header.pack(fill="x", pady=(0, 10))

        tk.Label(
            chat_header, text="💬 Chat — Respostas do Agente",
            bg=self.BG_CARD, fg=self.ACCENT_GREEN,
            font=("Segoe UI", 13, "bold")
        ).pack(side="left")

        # Área de texto do chat
        self.chat_display = scrolledtext.ScrolledText(
            inner, width=50, height=20,
            bg=self.BG_DARK, fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 11),
            relief="flat", insertbackground=self.TEXT_PRIMARY,
            selectbackground=self.ACCENT_BLUE,
            wrap="word", state="disabled",
            padx=10, pady=10
        )
        self.chat_display.pack(fill="both", expand=True)

        # Tags para formatação
        self.chat_display.tag_config("agent", foreground=self.ACCENT_GREEN)
        self.chat_display.tag_config("user", foreground=self.ACCENT_BLUE)
        self.chat_display.tag_config("system", foreground=self.ACCENT_ORANGE)
        self.chat_display.tag_config("timestamp", foreground=self.TEXT_SECONDARY)

        # Input frame
        input_frame = tk.Frame(inner, bg=self.BG_CARD, pady=10)
        input_frame.pack(fill="x")

        self.text_input = tk.Entry(
            input_frame,
            bg=self.BG_INPUT, fg=self.TEXT_PRIMARY,
            font=("Segoe UI", 11),
            relief="flat", insertbackground=self.TEXT_PRIMARY,
            selectbackground=self.ACCENT_BLUE
        )
        self.text_input.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 8))
        self.text_input.bind("<Return>", self._send_text)
        self.text_input.insert(0, "Digite uma mensagem ou fale pelo microfone...")
        self.text_input.bind("<FocusIn>", self._clear_placeholder)
        self.text_input.bind("<FocusOut>", self._restore_placeholder)

        send_btn = tk.Button(
            input_frame, text="📤 Enviar",
            bg=self.ACCENT_BLUE, fg="#FFFFFF",
            font=("Segoe UI", 10, "bold"),
            activebackground="#1F6FEB", activeforeground="#FFFFFF",
            relief="flat", cursor="hand2", padx=15, pady=5,
            command=lambda: self._send_text(None)
        )
        send_btn.pack(side="right")

    # ═══════════════════════════════════════════════════
    # Lógica de Integração (Backend)
    # ═══════════════════════════════════════════════════

    def start_agent(self):
        """Inicia o agente (backend) em uma thread separada."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            self.add_chat_message("❌ ERRO: GEMINI_API_KEY não encontrada no .env", "system")
            # Reseta estado visual
            self.root.after(1000, lambda: self.set_connected(False))
            return

        self.stop_event.clear()
        
        def _run_async_backend():
            # Criar loop para esta thread
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.agent_loop = loop  # Guardar referência do loop
            
            try:
                # 1. Instanciar Agente
                self.agent = AgentCore(
                    api_key=api_key,
                    on_text=lambda t: self.add_chat_message(f"🤖 {t}", "agent"),
                    on_status=self.update_status,
                    on_skill_log=self.add_skill_log
                )

                # 2. Instanciar Captura
                self.audio = AudioCapture()
                # Atualizar estado inicial do mute
                self.audio.mic_muted = self.mic_muted
                
                # self.screen = ScreenCapture(fps=1.0)
                
                # Definir callbacks de fila
                # O AgentCore já cria as filas: audio_input_queue, screen_input_queue, audio_output_queue
                
                # 3. Rodar Tasks
                async def main_tasks():
                    async with asyncio.TaskGroup() as tg:
                        # Task principal do agente
                        self.agent.running = True # EVITAR RACE CONDITION
                        tg.create_task(self.agent.run_with_reconnect())
                        
                        # Tasks de I/O
                        tg.create_task(self.audio.stream_mic(self.agent.audio_input_queue))
                        tg.create_task(self.audio.play_audio(self.agent.audio_output_queue))
                        # tg.create_task(self.screen.stream_frames(self.agent.screen_input_queue))
                        
                        # Monitorar stop_event
                        while not self.stop_event.is_set() and self.agent.running:
                            await asyncio.sleep(0.5)
                        
                        # Quando sair do loop, parar tudo
                        self.agent.stop()
                        self.audio.stop()
                        # self.screen.stop()

                # Sinalizar sucesso na GUI
                self.set_connected(True)
                
                # Bloquear rodando tasks
                loop.run_until_complete(main_tasks())
            
            except Exception as e:
                error_msg = f"❌ Erro fatal no backend: {e}"
                
                # Tentar extrair erros do TaskGroup (ExceptionGroup)
                if hasattr(e, 'exceptions'):
                    error_msg += "\nDetalhes:"
                    for sub_e in e.exceptions:
                        error_msg += f"\n - {sub_e}"
                
                self.add_chat_message(error_msg, "system")
                print(f"Erro backend: {e}")
                if hasattr(e, 'exceptions'):
                    for sub_e in e.exceptions:
                        print(f"  - Sub-erro: {sub_e}")
                        import traceback
                        traceback.print_exception(type(sub_e), sub_e, sub_e.__traceback__)
            finally:
                loop.close()
                self.agent_loop = None
                self.set_connected(False)
        
        # Iniciar thread
        self.agent_loop_thread = threading.Thread(target=_run_async_backend, daemon=True)
        self.agent_loop_thread.start()

    def stop_agent(self):
        """Para o agente."""
        # Feedback visual IMEDIATO
        self.stop_btn.configure(state="disabled", text="Parando...")
        self.add_chat_message("🛑 Parando sistema...", "system")
        self.stop_event.set()
        
        # Sinalizar parada para o agente (não bloqueante)
        if self.agent:
            self.agent.stop()
        
        # Não chamar self.audio.stop() aqui para não travar a GUI
        # A thread de background fará o cleanup com segurança
        
        # A thread vai perceber o evento, encerará as tasks
        # E o callback finally da thread vai chamar self.set_connected(False)

    def toggle_mic(self):
        """Alterna mute do microfone."""
        # Visual
        # Lógica backend
        if self.audio:
            muted = self.audio.toggle_mic() # AudioCapture tem toggle_mic que retorna estado
            self.mic_muted = muted
        else:
            self.mic_muted = not self.mic_muted
            
        self.update_mic_state(self.mic_muted)

    def toggle_screen(self):
        """Alterna envio de tela (pausa captura)."""
        self.screen_enabled = not self.screen_enabled
        if self.screen:
            self.screen.running = self.screen_enabled # Hack para pausar loop do ScreenCapture se suportado
            # Se ScreenCapture não tiver suporte nativo a pause em tempo real, 
            # podemos implementar depois. Por enquanto muda só visual e flag.
        
        if self.screen_enabled:
            self.screen_btn.config(text="🖥️ Tela ON", fg=self.ACCENT_GREEN)
        else:
            self.screen_btn.config(text="🖥️ Tela OFF", fg=self.ACCENT_RED)

    def send_text_to_agent(self, text: str):
        """Envia texto para o agente (thread-safe)."""
        if self.agent and self.agent.running and self.agent_loop:
            # Enviar texto de forma thread-safe usando o loop do backend
            try:
                asyncio.run_coroutine_threadsafe(
                    self.agent.send_text(text), 
                    self.agent_loop
                )
            except Exception as e:
                self.add_chat_message(f"❌ Erro ao enviar texto: {e}", "system")
        else:
            self.add_chat_message("⚠️ Conecte o agente primeiro!", "system")

    def update_preview_loop(self):
        """Loop independente para atualizar o preview da tela na GUI."""
        if self.is_connected and self.screen_enabled:
            # Usar ScreenCapture estático para preview (não precisa da instância do agente)
            try:
                # Criar instância temporária só para um frame é ineficiente, 
                # mas o ScreenCapture atual cria mss() a cada chamada, então ok.
                # Melhor usar o método estático ou criar uma instância global de preview.
                preview_capture = ScreenCapture() 
                img = preview_capture.capture_frame_pil() # Retorna PIL Image
                self.update_preview(img)
            except Exception:
                pass
        
        # Reagendar
        self.root.after(200, self.update_preview_loop) # 5 FPS no preview

    # ═══════════════════════════════════════════════════
    # Callbacks da UI (Acionadores)
    # ═══════════════════════════════════════════════════

    def _toggle_connection(self):
        """Alterna entre conectar e desconectar."""
        if not self.is_connected:
            self.connect_btn.config(text="⏳ Conectando...", bg=self.ACCENT_ORANGE, state="disabled")
            if self.on_connect:
                self.on_connect()
        else:
            if self.on_disconnect:
                self.on_disconnect()

    def _toggle_mic(self):
        if self.on_toggle_mic:
            self.on_toggle_mic()

    def _toggle_screen(self):
        if self.on_toggle_screen:
            self.on_toggle_screen()

    def _send_text(self, event):
        text = self.text_input.get().strip()
        placeholder = "Digite uma mensagem ou fale pelo microfone..."
        if text and text != placeholder:
            self.add_chat_message(f"Você: {text}", "user")
            self.text_input.delete(0, "end")
            if self.on_send_text:
                self.on_send_text(text)

    def _clear_placeholder(self, event):
        placeholder = "Digite uma mensagem ou fale pelo microfone..."
        if self.text_input.get() == placeholder:
            self.text_input.delete(0, "end")
            self.text_input.config(fg=self.TEXT_PRIMARY)

    def _restore_placeholder(self, event):
        if not self.text_input.get():
            self.text_input.insert(0, "Digite uma mensagem ou fale pelo microfone...")
            self.text_input.config(fg=self.TEXT_SECONDARY)

    # ═══════════════════════════════════════════════════
    # Métodos públicos (thread-safe) para UI
    # ═══════════════════════════════════════════════════

    def set_connected(self, connected: bool):
        """Atualiza estado de conexão (thread-safe)."""
        def _update():
            self.is_connected = connected
            if connected:
                self.connect_btn.config(
                    text="⏹  PARAR AGENTE",
                    bg=self.ACCENT_RED, state="normal"
                )
                self.status_label.config(text="🟢 Conectado", fg=self.ACCENT_GREEN)
            else:
                self.connect_btn.config(
                    text="▶  INICIAR AGENTE",
                    bg=self.ACCENT_GREEN, state="normal"
                )
                self.status_label.config(text="⚫ Desconectado", fg=self.TEXT_SECONDARY)
        self.root.after(0, _update)

    def update_status(self, text: str):
        """Atualiza o status (thread-safe)."""
        def _update():
            self.status_label.config(text=text)
        self.root.after(0, _update)

    def add_chat_message(self, message: str, tag: str = "agent"):
        """Adiciona mensagem ao chat (thread-safe)."""
        def _update():
            self.chat_display.config(state="normal")
            self.chat_display.insert("end", message + "\n", tag)
            self.chat_display.see("end")
            self.chat_display.config(state="disabled")
        self.root.after(0, _update)

    def add_skill_log(self, message: str):
        """Adiciona log de skill (thread-safe)."""
        def _update():
            self.skills_log.config(state="normal")
            self.skills_log.insert("end", message + "\n")
            self.skills_log.see("end")
            self.skills_log.config(state="disabled")
        self.root.after(0, _update)

    def update_mic_state(self, muted: bool):
        """Atualiza estado visual do microfone."""
        def _update():
            self.mic_muted = muted
            if muted:
                self.mic_btn.config(text="🎤 Mic OFF", fg=self.ACCENT_RED)
            else:
                self.mic_btn.config(text="🎤 Mic ON", fg=self.ACCENT_GREEN)
        self.root.after(0, _update)

    def update_preview(self, pil_image):
        """Atualiza preview da tela (thread-safe)."""
        def _update():
            try:
                self.preview_image = ImageTk.PhotoImage(pil_image)
                self.preview_canvas.delete("all")
                self.preview_canvas.create_image(0, 0, anchor="nw", image=self.preview_image)
            except Exception:
                pass
        self.root.after(0, _update)

    def run(self):
        """Inicia o loop principal do Tkinter."""
        self.root.mainloop()

    def destroy(self):
        """Fecha a janela."""
        self.stop_agent()
        try:
            self.root.quit()
            self.root.destroy()
        except Exception:
            pass


if __name__ == "__main__":
    app = AgentGUI()
    app.run()
