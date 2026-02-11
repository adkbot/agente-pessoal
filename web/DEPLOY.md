# Deploy via GitHub - Passo a Passo

## ✅ Método Mais Simples: Importar do GitHub

Vou guiar você pelo deploy usando a interface web do Vercel (mais fácil!):

### 1️⃣ Acesse o Vercel Dashboard

👉 **https://vercel.com/new**

### 2️⃣ Faça Login/Cadastro

- Se já tem conta: Faça login
- Se não tem: Clique em "Sign Up" e use GitHub

### 3️⃣ Conecte o GitHub

1. Clique em **"Import Git Repository"**
2. Autorize o Vercel a acessar seu GitHub
3. Selecione o repositório onde está o código

### 4️⃣ Configure o Projeto

**No formulário de configuração:**

```
Project Name: antigravity-remote
Framework Preset: Next.js
Root Directory: web
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### 5️⃣ Variáveis de Ambiente (IMPORTANTE!)

Clique em "Environment Variables" e adicione:

```
ADK_SECRET = meu_segredo_super_forte_123
```

### 6️⃣ Deploy!

Clique no botão **"Deploy"**

Aguarde 1-2 minutos. Você verá:
```
✓ Building...
✓ Deploying...
✓ Ready!
```

### 7️⃣ Acesse Sua Aplicação

Você receberá uma URL tipo:
```
https://antigravity-remote.vercel.app
```

---

## 🔄 Alternativa: Deploy via CLI sem Login

Se preferir não fazer login, podemos:

1. **Fazer build local**:
```bash
cd web
npm run build
```

2. **Usar GitHub Actions** para deploy automático
3. **Ou usar outro serviço** (Netlify, Railway, etc.)

---

## 📸 Guia Visual

Siga estes passos na interface Vercel:

1. **Import Git Repository** → Escolha seu repo
2. **Configure Project** → Selecione pasta `web`
3. **Environment Variables** → Adicione `ADK_SECRET`
4. **Deploy** → Aguarde conclusão

---

## ✅ Verificação Pós-Deploy

Quando completar:

1. Abra a URL da produção
2. Verifique se a interface carrega
3. Teste: `https://sua-url.vercel.app/api/relay`
4. Deve retornar: `{"status":"operational",...}`

---

**Quer que eu teste o build local primeiro?** 
Isso garante que não haverá erros no deploy.
