import os
import time
import json
import re
import markdownify
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from .llm_bridge import LLMBridge

class Browser:
    def __init__(self, headless=False):
        self.driver = self._create_driver(headless)
        self.wait = WebDriverWait(self.driver, 10)

    def _create_driver(self, headless):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        
        # Anti-detect options
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-infobars")
        options.add_argument("--window-size=1920,1080")

        try:
            driver = uc.Chrome(options=options)
        except Exception as e:
            print(f"[Browser] Erro ao criar driver undetected, tentando normal: {e}")
            from selenium import webdriver
            driver = webdriver.Chrome(options=options)
        
        return driver

    def go_to(self, url):
        try:
            if not url.startswith("http"):
                url = "https://" + url
            self.driver.get(url)
            self._wait_for_load()
            return True
        except Exception as e:
            return f"Erro ao navegar: {e}"

    def _wait_for_load(self):
        time.sleep(2)
        try:
            WebDriverWait(self.driver, 5).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except:
            pass

    def get_markdown(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
            # Remove scripts, styles
            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()
            
            # Convert to markdown
            md = markdownify.markdownify(str(soup), heading_style="ATX")
            # Clean up empty lines
            lines = [line.strip() for line in md.splitlines() if line.strip()]
            return "\n".join(lines)[:15000] # Limit context
        except Exception as e:
            return f"Erro ao ler página: {e}"

    def get_links(self):
        links = []
        elements = self.driver.find_elements(By.TAG_NAME, "a")
        for el in elements:
            try:
                if el.is_displayed():
                    href = el.get_attribute("href")
                    text = el.text.strip()
                    if href and text and len(text) > 3:
                        links.append(f"[{text}]({href})")
            except:
                continue
        return links[:50] # Limit links

    def click_text(self, text):
        try:
            elements = self.driver.find_elements(By.TAG_NAME, "a") + self.driver.find_elements(By.TAG_NAME, "button")
            for el in elements:
                if text.lower() in el.text.lower():
                    el.click()
                    self._wait_for_load()
                    return f"Cliquei em '{text}'"
            return f"Não encontrei elemento com texto '{text}'"
        except Exception as e:
            return f"Erro ao clicar: {e}"
            
    def fill_input(self, placeholder_or_name, value):
        try:
            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for inp in inputs:
                attr = (inp.get_attribute("placeholder") or inp.get_attribute("name") or inp.get_attribute("id") or "").lower()
                if placeholder_or_name.lower() in attr:
                    inp.clear()
                    inp.send_keys(value)
                    return f"Digitei '{value}' em '{placeholder_or_name}'"
            return f"Input '{placeholder_or_name}' não encontrado"
        except Exception as e:
            return f"Erro ao digitar: {e}"

    def close(self):
        self.driver.quit()


class AutonomousBrowser:
    def __init__(self):
        self.browser = None
        self.llm = LLMBridge()

    def start_research(self, goal):
        if not self.browser:
            self.browser = Browser(headless=True) # Default headless for background work
        
        history = []
        max_steps = 10
        current_step = 0
        final_answer = ""

        # Step 1: Initial search (if not URL)
        if "http" not in goal:
            search_url = f"https://www.google.com/search?q={goal.replace(' ', '+')}"
            self.browser.go_to(search_url)
            history.append(f"Search: {goal}")
        else:
            self.browser.go_to(goal)
            history.append(f"Navigated to: {goal}")

        while current_step < max_steps:
            content = self.browser.get_markdown()
            current_url = self.browser.driver.current_url
            
            prompt = f"""
            Você é um Agente de Navegação Autônomo.
            Objetivo: {goal}
            
            URL Atual: {current_url}
            
            Conteúdo da Página (resumo):
            {content[:4000]}
            
            Histórico de ações:
            {history}
            
            Decida o próximo passo. Responda APENAS UM JSON no formato:
            {{
                "pensamento": "Seu raciocínio aqui",
                "acao": "clicar" | "digitar" | "google" | "finalizar",
                "detalhe": "texto do link" | "input_name:valor" | "novo termo busca" | "resumo final da resposta"
            }}
            """
            
            response = self.llm.chat(prompt)
            print(f"[AutonomousBrowser] Step {current_step}: {response}")
            
            try:
                # Extract JSON
                json_str = re.search(r'\{.*\}', response, re.DOTALL).group(0)
                plan = json.loads(json_str)
                
                action = plan.get("acao")
                detail = plan.get("detalhe")
                
                if action == "finalizar":
                    final_answer = detail
                    break
                
                elif action == "clicar":
                    res = self.browser.click_text(detail)
                    history.append(f"Clicou em '{detail}': {res}")
                
                elif action == "digitar":
                    if ":" in detail:
                        field, val = detail.split(":", 1)
                        res = self.browser.fill_input(field, val)
                        history.append(f"Digitou '{val}' em '{field}': {res}")
                
                elif action == "google":
                    url = f"https://www.google.com/search?q={detail.replace(' ', '+')}"
                    self.browser.go_to(url)
                    history.append(f"Google Search: {detail}")
                
                current_step += 1
                
            except Exception as e:
                print(f"[AutonomousBrowser] Erro no loop: {e}")
                current_step += 1
                
        self.browser.close()
        self.browser = None
        return final_answer or "Não consegui encontrar uma resposta conclusiva."
