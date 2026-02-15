import os
import subprocess
import time
import re
from .llm_bridge import LLMBridge

class CoderAgent:
    def __init__(self):
        self.llm = LLMBridge()
        self.work_dir = os.path.join(os.getcwd(), "workspace")
        os.makedirs(self.work_dir, exist_ok=True)

    def write_code(self, task):
        prompt = f"""
        Você é um Programador Python Especialista.
        Tarefa: {task}
        
        Escreva um script Python completo que resolva esta tarefa.
        O script deve ser auto-contido e imprimir o resultado final no stdout.
        
        Responda APENAS com o código Python dentro de blocos ```python ... ```.
        Não explique nada.
        """
        response = self.llm.chat(prompt)
        
        # Extract code
        code_match = re.search(r'```python(.*?)```', response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
        else:
            code = response # Fallback if no block
            
        filename = os.path.join(self.work_dir, f"script_{int(time.time())}.py")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(code)
            
        return filename

    def run_with_correction(self, task, max_attempts=3):
        filename = self.write_code(task)
        
        for attempt in range(max_attempts):
            print(f"[CoderAgent] Executando {filename} (Tentativa {attempt+1}/{max_attempts})")
            
            result = subprocess.run(
                ["python", filename],
                capture_output=True,
                text=True,
                encoding="utf-8"
            )
            
            if result.returncode == 0:
                return f"Sucesso!\nOutput:\n{result.stdout}"
            
            # Failed, try to fix
            error_msg = result.stderr
            print(f"[CoderAgent] Erro na execução: {error_msg}")
            
            fix_prompt = f"""
            O script Python gerado falhou ao executar.
            Tarefa Original: {task}
            
            Código Atual:
            {open(filename, 'r', encoding='utf-8').read()}
            
            Erro Capturado (Stderr):
            {error_msg}
            
            Corrija o código para resolver o erro.
            Responda APENAS com o código Python corrigido dentro de ```python ... ```.
            """
            
            response = self.llm.chat(fix_prompt)
            code_match = re.search(r'```python(.*?)```', response, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(code)
            else:
                print("[CoderAgent] Não consegui extrair código na correção.")
        
        return f"Falha após {max_attempts} tentativas. Último erro: {error_msg}"
