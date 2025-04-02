"""Information gathering tools integration"""

import subprocess
import json
from typing import Dict, Any
import nmap
import whois

class InformationGathering:
    """Information gathering tools"""
    
    def __init__(self):
        """Initialize information gathering tools"""
        self.nmap = nmap.PortScanner()
        
    def run_nmap_scan(self, target: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run Nmap scan using native Kali Linux nmap"""
        try:
            # Default scan parameters
            scan_params = {
                'aggressive': '-A',  # Aggressive scan
                'version': '-sV',    # Version detection
                'os': '-O',         # OS detection
                'timing': '-T4',     # Timing template (0-5)
                'ports': '-p-'      # All ports
            }
            
            # Update with custom parameters if provided
            if params:
                scan_params.update(params)
                
            # Build nmap command
            cmd = ['nmap']
            for param in scan_params.values():
                cmd.extend(param.split())
            cmd.append(target)
            
            # Run nmap scan
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {'error': f'Nmap scan failed: {result.stderr}'}
                
            return {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            return {'error': f'Error running Nmap scan: {str(e)}'}
            
    def run_whois_lookup(self, domain: str) -> Dict[str, Any]:
        """Run WHOIS lookup using native Kali Linux whois"""
        try:
            # Run whois command
            result = subprocess.run(['whois', domain], capture_output=True, text=True)
            
            if result.returncode != 0:
                return {'error': f'WHOIS lookup failed: {result.stderr}'}
                
            return {
                'output': result.stdout,
                'command': f'whois {domain}'
            }
            
        except Exception as e:
            return {'error': f'Error running WHOIS lookup: {str(e)}'}
            
    def run_dns_enum(self, domain: str) -> Dict[str, Any]:
        """Run DNS enumeration using dnsenum"""
        try:
            # Run dnsenum command
            cmd = ['dnsenum', '--noreverse', '--nocolor', domain]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {'error': f'DNS enumeration failed: {result.stderr}'}
                
            return {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            return {'error': f'Error running DNS enumeration: {str(e)}'}
            
    def run_nikto_scan(self, target: str) -> Dict[str, Any]:
        """Run Nikto web server scanner"""
        try:
            # Run nikto command
            cmd = ['nikto', '-h', target, '-Format', 'json']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                return {'error': f'Nikto scan failed: {result.stderr}'}
                
            try:
                output = json.loads(result.stdout)
            except json.JSONDecodeError:
                output = result.stdout
                
            return {
                'output': output,
                'command': ' '.join(cmd)
            }
            
        except Exception as e:
            return {'error': f'Error running Nikto scan: {str(e)}'}
