# HackFusion

⚠️ **IMPORTANT: This tool is designed to run ONLY on Kali Linux** ⚠️

HackFusion is an advanced cybersecurity toolkit that integrates native Kali Linux security tools with an AI assistant for enhanced penetration testing and security assessments.

## Requirements

- Kali Linux (Latest Version)
- Python 3.8+
- OpenAI API Key

The following Kali Linux tools must be installed:
- nmap
- whois
- dnsenum
- nikto
- dirb
- sqlmap
- wpscan
- skipfish
- xsser
- sslyze
- cmsmap
- cmseek
- aircrack-ng suite

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/HackFusion.git
cd HackFusion
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

## Usage

Run HackFusion:
```bash
python3 src/main.py
```

## Features

1. **AI Assistant**
   - Natural language interface
   - Automated tool selection
   - Smart parameter optimization
   - Detailed report generation

2. **Information Gathering**
   - Network scanning (nmap)
   - WHOIS lookup
   - DNS enumeration
   - Service detection

3. **Vulnerability Analysis**
   - Automated vulnerability scanning
   - Service-specific checks
   - Risk assessment
   - Remediation suggestions

4. **Web Application Analysis**
   - Web server scanning (nikto)
   - Directory enumeration (dirb)
   - SQL injection testing (sqlmap)
   - WordPress scanning (wpscan)
   - General crawling (skipfish)
   - XSS detection (xsser)
   - SSL/TLS analysis (sslyze)
   - CMS detection (cmsmap, cmseek)

5. **Wireless Network Analysis**
   - Network discovery
   - WEP/WPA analysis
   - Client detection
   - Packet capture
   - Deauthentication testing

## Security Notice

This tool is for educational and authorized security testing only. Always:
1. Obtain proper authorization before testing
2. Follow responsible disclosure practices
3. Comply with local laws and regulations
4. Document all testing activities
5. Respect privacy and data protection

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
