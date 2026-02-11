# Remote Control Module

Sistema de controle remoto para o AntiGravity Trading System.

## 🏗️ Arquitetura

```
remote/
├── permission_guard.py    # Sistema de permissões (5 níveis)
├── security.py            # Assinatura HMAC de mensagens
├── protocol.py            # Protocolo de mensagens
├── dispatcher.py          # Roteamento de comandos
├── client.py              # Cliente WebSocket
└── credentials_manager.py # Gerenciador de credenciais criptografadas
```

## 🔐 Níveis de Permissão

O sistema implementa 5 níveis de permissão obrigatórios:

1. **`system_access`** - Acesso ao sistema operacional
2. **`browser_automation`** - Controle do navegador
3. **`trade_execution`** - Execução de ordens
4. **`file_modification`** - Modificação de arquivos
5. **`api_call`** - Chamadas para APIs externas

### Funcionamento

- **Primeira execução**: Solicita confirmação do usuário
- **Confirmado**: Salva permanentemente em `config_permissions.json`
- **Negado**: Bloqueia a operação

## 🔒 Segurança

### Assinatura de Mensagens (HMAC)

Todas as mensagens são assinadas com HMAC-SHA256:

```python
from remote.security import sign_message, verify_signature

# Assinar
signature = sign_message("meu comando")

# Verificar
is_valid = verify_signature("meu comando", signature)
```

### Credenciais Criptografadas

Credenciais são armazenadas com criptografia Fernet:

```python
from remote.credentials_manager import CredentialsManager

creds = CredentialsManager()

# Salvar
creds.set_binance("api_key", "api_secret")

# Recuperar
binance = creds.get("binance")
```

**Arquivos gerados:**
- `.cred_key` - Chave de criptografia (NÃO compartilhar)
- `credentials.enc` - Credenciais criptografadas

⚠️ **Ambos estão no `.gitignore`**

## 📡 WebSocket Client

Cliente com reconexão automática:

```python
from remote.client import RemoteClient

# Modo blocking
client = RemoteClient(adk_system)
client.start()

# Modo background
client.start_background()
```

### Configuração

Servidor via variável de ambiente:

```bash
export ADK_RELAY_URL="wss://seu-relay.vercel.app/ws"
```

## 🎯 Uso

### 1. Modo Interativo (padrão)

```bash
python main.py
```

### 2. Modo Remoto (apenas WebSocket)

```bash
python main.py --mode remote
```

### 3. Modo Híbrido (local + remoto)

```bash
python main.py --mode both
```

## 📨 Protocolo de Mensagens

### Comando

```json
{
  "type": "command",
  "timestamp": "2026-02-11T11:30:00",
  "command": "comprar BTC 0.01",
  "permission": "trade_execution",
  "params": {}
}
```

### Resposta

```json
{
  "type": "response",
  "timestamp": "2026-02-11T11:30:01",
  "status": "success",
  "result": "Ordem executada",
  "error": null
}
```

### Status

```json
{
  "type": "status",
  "timestamp": "2026-02-11T11:30:00",
  "status": {
    "active": true,
    "mode": "institutional",
    "permissions": {...}
  }
}
```

## 🧪 Testes

### Testar Permissões

```python
from remote.permission_guard import PermissionGuard, PermissionLevel

guard = PermissionGuard()
allowed = guard.check(PermissionLevel.TRADE_EXECUTION)
```

### Testar Dispatcher

```python
from remote.dispatcher import Dispatcher
from remote.protocol import Protocol

dispatcher = Dispatcher(adk_system)

command = Protocol.create_command(
    "comprar BTC 0.01",
    "trade_execution"
)

response = dispatcher.handle(command)
print(response)
```

## 🔑 Gerenciamento de Credenciais

### Binance

```python
creds.set_binance(
    api_key="sua_api_key",
    api_secret="seu_api_secret"
)
```

### Bybit

```python
creds.set_bybit(
    api_key="sua_api_key",
    api_secret="seu_api_secret"
)
```

### MT5

```python
creds.set_mt5(
    account="12345678",
    password="sua_senha",
    server="MetaQuotes-Demo"
)
```

### TradingView

```python
creds.set_tradingview(
    username="seu_usuario",
    password="sua_senha"
)
```

### Exportar para Ambiente

```python
creds.export_to_env()
# Agora as credenciais estão em os.environ
```

## ⚠️ Segurança em Produção

1. **Mudar SECRET_KEY**:
   ```bash
   export ADK_SECRET="seu_segredo_forte_aqui"
   ```

2. **Usar WSS** (não WS):
   ```bash
   export ADK_RELAY_URL="wss://relay.com/ws"
   ```

3. **Rate Limiting**: Implementar no relay

4. **IP Whitelist**: Apenas IPs confiáveis

5. **Logs**: Registrar todas as execuções

## 📚 Dependências

```bash
pip install websockets cryptography
```

## 🔗 Integração com Web UI

O módulo é usado pela interface web Next.js para:
- Enviar comandos remotos
- Gerenciar credenciais via modal
- Controlar permissões
- Receber status em tempo real

---

**Resultado**: Sistema de controle remoto profissional com segurança enterprise-grade.
