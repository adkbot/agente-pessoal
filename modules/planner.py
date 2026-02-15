import json
import re
from .llm_bridge import LLMBridge
from .browser import AutonomousBrowser
from .coder import CoderAgent

class PlannerAgent:
    def __init__(self):
        self.llm = LLMBridge()
        self.browser = AutonomousBrowser()
        self.coder = CoderAgent()

    def execute_plan(self, goal):
        prompt = f"""
        Você é um Planejador Mestre de IA.
        Objetivo Complexo: {goal}
        
        Sua tarefa é quebrar este objetivo em uma lista de passos SEQUENCIAIS.
        Para cada passo, escolha o agente mais adequado:
        - "browser": Para pesquisar na internet, ler sites, buscar informações.
        - "coder": Para escrever scripts Python, fazer cálculos, processar arquivos, gerar gráficos.
        - "casual": Para responder perguntas simples ou sumarizar informações finais.
        
        Formato de Resposta (JSON):
        {{
            "plano": [
                {{
                    "passo": 1,
                    "agente": "browser" | "coder" | "casual",
                    "tarefa": "Descrição detalhada do que este agente deve fazer neste passo"
                }},
                ...
            ]
        }}
        """
        response = self.llm.chat(prompt)
        
        try:
            json_str = re.search(r'\{.*\}', response, re.DOTALL).group(0)
            plan_data = json.loads(json_str)
            plan = plan_data.get("plano", [])
            
            results = []
            
            for step in plan:
                agent_type = step["agente"]
                task_desc = step["tarefa"]
                
                print(f"[Planner] Executando Passo {step['passo']} ({agent_type}): {task_desc}")
                
                step_result = ""
                if agent_type == "browser":
                    step_result = self.browser.start_research(task_desc)
                elif agent_type == "coder":
                    step_result = self.coder.run_with_correction(task_desc)
                else: # casual
                    context = "\n".join(results)
                    step_result = self.llm.chat(f"Contexto anterior:\n{context}\n\nTarefa atual: {task_desc}")
                
                results.append(f"Passo {step['passo']} ({agent_type}): {step_result}")
                
            return "\n\n".join(results)

        except Exception as e:
            return f"Erro no planejamento: {e}"
