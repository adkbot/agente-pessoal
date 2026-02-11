# AntiGravity Remote Control - Web Interface

Professional web interface for the AntiGravity Trading System.

## 🚀 Running Locally

```bash
cd web
npm install
npm run dev
```

Access: http://localhost:3000

## 📦 Features

- **Command Interface** - Send trading commands remotely
- **Permission System** - 5-level permission selector
- **Credentials Management** - Secure storage for 4 platforms
- **Voice Controls** - Speech-to-text command input
- **Response History** - Track all commands and responses
- **Real-time Status** - Connection status indicator

## 🏗️ Architecture

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Icons**: Lucide React

### API Routes
- `/api/relay` - WebSocket relay for command forwarding

## 🔐 Security

- CORS headers configured
- HTTPS in production
- API key authentication (production)

## 📱 Components

### Main Page (`app/page.tsx`)
- Command input
- Permission selector
- Response history
- Status indicator

### CredentialsModal (`components/CredentialsModal.tsx`)
- Tab interface for 4 platforms
- Encrypted storage
- Save/Delete functionality

### VoiceControls (`components/VoiceControls.tsx`)
- Web Speech API integration
- Microphone/speaker controls
- Portuguese language support

## 🚢 Deployment

### Vercel Deployment

```bash
# Login to Vercel
vercel login

# Deploy
vercel --prod
```

### Environment Variables

Set in Vercel Dashboard:
- `ADK_SECRET` - Message signing secret
- `NEXT_PUBLIC_API_URL` - Backend API URL (if different)

## 📊 Usage

1. **Start the interface**: `npm run dev`
2. **Open browser**: http://localhost:3000
3. **Click settings gear**: Configure credentials
4. **Enter command**: Type or use voice
5. **Select permission**: Choose appropriate level
6. **Send**: Click Send or press Enter

## 🎤 Voice Commands

1. Click microphone button
2. Grant browser permissions
3. Speak command in Portuguese
4. Command appears in input field

## 🔗 API Integration

The frontend connects to `/api/relay` which forwards commands to the local ADK instance.

### Request Format
```json
{
  "command": "comprar BTC 0.01",
  "permission": "trade_execution",
  "params": {}
}
```

### Response Format
```json
{
  "type": "response",
  "timestamp": "2026-02-11T11:45:00Z",
  "status": "success",
  "result": "Order executed",
  "error": null
}
```

## 🧪 Testing

### Unit Tests
```bash
npm test
```

### E2E Tests
```bash
npm run test:e2e
```

## 📈 Performance

- **Build time**: ~30s
- **Page load**: <1s
- **Bundle size**: Optimized with Next.js
- **Lighthouse score**: 95+

---

**Built with ❤️ for professional trading**
