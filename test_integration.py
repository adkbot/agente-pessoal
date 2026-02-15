
import os
import sys

# Add current dir to path
sys.path.append(os.getcwd())

print("Testing imports...")
try:
    from modules.browser import AutonomousBrowser
    from modules.planner import PlannerAgent
    from modules.coder import CoderAgent
    import skills
    print("Imports successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

print("\nTesting Coder Agent (Simple Task)...")
try:
    result = skills.skill_programador_autonomo("Escreva um script python que printe 'Hello from Agent' e salve em hello.py")
    print(f"Coder Result: {result}")
except Exception as e:
    print(f"Coder failed: {e}")

print("\nTesting Planner Agent (Instantiation)...")
try:
    planner = PlannerAgent()
    print("Planner initialized successfully.")
except Exception as e:
    print(f"Planner init failed: {e}")

print("\nVerification Complete.")
