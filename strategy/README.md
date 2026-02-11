# 📚 BIBLIOTECA DE CONHECIMENTO CRT - ZFOREX

Esta pasta contém as **regras institucionais** que governam o sistema de trading.

## 📄 Documentos

### 1. `crt_institutional_rules.md`
**Manual institucional completo** com 11 camadas operacionais baseadas na metodologia ZForex.

**Conteúdo:**
- Identidade do sistema (mesa proprietária)
- 11 camadas de validação
- Regras absolutas de operação
- Hierarquia de decisão

**Uso:** Consulta obrigatória em caso de dúvida sobre comportamento do sistema

---

### 2. `crt_strategy.md`
**Guia detalhado da estratégia CRT** com critérios específicos de entrada e saída.

**Conteúdo:**
- Regras de entrada (5 critérios obrigatórios)
- Gestão de risco
- Estrutura multi-timeframe
- Métricas de performance

**Uso:** Referência para configuração de parâmetros e backtesting

---

### 3. `crt_validator.py`
**Módulo de validação** que implementa as regras CRT no código.

**Funções principais:**
- `validate_structure()` - Camada 1: Estrutura H4
- `validate_correlation()` - Camada 2: Correlação multi-ativo
- `validate_timing()` - Camada 3: 5 critérios de execução
- `validate_discipline()` - Camada 11: Disciplina operacional
- `validate_complete()` - Validação completa através de todas as camadas

**Uso:** Integrado ao `DecisionEngine` para validação automática

---

## 🔗 Integração no Sistema

```python
# No DecisionEngine (core/decision_engine.py)
from strategy.crt_validator import CRTValidator

self.crt_validator = CRTValidator()
```

O validador CRT é **automaticamente consultado** em toda operação de trading para garantir conformidade com a metodologia ZForex.

---

## 📺 Fonte de Conhecimento

**Canal ZForex**: https://www.youtube.com/@zforeex

**Regra de ouro:**
> 💡 Em caso de dúvida sobre CRT, **SEMPRE** consultar os vídeos do canal ZForex e analisar até ter plena certeza.

---

## ⚠️ Regras Absolutas

1. **NUNCA** operar contra estrutura H4
2. **TODOS** os 5 critérios de timing devem estar atendidos
3. **RR mínimo** de 2.0
4. **Parar** após 3 perdas consecutivas
5. **Preservar capital** acima de tudo

---

## 🎯 Hierarquia de Decisão

```
1. ESTRUTURA H4 ← Prioridade máxima
2. CORRELAÇÃO MULTI-ATIVO
3. CONFIRMAÇÃO M15/M5
4. CAPTURA DE LIQUIDEZ
5. GESTÃO DE RISCO
```

Se **QUALQUER** critério falhar → **NÃO OPERAR**
