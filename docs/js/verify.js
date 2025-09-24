// Share Certificate Verification System
// Handles QR code scanning and certificate validation

class CertificateVerifier {
    constructor() {
        this.scanner = null;
        this.isScanning = false;
        this.certificates = {
            '000001': {
                number: '000001',
                name: 'Teknoledge Holdings Share Certificate',
                shares: 1000000,
                issueDate: '2024-01-01',
                status: 'valid',
                owner: 'Tim McGuckin',
                certificateType: 'Common Stock',
                parValue: '$0.001',
                authorizedShares: 10000000,
                issuedShares: 1000000
            }
        };
        
        this.init();
    }
    
    init() {
        this.setupEventListeners();
        this.setupQRScanner();
    }
    
    setupEventListeners() {
        // Manual certificate entry
        document.getElementById('verifyCertificate').addEventListener('click', () => {
            const certNumber = document.getElementById('certificateNumber').value.trim();
            if (certNumber) {
                this.verifyCertificate(certNumber);
            } else {
                alert('Please enter a certificate number');
            }
        });
        
        // QR Scanner controls
        document.getElementById('startScanner').addEventListener('click', () => {
            this.startQRScanner();
        });
        
        document.getElementById('stopScanner').addEventListener('click', () => {
            this.stopQRScanner();
        });
        
        // Enter key for manual entry
        document.getElementById('certificateNumber').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                document.getElementById('verifyCertificate').click();
            }
        });
    }
    
    setupQRScanner() {
        // QR Scanner will be initialized when needed
    }
    
    startQRScanner() {
        if (this.isScanning) return;
        
        this.isScanning = true;
        document.getElementById('startScanner').style.display = 'none';
        document.getElementById('stopScanner').style.display = 'inline-block';
        
        // Create scanner overlay
        const overlay = document.createElement('div');
        overlay.className = 'scanner-overlay';
        overlay.innerHTML = `
            <div class="scanner-content">
                <button class="scanner-close" onclick="this.parentElement.parentElement.remove()">×</button>
                <h3>📱 Scan QR Code</h3>
                <p>Point your camera at the QR code on the share certificate</p>
                <div id="qr-reader-overlay"></div>
            </div>
        `;
        
        document.body.appendChild(overlay);
        
        // Initialize QR Scanner
        this.scanner = new QrScanner(
            document.getElementById('qr-reader-overlay'),
            (result) => {
                this.handleQRResult(result);
            },
            {
                highlightScanRegion: true,
                highlightCodeOutline: true,
                preferredCamera: 'environment'
            }
        );
        
        this.scanner.start().catch(err => {
            console.error('QR Scanner error:', err);
            alert('Camera access denied. Please allow camera access to scan QR codes.');
            this.stopQRScanner();
        });
    }
    
    stopQRScanner() {
        if (this.scanner) {
            this.scanner.stop();
            this.scanner.destroy();
            this.scanner = null;
        }
        
        this.isScanning = false;
        document.getElementById('startScanner').style.display = 'inline-block';
        document.getElementById('stopScanner').style.display = 'none';
        
        // Remove scanner overlay
        const overlay = document.querySelector('.scanner-overlay');
        if (overlay) {
            overlay.remove();
        }
    }
    
    handleQRResult(result) {
        console.log('QR Code scanned:', result);
        
        // Extract certificate number from QR code
        const certNumber = this.extractCertificateNumber(result);
        if (certNumber) {
            this.verifyCertificate(certNumber);
            this.stopQRScanner();
        } else {
            alert('Invalid QR code. Please scan a valid share certificate QR code.');
        }
    }
    
    extractCertificateNumber(qrResult) {
        // Check for encrypted QR code first
        if (qrResult.startsWith('SEC_CERT:')) {
            return qrResult; // Return full encrypted data
        }
        
        // Check for regular certificate number
        // Format: "CERT:000001" or just "000001"
        const match = qrResult.match(/CERT:(\d+)|(\d{6})/);
        if (match) {
            return match[1] || match[2];
        }
        return null;
    }
    
    async verifyCertificate(certNumber) {
        console.log('Verifying certificate:', certNumber);
        
        // Show loading state
        const verifyBtn = document.getElementById('verifyCertificate');
        const originalText = verifyBtn.textContent;
        verifyBtn.innerHTML = '<span class="loading"></span> Verifying...';
        verifyBtn.disabled = true;
        
        try {
            let response;
            
            // Check if it's an encrypted QR code
            if (certNumber.startsWith('SEC_CERT:')) {
                response = await fetch('/api/verify-encrypted-qr', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        qr_data: certNumber
                    })
                });
            } else {
                // Regular certificate number verification
                response = await fetch('/api/verify-certificate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        certificate_number: certNumber
                    })
                });
            }
            
            const result = await response.json();
            
            if (result.success) {
                this.displayResults(result.certificate, result.encrypted || false);
            } else {
                this.displayError(result.message);
            }
            
        } catch (error) {
            console.error('Verification error:', error);
            this.displayError('Network error. Please try again.');
        } finally {
            verifyBtn.textContent = originalText;
            verifyBtn.disabled = false;
        }
    }
    
    displayResults(certificate, isEncrypted = false) {
        const resultsDiv = document.getElementById('verificationResults');
        const certInfoDiv = document.getElementById('certificateInfo');
        
        if (certificate) {
            const encryptionBadge = isEncrypted ? '<span style="color: #00ff00; font-weight: bold;">🔒 ENCRYPTED</span>' : '';
            
            certInfoDiv.innerHTML = `
                <div class="certificate-info certificate-valid">
                    <h4 class="status-valid">Certificate Valid ${encryptionBadge}</h4>
                    <p><strong>Certificate Number:</strong> ${certificate.certificate_number}</p>
                    <p><strong>Certificate Name:</strong> ${certificate.certificate_name}</p>
                    <p><strong>Number of Shares:</strong> ${certificate.number_of_shares.toLocaleString()}</p>
                    <p><strong>Owner:</strong> ${certificate.owner_name}</p>
                    <p><strong>Certificate Type:</strong> ${certificate.certificate_type}</p>
                    <p><strong>Par Value:</strong> ${certificate.par_value}</p>
                    <p><strong>Issue Date:</strong> ${certificate.issue_date}</p>
                    <p><strong>Status:</strong> ${certificate.status.toUpperCase()}</p>
                    <p><strong>Authorized Shares:</strong> ${certificate.authorized_shares.toLocaleString()}</p>
                    <p><strong>Issued Shares:</strong> ${certificate.issued_shares.toLocaleString()}</p>
                    ${isEncrypted ? '<p><strong>Security:</strong> 🔒 Encrypted QR Code - Maximum Security</p>' : ''}
                </div>
            `;
        } else {
            certInfoDiv.innerHTML = `
                <div class="certificate-info certificate-invalid">
                    <h4 class="status-invalid">Certificate Not Found</h4>
                    <p><strong>Status:</strong> INVALID</p>
                    <p>This certificate does not exist in our database.</p>
                    <p>Please verify the certificate and try again.</p>
                </div>
            `;
        }
        
        resultsDiv.style.display = 'block';
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    displayError(message) {
        const resultsDiv = document.getElementById('verificationResults');
        const certInfoDiv = document.getElementById('certificateInfo');
        
        certInfoDiv.innerHTML = `
            <div class="certificate-info certificate-invalid">
                <h4 class="status-invalid">Verification Error</h4>
                <p><strong>Error:</strong> ${message}</p>
                <p>Please try again or contact support if the problem persists.</p>
            </div>
        `;
        
        resultsDiv.style.display = 'block';
        resultsDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Generate QR code for a certificate (for testing)
    generateQRCode(certNumber) {
        const qrContainer = document.createElement('div');
        qrContainer.className = 'qr-code-display';
        qrContainer.innerHTML = `<h4>QR Code for Certificate ${certNumber}</h4>`;
        
        QRCode.toCanvas(qrContainer, `CERT:${certNumber}`, {
            width: 200,
            height: 200,
            color: {
                dark: '#000000',
                light: '#FFFFFF'
            }
        }, (error) => {
            if (error) console.error('QR Code generation error:', error);
        });
        
        return qrContainer;
    }
}

// Initialize the certificate verifier when page loads
document.addEventListener('DOMContentLoaded', () => {
    new CertificateVerifier();
});

// Handle page visibility changes to stop scanner when page is hidden
document.addEventListener('visibilitychange', () => {
    if (document.hidden && window.certificateVerifier) {
        window.certificateVerifier.stopQRScanner();
    }
});

// Export for global access
window.CertificateVerifier = CertificateVerifier;
