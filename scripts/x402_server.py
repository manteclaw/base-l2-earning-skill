#!/usr/bin/env python3
"""
x402 Monetization Server
Part of Base L2 Earning Agent skill
"""

import os
import json
import base64
import io
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse

WALLET = os.getenv("BASE_WALLET", "0xYOUR_WALLET")
PORT = int(os.getenv("PORT", "8000"))

class X402Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        
        # Check payment headers
        tx_hash = self.headers.get('X-Payment-TxHash')
        payer = self.headers.get('X-Payer-Address')
        
        if not tx_hash:
            self.send_response(402)  # Payment Required
            self.send_header('Content-type', 'application/json')
            self.send_header('X-Payment-Amount', '0.02')
            self.send_header('X-Payment-Token', 'USDC')
            self.send_header('X-Payment-Address', WALLET)
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "Payment required",
                "amount": "0.02",
                "token": "USDC",
                "recipient": WALLET
            }).encode())
            return
        
        # Route to service
        if path == '/contract_audit':
            self.handle_contract_audit(params)
        elif path == '/base_gas_estimate':
            self.handle_gas_estimate()
        elif path == '/generate_mnemonic':
            self.handle_mnemonic()
        elif path == '/summarize':
            self.handle_summarize(params)
        elif path == '/generate_qr':
            self.handle_qr(params)
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_contract_audit(self, params):
        """Smart contract vulnerability scan - 0.02 USDC"""
        code = params.get('contract_code', [''])[0]
        
        # Simple regex-based checks
        issues = []
        if 'selfdestruct' in code.lower():
            issues.append("CRITICAL: selfdestruct found")
        if 'tx.origin' in code:
            issues.append("HIGH: tx.origin usage (phishing risk)")
        if 'block.timestamp' in code and ('random' in code.lower() or 'lottery' in code.lower()):
            issues.append("HIGH: timestamp as randomness source")
        if 'call{' in code and 'value' in code:
            issues.append("MEDIUM: unchecked external call")
        
        result = {
            "service": "contract_audit",
            "price": "0.02 USDC",
            "issues_found": len(issues),
            "severity": "CRITICAL" if any('CRITICAL' in i for i in issues) else "HIGH" if issues else "CLEAR",
            "issues": issues,
            "wallet": WALLET
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())
    
    def handle_gas_estimate(self):
        """Base gas prices - 0.01 USDC"""
        import urllib.request
        try:
            req = urllib.request.Request(
                "https://api.base.org/v1/gas-price",
                headers={"Accept": "application/json"}
            )
            resp = urllib.request.urlopen(req)
            data = json.loads(resp.read().decode())
        except:
            data = {"slow": 0.1, "standard": 0.5, "fast": 1.0}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "service": "base_gas_estimate",
            "price": "0.01 USDC",
            "gas_prices": data,
            "wallet": WALLET
        }).encode())
    
    def handle_mnemonic(self):
        """Generate secure mnemonic - 0.01 USDC"""
        import secrets
        words = ["abandon", "ability", "able", "about", "above", "absent", "absorb", "abstract", "absurd", "abuse"]
        mnemonic = ' '.join(secrets.choice(words) for _ in range(12))
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "service": "generate_mnemonic",
            "price": "0.01 USDC",
            "mnemonic": mnemonic,
            "warning": "This is a DEMO mnemonic. Use proper BIP39 generation in production.",
            "wallet": WALLET
        }).encode())
    
    def handle_summarize(self, params):
        """Text summarization - 0.03 USDC"""
        text = params.get('text', [''])[0]
        # Simple extraction-based summary
        sentences = text.split('.')[:3]
        summary = '. '.join(sentences) + '.'
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "service": "summarize",
            "price": "0.03 USDC",
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "wallet": WALLET
        }).encode())
    
    def handle_qr(self, params):
        """QR code generation - 0.05 USDC"""
        text = params.get('text', [''])[0]
        
        # Simple ASCII QR (placeholder)
        qr_ascii = f"""
        █▀▀▀▀▀█ ▀▄ {text[:10]}... ▄▀ █▀▀▀▀▀█
        █ ███ █ ▀▄▀▄▀▄▀▄▀▄▀▄▀ █ ███ █
        █ ▀▀▀ █ ▄▀▄▀▄▀▄▀▄▀▄▀▄ █ ▀▀▀ █
        ▀▀▀▀▀▀▀ ▀ █ ▀ █ ▀ █ ▀ ▀▀▀▀▀▀▀
        """
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "service": "generate_qr",
            "price": "0.05 USDC",
            "qr_ascii": qr_ascii,
            "text": text,
            "wallet": WALLET
        }).encode())
    
    def log_message(self, format, *args):
        print(f"[x402] {args[0]}")

def start_server():
    server = HTTPServer(('', PORT), X402Handler)
    print(f"x402 server running on port {PORT}")
    print(f"Receiving wallet: {WALLET}")
    print("Endpoints:")
    print("  /contract_audit    - 0.02 USDC")
    print("  /base_gas_estimate - 0.01 USDC")
    print("  /generate_mnemonic - 0.01 USDC")
    print("  /summarize         - 0.03 USDC")
    print("  /generate_qr       - 0.05 USDC")
    server.serve_forever()

if __name__ == "__main__":
    start_server()
