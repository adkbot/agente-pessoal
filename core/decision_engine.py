"""
Decision Engine - Institutional Trading Logic
Validates trade setups based on multi-timeframe structure and market context
Integrated with CRT (Candle Range Theory) methodology from ZForex
"""
from strategy.crt_validator import CRTValidator


class DecisionEngine:
    """
    Validates commands against institutional trading rules:
    - CRT methodology (ZForex)
    - H4 structure alignment
    - Multi-timeframe confirmation
    - Session validation
    - Risk/Reward ratios
    """
    
    def __init__(self, config):
        self.config = config['decision']
        self.require_h4 = self.config['require_h4_structure']
        self.require_mtf = self.config['require_mtf_confirmation']
        self.min_rr = self.config['min_rr_ratio']
        self.allowed_sessions = self.config['allowed_sessions']
        
        # Initialize CRT Validator
        self.crt_validator = CRTValidator()
        print("✅ CRT Validator initialized - ZForex methodology active")

    
    def validate(self, command: dict) -> dict:
        """
        Validate command against decision rules
        
        Args:
            command: Structured command dict
            
        Returns:
            dict: {"approved": bool, "reason": str}
        """
        action = command.get("action")
        
        # Allow non-trading actions
        if action in ["change_timeframe", "draw_trendline", "apply_fib", "open_trade_panel"]:
            return {
                "approved": True,
                "reason": "Non-trading action approved"
            }
        
        # Trading actions require validation
        if action in ["execute_market_order", "execute_limit_order", "execute_stop_order"]:
            return self._validate_trade(command)
        
        # Default approve for other actions
        return {
            "approved": True,
            "reason": "Action approved"
        }
    
    def _validate_trade(self, command: dict) -> dict:
        """
        Validate trading command against institutional rules and CRT methodology
        
        Applies ZForex CRT validation through multiple layers:
        - Layer 1: Core Engine (H4 structure)
        - Layer 2: Correlation
        - Layer 3: Timing (5 criteria)
        - Layer 11: Discipline
        """
        
        # Prepare trade data for CRT validation
        trade_data = {
            'h4_structure_aligned': command.get('h4_structure_aligned', False),
            'm15_displacement': command.get('m15_displacement', False),
            'm5_retest': command.get('m5_retest', False),
            'liquidity_swept': command.get('liquidity_swept', False),
            'liquidity_identified': command.get('liquidity_identified', False),
            'correlation_aligned': command.get('correlation_aligned', True),
            'allowed_trading_hours': range(8, 18)  # London/NY sessions
        }
        
        # Get trade history for discipline check
        trade_history = {
            'consecutive_losses': command.get('consecutive_losses', 0)
        }
        
        # Run complete CRT validation
        crt_result = self.crt_validator.validate_complete(trade_data, trade_history)
        
        if not crt_result['approved']:
            return {
                "approved": False,
                "reason": f"CRT Layer {crt_result['failed_layer']}: {crt_result['reason']}"
            }
        
        # Check if RR ratio is provided and meets minimum
        rr_ratio = command.get("rr_ratio", 0)
        if rr_ratio < self.min_rr:
            return {
                "approved": False,
                "reason": f"RR ratio {rr_ratio} below minimum {self.min_rr} (CRT requires >= 2.0)"
            }
        
        # Check session (if provided)
        session = command.get("session", "").lower()
        if session and session not in self.allowed_sessions:
            return {
                "approved": False,
                "reason": f"Session {session} not in allowed sessions (CRT: London/NY preferred)"
            }
        
        return {
            "approved": True,
            "reason": crt_result['reason']
        }
