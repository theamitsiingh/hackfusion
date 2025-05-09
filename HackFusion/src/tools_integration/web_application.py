"""
Web application analysis tools integration
"""

import subprocess
import json
from typing import Dict, Any
import os
from src.utils.tool_decorators import tool_loading_animation

class WebApplicationAnalysis:
    """Web application analysis tools"""
    
    def __init__(self):
        """Initialize web application analysis tools"""
        self.required_tools = [
            # Web Vulnerability Scanners
            'nikto', 'w3af', 'zaproxy', 'burpsuite',
            
            # Injection Tools
            'sqlmap', 'xsstrike', 'xsser',
            
            # Brute Force Tools
            'dirb', 'gobuster',
            
            # CMS Scanners
            'wpscan', 'cmsmap', 'cmseek',
            
            # SSL/TLS Scanners
            'sslyze',
            
            # Additional Web Tools
            'skipfish', 'fierce', 'whatweb', 'wafw00f'
        ]
        self._check_required_tools()
    
    def _check_required_tools(self):
        """Check required web application tools"""
        missing_tools = []
        
        for tool in self.required_tools:
            try:
                result = subprocess.run(['which', tool], capture_output=True, text=True)
                if result.returncode != 0:
                    missing_tools.append(tool)
            except Exception:
                missing_tools.append(tool)
        
        if missing_tools:
            print(f"[yellow]Missing web application tools: {', '.join(missing_tools)}[/yellow]")
            print("[yellow]Some web application analysis features may be limited.[/yellow]")
            print("[yellow]Run the tool installer from the main menu to install missing tools.[/yellow]")
            
    @tool_loading_animation
    def run_scan(self, target: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """Run web application security scan"""
        results = {}
        
        # Run Nikto scan
        try:
            cmd = ['nikto', '-h', target, '-Format', 'json']
            if params and params.get('ssl'):
                cmd.append('-ssl')
            result = subprocess.run(cmd, capture_output=True, text=True)
            results['nikto'] = {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            results['nikto'] = {'error': f'Nikto scan failed: {str(e)}'}
            
        # Run Dirb directory scan
        try:
            cmd = ['dirb', target]
            if params and params.get('wordlist'):
                cmd.append(params['wordlist'])
            result = subprocess.run(cmd, capture_output=True, text=True)
            results['dirb'] = {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            results['dirb'] = {'error': f'Dirb scan failed: {str(e)}'}
            
        # Run SQLmap
        try:
            cmd = ['sqlmap', '-u', target, '--batch', '--random-agent']
            if params and params.get('forms'):
                cmd.append('--forms')
            if params and params.get('risk'):
                cmd.extend(['--risk', str(params['risk'])])
            result = subprocess.run(cmd, capture_output=True, text=True)
            results['sqlmap'] = {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            results['sqlmap'] = {'error': f'SQLmap scan failed: {str(e)}'}
            
        # Run WPScan if WordPress is detected
        if self._is_wordpress(target):
            try:
                cmd = ['wpscan', '--url', target, '--random-user-agent', '--format', 'json']
                result = subprocess.run(cmd, capture_output=True, text=True)
                results['wpscan'] = {
                    'output': result.stdout,
                    'command': ' '.join(cmd)
                }
            except Exception as e:
                results['wpscan'] = {'error': f'WPScan failed: {str(e)}'}
                
        # Run Skipfish
        try:
            output_dir = '/tmp/skipfish-output'
            os.makedirs(output_dir, exist_ok=True)
            cmd = ['skipfish', '-o', output_dir, target]
            result = subprocess.run(cmd, capture_output=True, text=True)
            results['skipfish'] = {
                'output': result.stdout,
                'command': ' '.join(cmd),
                'output_dir': output_dir
            }
        except Exception as e:
            results['skipfish'] = {'error': f'Skipfish scan failed: {str(e)}'}
            
        return results
        
    def _is_wordpress(self, target: str) -> bool:
        """Check if target is a WordPress site"""
        try:
            # Check common WordPress paths
            wp_paths = ['/wp-login.php', '/wp-admin', '/wp-content']
            cmd = ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}']
            
            for path in wp_paths:
                url = target.rstrip('/') + path
                result = subprocess.run(cmd + [url], capture_output=True, text=True)
                if result.stdout.strip() in ['200', '301', '302', '403']:
                    return True
            return False
            
        except Exception:
            return False
            
    @tool_loading_animation
    def run_xss_scan(self, target: str) -> Dict[str, Any]:
        """Run XSS vulnerability scan"""
        try:
            cmd = ['xsser', '--url', target, '--auto']
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            return {'error': f'XSS scan failed: {str(e)}'}
            
    @tool_loading_animation
    def run_ssl_scan(self, target: str) -> Dict[str, Any]:
        """Run SSL/TLS vulnerability scan"""
        try:
            cmd = ['sslyze', target, '--json_out', '-']
            result = subprocess.run(cmd, capture_output=True, text=True)
            return {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            return {'error': f'SSL scan failed: {str(e)}'}
            
    @tool_loading_animation
    def run_cms_scan(self, target: str) -> Dict[str, Any]:
        """Run CMS vulnerability scan"""
        results = {}
        
        # Run CMSmap
        try:
            cmd = ['cmsmap', target]
            result = subprocess.run(cmd, capture_output=True, text=True)
            results['cmsmap'] = {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            results['cmsmap'] = {'error': f'CMSmap scan failed: {str(e)}'}
            
        # Run CMSeek
        try:
            cmd = ['cmseek', '-u', target]
            result = subprocess.run(cmd, capture_output=True, text=True)
            results['cmseek'] = {
                'output': result.stdout,
                'command': ' '.join(cmd)
            }
        except Exception as e:
            results['cmseek'] = {'error': f'CMSeek scan failed: {str(e)}'}
            
        return results
