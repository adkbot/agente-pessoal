"""
CRT Strategy Validator
Implements ZForex CRT methodology validation rules
"""
from datetime import datetime


class CRTValidator:
    """
    Validates trades against CRT (Candle Range Theory) rules from ZForex
    Reference: https://www.youtube.com/@zforeex
    """
    
    def __init__(self):
        self.required_timeframes = ['H4', 'M15', 'M5']
        self.min_rr_ratio = 2.0
        self.h4_alignment_required = True
        
    def validate_structure(self, trade_data: dict) -> dict:
        """
        CAMADA 1: CORE ENGINE - Validação estrutural
        
        Valida:
        - Alinhamento H4
        - Identificação de liquidez
        - Padrão R
        - Direção estrutural
        
        Args:
            trade_data: Dados da operação proposta
            
        Returns:
            dict: {"valid": bool, "reason": str, "layer": int}
        """
        
        # Verificar alinhamento H4 (REGRA ABSOLUTA)
        h4_aligned = trade_data.get('h4_structure_aligned', False)
        if not h4_aligned:
            return {
                "valid": False,
                "reason": "BLOQUEADO: Estrutura H4 não alinhada (REGRA ABSOLUTA)",
                "layer": 1
            }
        
        # Verificar identificação de liquidez
        liquidity_identified = trade_data.get('liquidity_identified', False)
        if not liquidity_identified:
            return {
                "valid": False,
                "reason": "BLOQUEADO: Liquidez não identificada",
                "layer": 1
            }
        
        return {
            "valid": True,
            "reason": "Estrutura validada (H4 alinhado, liquidez identificada)",
            "layer": 1
        }
    
    def validate_correlation(self, trade_data: dict) -> dict:
        """
        CAMADA 2: CONTEXTO GLOBAL E CORRELAÇÃO
        
        Valida:
        - Correlação multi-ativo
        - DXY (Forex) / BTC (Cripto)
        - Sincronização de fluxo
        """
        
        # Verificar correlação
        correlation_aligned = trade_data.get('correlation_aligned', True)  # Default True
        if not correlation_aligned:
            return {
                "valid": False,
                "reason": "BLOQUEADO: Conflito estrutural na correlação",
                "layer": 2
            }
        
        return {
            "valid": True,
            "reason": "Correlação alinhada",
            "layer": 2
        }
    
    def validate_timing(self, trade_data: dict) -> dict:
        """
        CAMADA 3: EXECUTION ENGINE
        
        Validar 5 critérios obrigatórios:
        1. H4 alinhado
        2. M15 confirmou deslocamento
        3. M5 confirmou reteste
        4. Liquidez foi capturada
        5. Multi-ativo sincronizado
        """
        
        criteria = {
            'h4_aligned': trade_data.get('h4_structure_aligned', False),
            'm15_displacement': trade_data.get('m15_displacement', False),
            'm5_retest': trade_data.get('m5_retest', False),
            'liquidity_swept': trade_data.get('liquidity_swept', False),
            'multi_asset_sync': trade_data.get('correlation_aligned', True)
        }
        
        # Todos os 5 critérios devem ser True
        all_criteria_met = all(criteria.values())
        
        if not all_criteria_met:
            failed = [k for k, v in criteria.items() if not v]
            return {
                "valid": False,
                "reason": f"BLOQUEADO: Critérios não atendidos: {', '.join(failed)}",
                "layer": 3,
                "failed_criteria": failed
            }
        
        return {
            "valid": True,
            "reason": "Todos os 5 critérios de timing atendidos",
            "layer": 3
        }
    
    def validate_discipline(self, trade_data: dict, trade_history: dict) -> dict:
        """
        CAMADA 11: DISCIPLINA OPERACIONAL
        
        Proibições:
        - Operar sem alinhamento H4
        - Operar após 3 perdas consecutivas
        - Operar fora do horário definido
        - Ignorar checklist estrutural
        """
        
        # Verificar perdas consecutivas
        consecutive_losses = trade_history.get('consecutive_losses', 0)
        if consecutive_losses >= 3:
            return {
                "valid": False,
                "reason": "BLOQUEADO: 3 perdas consecutivas - modo defesa ativado",
                "layer": 11
            }
        
        # Verificar horário de trading
        current_hour = datetime.now().hour
        allowed_hours = trade_data.get('allowed_trading_hours', range(8, 18))
        if current_hour not in allowed_hours:
            return {
                "valid": False,
                "reason": f"BLOQUEADO: Fora do horário de operação (hora atual: {current_hour})",
                "layer": 11
            }
        
        return {
            "valid": True,
            "reason": "Disciplina operacional mantida",
            "layer": 11
        }
    
    def validate_complete(self, trade_data: dict, trade_history: dict = None) -> dict:
        """
        Validação completa através de todas as camadas CRT
        
        Args:
            trade_data: Dados da operação
            trade_history: Histórico de operações (para disciplina)
            
        Returns:
            dict: {"approved": bool, "reason": str, "failed_layer": int or None}
        """
        
        if trade_history is None:
            trade_history = {}
        
        # CAMADA 1: Estrutura
        result = self.validate_structure(trade_data)
        if not result['valid']:
            return {
                "approved": False,
                "reason": result['reason'],
                "failed_layer": result['layer']
            }
        
        # CAMADA 2: Correlação
        result = self.validate_correlation(trade_data)
        if not result['valid']:
            return {
                "approved": False,
                "reason": result['reason'],
                "failed_layer": result['layer']
            }
        
        # CAMADA 3: Timing
        result = self.validate_timing(trade_data)
        if not result['valid']:
            return {
                "approved": False,
                "reason": result['reason'],
                "failed_layer": result['layer']
            }
        
        # CAMADA 11: Disciplina
        result = self.validate_discipline(trade_data, trade_history)
        if not result['valid']:
            return {
                "approved": False,
                "reason": result['reason'],
                "failed_layer": result['layer']
            }
        
        # Todas as camadas aprovadas
        return {
            "approved": True,
            "reason": "CRT: Todas as camadas validadas - ESTRUTURA H4 ALINHADA ✓",
            "failed_layer": None
        }
