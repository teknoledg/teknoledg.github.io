#!/usr/bin/env python3
"""
Share Certificate Verification API
Handles certificate validation and QR code generation
"""

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import qrcode
import io
import base64
from datetime import datetime
import os
import logging
from encryption_utils import encrypt_certificate_for_qr, decrypt_qr_certificate, verify_qr_certificate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Database configuration
DB_PATH = 'certificates.db'

def init_certificate_database():
    """Initialize the certificate database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS certificates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            certificate_number TEXT NOT NULL UNIQUE,
            certificate_name TEXT NOT NULL,
            number_of_shares INTEGER NOT NULL,
            owner_name TEXT NOT NULL,
            certificate_type TEXT NOT NULL,
            par_value TEXT NOT NULL,
            issue_date DATE NOT NULL,
            status TEXT DEFAULT 'valid',
            authorized_shares INTEGER NOT NULL,
            issued_shares INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert sample certificate
    cursor.execute('''
        INSERT OR IGNORE INTO certificates 
        (certificate_number, certificate_name, number_of_shares, owner_name, 
         certificate_type, par_value, issue_date, authorized_shares, issued_shares)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        '000001',
        'Teknoledge Holdings Share Certificate',
        1000000,
        'Tim McGuckin',
        'Common Stock',
        '$0.001',
        '2024-01-01',
        10000000,
        1000000
    ))
    
    conn.commit()
    conn.close()
    logger.info("Certificate database initialized")

def generate_qr_code(certificate_number, certificate_data=None):
    """Generate encrypted QR code for certificate"""
    if certificate_data is None:
        # Get certificate data from database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT certificate_number, certificate_name, number_of_shares, 
                   owner_name, certificate_type, par_value, issue_date, 
                   status, authorized_shares, issued_shares
            FROM certificates 
            WHERE certificate_number = ?
        """, (certificate_number,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise Exception("Certificate not found")
        
        certificate_data = {
            'certificate_number': result[0],
            'certificate_name': result[1],
            'number_of_shares': result[2],
            'owner_name': result[3],
            'certificate_type': result[4],
            'par_value': result[5],
            'issue_date': result[6],
            'status': result[7],
            'authorized_shares': result[8],
            'issued_shares': result[9]
        }
    
    # Generate encrypted QR data
    encrypted_qr_data = encrypt_certificate_for_qr(certificate_data)
    
    # Create QR code with encrypted data
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # Medium error correction for encrypted data
        box_size=10,
        border=4,
    )
    qr.add_data(encrypted_qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    return base64.b64encode(buffer.getvalue()).decode()

@app.route('/')
def serve_verify():
    """Serve the verification page"""
    return send_from_directory('..', 'verify.html')

@app.route('/css/<path:filename>')
def serve_css(filename):
    """Serve CSS files"""
    return send_from_directory('../css', filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    """Serve JavaScript files"""
    return send_from_directory('../js', filename)

@app.route('/images/<path:filename>')
def serve_images(filename):
    """Serve image files"""
    return send_from_directory('../images', filename)

@app.route('/api/verify-certificate', methods=['POST'])
def verify_certificate():
    """Verify a share certificate"""
    try:
        data = request.get_json()
        certificate_number = data.get('certificate_number', '').strip()
        
        if not certificate_number:
            return jsonify({
                'success': False,
                'message': 'Certificate number is required'
            }), 400
        
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Query certificate
        cursor.execute("""
            SELECT certificate_number, certificate_name, number_of_shares, 
                   owner_name, certificate_type, par_value, issue_date, 
                   status, authorized_shares, issued_shares
            FROM certificates 
            WHERE certificate_number = ?
        """, (certificate_number,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            certificate = {
                'certificate_number': result[0],
                'certificate_name': result[1],
                'number_of_shares': result[2],
                'owner_name': result[3],
                'certificate_type': result[4],
                'par_value': result[5],
                'issue_date': result[6],
                'status': result[7],
                'authorized_shares': result[8],
                'issued_shares': result[9]
            }
            
            return jsonify({
                'success': True,
                'certificate': certificate,
                'message': 'Certificate verified successfully'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Certificate not found',
                'certificate_number': certificate_number
            }), 404
            
    except Exception as e:
        logger.error(f"Certificate verification error: {e}")
        return jsonify({
            'success': False,
            'message': 'An error occurred during verification'
        }), 500

@app.route('/api/verify-encrypted-qr', methods=['POST'])
def verify_encrypted_qr():
    """Verify an encrypted QR code"""
    try:
        data = request.get_json()
        qr_data = data.get('qr_data', '').strip()
        
        if not qr_data:
            return jsonify({
                'success': False,
                'message': 'QR code data is required'
            }), 400
        
        # Decrypt and verify QR code
        is_valid, certificate_data = verify_qr_certificate(qr_data, '')
        
        if is_valid and certificate_data:
            return jsonify({
                'success': True,
                'certificate': certificate_data,
                'message': 'Encrypted certificate verified successfully',
                'encrypted': True
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Invalid or corrupted QR code',
                'encrypted': True
            }), 400
            
    except Exception as e:
        logger.error(f"Encrypted QR verification error: {e}")
        return jsonify({
            'success': False,
            'message': 'Error verifying encrypted QR code'
        }), 500

@app.route('/api/generate-qr/<certificate_number>')
def generate_qr(certificate_number):
    """Generate QR code for certificate"""
    try:
        # Verify certificate exists
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT certificate_number FROM certificates WHERE certificate_number = ?", (certificate_number,))
        
        if not cursor.fetchone():
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Certificate not found'
            }), 404
        
        conn.close()
        
        # Generate QR code
        qr_code = generate_qr_code(certificate_number)
        
        return jsonify({
            'success': True,
            'qr_code': qr_code,
            'certificate_number': certificate_number
        })
        
    except Exception as e:
        logger.error(f"QR code generation error: {e}")
        return jsonify({
            'success': False,
            'message': 'Error generating QR code'
        }), 500

@app.route('/api/certificates')
def list_certificates():
    """List all certificates"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT certificate_number, certificate_name, number_of_shares, 
                   owner_name, status, issue_date
            FROM certificates 
            ORDER BY certificate_number
        """)
        
        certificates = []
        for row in cursor.fetchall():
            certificates.append({
                'certificate_number': row[0],
                'certificate_name': row[1],
                'number_of_shares': row[2],
                'owner_name': row[3],
                'status': row[4],
                'issue_date': row[5]
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'certificates': certificates,
            'total': len(certificates)
        })
        
    except Exception as e:
        logger.error(f"List certificates error: {e}")
        return jsonify({
            'success': False,
            'message': 'Error retrieving certificates'
        }), 500

@app.route('/api/add-certificate', methods=['POST'])
def add_certificate():
    """Add a new certificate"""
    try:
        data = request.get_json()
        
        required_fields = [
            'certificate_number', 'certificate_name', 'number_of_shares',
            'owner_name', 'certificate_type', 'par_value', 'issue_date',
            'authorized_shares', 'issued_shares'
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO certificates 
            (certificate_number, certificate_name, number_of_shares, owner_name,
             certificate_type, par_value, issue_date, authorized_shares, issued_shares)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['certificate_number'],
            data['certificate_name'],
            data['number_of_shares'],
            data['owner_name'],
            data['certificate_type'],
            data['par_value'],
            data['issue_date'],
            data['authorized_shares'],
            data['issued_shares']
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Certificate added successfully'
        })
        
    except sqlite3.IntegrityError:
        return jsonify({
            'success': False,
            'message': 'Certificate number already exists'
        }), 400
    except Exception as e:
        logger.error(f"Add certificate error: {e}")
        return jsonify({
            'success': False,
            'message': 'Error adding certificate'
        }), 500

if __name__ == '__main__':
    # Initialize database
    init_certificate_database()
    
    # Run the app
    port = int(os.getenv('PORT', 5001))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Certificate Verification API on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
