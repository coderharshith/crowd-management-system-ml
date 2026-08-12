"""
Gate Control Module
Manages automated gate closure based on crowd density thresholds.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import threading


class GateController:
    """Manages gate states and automated control logic."""
    
    def __init__(self, config: Dict, base_dir: str):
        self.config = config
        self.base_dir = base_dir
        self.gate_log_file = os.path.join(base_dir, 'gate_events.log')
        self.gates = {}
        self.lock = threading.Lock()
        
        # Initialize gates from config
        for gate_info in config.get('gate_control', {}).get('gates', []):
            self.gates[gate_info['id']] = {
                'name': gate_info['name'],
                'status': gate_info.get('status', 'open'),
                'mode': 'auto',  # auto or manual
                'last_action': None,
                'last_action_reason': None
            }
    
    def check_auto_closure_conditions(self, total_count: int, zone_data: Dict) -> Dict[str, str]:
        """
        Check if automatic gate closure conditions are met.
        
        Args:
            total_count: Total number of people detected
            zone_data: Current zone data with counts
        
        Returns:
            Dictionary mapping gate_id to recommended action ('close', 'open', 'none')
        """
        if not self.config.get('gate_control', {}).get('enabled', False):
            return {}
        
        recommendations = {}
        auto_close_threshold = self.config['gate_control'].get('auto_close_threshold', 50)
        auto_open_threshold = self.config['gate_control'].get('auto_open_threshold', 30)
        
        for gate_id, gate_info in self.gates.items():
            # Skip if in manual mode
            if gate_info['mode'] == 'manual':
                recommendations[gate_id] = 'none'
                continue
            
            current_status = gate_info['status']
            
            # Determine action based on thresholds
            if total_count >= auto_close_threshold and current_status == 'open':
                recommendations[gate_id] = 'close'
            elif total_count <= auto_open_threshold and current_status == 'closed':
                recommendations[gate_id] = 'open'
            else:
                recommendations[gate_id] = 'none'
        
        return recommendations
    
    def execute_gate_action(self, gate_id: str, action: str, reason: str = 'auto') -> bool:
        """
        Execute a gate action (open/close).
        
        Args:
            gate_id: Gate identifier
            action: 'open' or 'close'
            reason: Reason for action (auto, manual, emergency)
        
        Returns:
            True if successful, False otherwise
        """
        with self.lock:
            if gate_id not in self.gates:
                return False
            
            gate = self.gates[gate_id]
            
            # Check manual override
            if gate['mode'] == 'manual' and reason == 'auto':
                return False
            
            # Update gate status
            old_status = gate['status']
            gate['status'] = 'closed' if action == 'close' else 'open'
            gate['last_action'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            gate['last_action_reason'] = reason
            
            # Log the event
            self.log_gate_event(gate_id, action, reason, old_status)
            
            # In a real implementation, this would send a command to hardware
            # For now, we just update the state
            print(f"🚪 Gate {gate_id} ({gate['name']}): {old_status} -> {gate['status']} (reason: {reason})")
            
            return True
    
    def set_gate_mode(self, gate_id: str, mode: str) -> bool:
        """
        Set gate control mode (auto or manual).
        
        Args:
            gate_id: Gate identifier
            mode: 'auto' or 'manual'
        
        Returns:
            True if successful
        """
        with self.lock:
            if gate_id not in self.gates:
                return False
            
            self.gates[gate_id]['mode'] = mode
            self.log_gate_event(gate_id, f'mode_change_{mode}', 'user', self.gates[gate_id]['status'])
            return True
    
    def get_gate_status(self, gate_id: Optional[str] = None) -> Dict:
        """
        Get status of one or all gates.
        
        Args:
            gate_id: Specific gate ID, or None for all gates
        
        Returns:
            Gate status dictionary
        """
        with self.lock:
            if gate_id:
                return self.gates.get(gate_id, {})
            else:
                return dict(self.gates)
    
    def log_gate_event(self, gate_id: str, action: str, reason: str, previous_status: str):
        """Log gate event to file."""
        try:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            gate_name = self.gates[gate_id]['name']
            log_entry = f"[{timestamp}] Gate: {gate_name} ({gate_id}) | Action: {action} | Reason: {reason} | Previous: {previous_status}\n"
            
            with open(self.gate_log_file, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error logging gate event: {e}")
    
    def get_recent_events(self, limit: int = 10) -> List[str]:
        """Get recent gate events from log."""
        try:
            if not os.path.exists(self.gate_log_file):
                return []
            
            with open(self.gate_log_file, 'r') as f:
                lines = f.readlines()
            
            return lines[-limit:][::-1]  # Return last N lines, reversed
        except Exception:
            return []
    
    def emergency_close_all(self) -> Dict[str, bool]:
        """Emergency close all gates regardless of mode."""
        results = {}
        for gate_id in self.gates.keys():
            results[gate_id] = self.execute_gate_action(gate_id, 'close', 'emergency')
        return results
    
    def open_all(self) -> Dict[str, bool]:
        """Open all gates (manual override)."""
        results = {}
        for gate_id in self.gates.keys():
            results[gate_id] = self.execute_gate_action(gate_id, 'open', 'manual')
        return results


def send_gate_command(gate_id: str, command: str) -> bool:
    """
    Interface for sending commands to physical gate hardware.
    This is a placeholder - implement actual hardware communication here.
    
    Args:
        gate_id: Gate identifier
        command: Command to send ('open', 'close', 'stop')
    
    Returns:
        True if command sent successfully
    """
    # TODO: Implement actual hardware communication
    # Examples:
    # - Serial communication to relay board
    # - HTTP request to IoT device
    # - MQTT message to gate controller
    # - GPIO control on Raspberry Pi
    
    print(f"[HARDWARE INTERFACE] Sending command '{command}' to gate {gate_id}")
    
    # Placeholder implementation
    return True
