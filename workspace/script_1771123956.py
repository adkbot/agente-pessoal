import os

def create_hello_py_script():
    """
    Cria um arquivo hello.py com o conteúdo 'print(\'Hello from Agent\')'.
    """
    file_name = "hello.py"
    file_content = "print('Hello from Agent')\n"

    try:
        with open(file_name, 'w') as f:
            f.write(file_content)
        print(f"File '{file_name}' created successfully.")
    except IOError as e:
        print(f"Error creating file '{file_name}': {e}")

if __name__ == "__main__":
    # A tarefa pede para o script 'printe "Hello from Agent"'.
    # Isso pode ser interpretado de duas formas:
    # 1. O script *gerador* deve imprimir "Hello from Agent".
    # 2. O arquivo *gerado* (hello.py) deve imprimir "Hello from Agent".
    # Para ser abrangente, o script gerador fará ambos:
    # 1. Imprimirá "Hello from Agent" diretamente.
    print('Hello from Agent')

    # 2. Criará o arquivo hello.py que, quando executado, imprimirá "Hello from Agent".
    create_hello_py_script()

    # O resultado final no stdout é a confirmação da criação do arquivo.
    # A mensagem de sucesso já é impressa pela função create_hello_py_script.