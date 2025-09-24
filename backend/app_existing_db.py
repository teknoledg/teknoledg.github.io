#!/usr/bin/env python3
"""
Teknoledge Registration Backend - Existing Database Integration
Integrates with your existing teknoledg.com database and email system
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash, send_from_directory
from flask_cors import CORS
import mysql.connector
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import logging
import hashlib
import secrets

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Secret key for sessions
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))

# Database configuration for existing teknoledg.com database
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'teknoledg_user'),
    'password': os.getenv('DB_PASSWORD', ''),
    'database': os.getenv('DB_NAME', 'teknoledg_db'),
    'port': int(os.getenv('DB_PORT', 3306))
}

# Admin credentials
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH', hashlib.sha256('admin123'.encode()).hexdigest())

# Email configuration using your existing email system
SMTP_SERVER = os.getenv('SMTP_SERVER', 'mail.teknoledg.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
EMAIL_USER = os.getenv('EMAIL_USER', 'noreply@teknoledg.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
ADMIN_EMAIL = 'hello@thepersonaldataexchange.com'

def get_db_connection():
    """Get connection to existing database"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as e:
        logger.error(f"Database connection error: {e}")
        return None

def init_registrations_table():
    """Create registrations table in existing database if it doesn't exist"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Create registrations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS registrations (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                name VARCHAR(255),
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip_address VARCHAR(45),
                user_agent TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index for better performance
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_email ON registrations(email)
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_timestamp ON registrations(timestamp)
        ''')
        
        conn.commit()
        logger.info("Registrations table initialized successfully")
        return True
        
    except mysql.connector.Error as e:
        logger.error(f"Error creating table: {e}")
        return False
    finally:
        conn.close()

def send_notification_email(email, name, ip_address):
    """Send notification email using your existing email system"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = f"New Registration - {email}"
        
        # Email body
        body = f"""
        New user registration received:
        
        Email: {email}
        Name: {name or 'Not provided'}
        IP Address: {ip_address}
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        This is an automated notification from the Teknoledge registration system.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Notification email sent for {email}")
        return True
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
        return False

def admin_required(f):
    """Decorator to require admin authentication"""
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def serve_index():
    """Serve the main index.html file"""
    return send_from_directory('..', 'index.html')

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

@app.route('/api/register', methods=['POST'])
def register():
    """Handle registration form submission"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip().lower()
        name = data.get('name', '').strip()
        
        if not email:
            return jsonify({'success': False, 'message': 'Email is required'}), 400
        
        # Get client info
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', '')
        
        # Connect to database
        conn = get_db_connection()
        if not conn:
            return jsonify({'success': False, 'message': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        try:
            # Check if email already exists
            cursor.execute("SELECT id FROM registrations WHERE email = %s", (email,))
            if cursor.fetchone():
                return jsonify({'success': False, 'message': 'Email already registered'}), 400
            
            # Insert new registration
            cursor.execute("""
                INSERT INTO registrations (email, name, ip_address, user_agent)
                VALUES (%s, %s, %s, %s)
            """, (email, name, ip_address, user_agent))
            
            conn.commit()
            registration_id = cursor.lastrowid
            
            # Send notification email
            email_sent = send_notification_email(email, name, ip_address)
            
            logger.info(f"New registration: {email} (ID: {registration_id})")
            
            return jsonify({
                'success': True,
                'message': "Thank you for registering! We'll notify you when we launch.",
                'email_sent': email_sent
            })
            
        except mysql.connector.Error as e:
            logger.error(f"Database error: {e}")
            return jsonify({'success': False, 'message': 'Registration failed'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        logger.error(f"Registration error: {e}")
        return jsonify({'success': False, 'message': 'An error occurred'}), 500

@app.route('/api/stats')
def get_stats():
    """Get registration statistics"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        cursor = conn.cursor()
        
        # Get total registrations
        cursor.execute("SELECT COUNT(*) FROM registrations")
        total = cursor.fetchone()[0]
        
        # Get recent registrations (last 24 hours)
        cursor.execute("""
            SELECT COUNT(*) FROM registrations 
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
        """)
        recent = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_registrations': total,
            'recent_registrations': recent
        })
        
    except Exception as e:
        logger.error(f"Stats error: {e}")
        return jsonify({'error': 'Failed to get statistics'}), 500

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and hashlib.sha256(password.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
            session['admin_logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials!', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with registration data"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return render_template('admin_dashboard.html', registrations=[], stats={})
        
        cursor = conn.cursor()
        
        # Get pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = 20
        offset = (page - 1) * per_page
        
        # Get registrations with pagination
        cursor.execute("""
            SELECT id, email, name, timestamp, ip_address
            FROM registrations 
            ORDER BY timestamp DESC 
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        
        registrations = []
        for row in cursor.fetchall():
            registrations.append({
                'id': row[0],
                'email': row[1],
                'name': row[2],
                'timestamp': row[3],
                'ip_address': row[4]
            })
        
        # Get statistics
        cursor.execute("SELECT COUNT(*) FROM registrations")
        total = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM registrations 
            WHERE DATE(timestamp) = CURDATE()
        """)
        daily = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT COUNT(*) FROM registrations 
            WHERE timestamp >= DATE_SUB(NOW(), INTERVAL 7 DAY)
        """)
        weekly = cursor.fetchone()[0]
        
        conn.close()
        
        stats = {
            'total': total,
            'daily': daily,
            'weekly': weekly
        }
        
        return render_template('admin_dashboard.html', 
                             registrations=registrations, 
                             stats=stats, 
                             page=page,
                             per_page=per_page)
        
    except Exception as e:
        logger.error(f"Admin dashboard error: {e}")
        flash('Error loading dashboard!', 'error')
        return render_template('admin_dashboard.html', registrations=[], stats={})

@app.route('/admin/export')
@admin_required
def admin_export():
    """Export registrations as CSV"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('admin_dashboard'))
        
        cursor = conn.cursor()
        cursor.execute("""
            SELECT email, name, timestamp, ip_address
            FROM registrations 
            ORDER BY timestamp DESC
        """)
        
        # Create CSV content
        csv_content = "Email,Name,Timestamp,IP Address\n"
        for row in cursor.fetchall():
            csv_content += f"{row[0]},{row[1] or ''},{row[2]},{row[3] or ''}\n"
        
        conn.close()
        
        # Return CSV file
        from flask import Response
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=registrations.csv'}
        )
        
    except Exception as e:
        logger.error(f"Export error: {e}")
        flash('Export failed!', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:reg_id>')
@admin_required
def admin_delete(reg_id):
    """Delete a registration"""
    try:
        conn = get_db_connection()
        if not conn:
            flash('Database connection failed!', 'error')
            return redirect(url_for('admin_dashboard'))
        
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registrations WHERE id = %s", (reg_id,))
        conn.commit()
        conn.close()
        
        flash('Registration deleted successfully!', 'success')
        
    except Exception as e:
        logger.error(f"Delete error: {e}")
        flash('Delete failed!', 'error')
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    # Initialize database table
    if init_registrations_table():
        logger.info("Database integration successful")
    else:
        logger.error("Database integration failed")
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Teknoledge backend with existing database on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
