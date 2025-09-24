#!/usr/bin/env python3
"""
Teknoledge Registration Backend
Handles form submissions, stores in SQLite, and sends email notifications
"""

from flask import Flask, request, jsonify, render_template, session, redirect, url_for, flash, send_from_directory
from flask_cors import CORS
import sqlite3
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

# Database configuration
DB_PATH = 'registrations.db'

# Admin credentials (in production, use environment variables)
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'admin')
ADMIN_PASSWORD_HASH = os.getenv('ADMIN_PASSWORD_HASH', hashlib.sha256('admin123'.encode()).hexdigest())

# Email configuration
SMTP_SERVER = 'mail.teknoledg.com'  # Update with actual email server
SMTP_PORT = 587  # or 465 for SSL
EMAIL_USER = 'noreply@teknoledg.com'  # Update with actual email
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')  # Set via environment variable
ADMIN_EMAIL = 'tim@teknoledg.com'

def init_database():
    """Initialize the SQLite database with registrations table"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            name TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            ip_address TEXT,
            user_agent TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")

def send_notification_email(email, name, ip_address):
    """Send notification email to admin"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = ADMIN_EMAIL
        msg['Subject'] = 'New Registration - Teknoledge Updates'
        
        # Email body
        body = f"""
        New user registration received:
        
        Email: {email}
        Name: {name if name else 'Not provided'}
        IP Address: {ip_address}
        Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        This user has registered for product updates.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(EMAIL_USER, ADMIN_EMAIL, text)
        server.quit()
        
        logger.info(f"Notification email sent to {ADMIN_EMAIL}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send notification email: {str(e)}")
        return False

@app.route('/')
def index():
    """Serve the main page"""
    # Read and serve the main index.html file
    try:
        with open('../index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return "Main page not found. Please ensure index.html is in the parent directory.", 404

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
    """Handle registration form submissions"""
    try:
        data = request.get_json()
        email = data.get('email', '').strip()
        name = data.get('name', '').strip()
        
        # Validate email
        if not email or '@' not in email:
            return jsonify({'success': False, 'message': 'Valid email is required'}), 400
        
        # Get client info
        ip_address = request.environ.get('HTTP_X_FORWARDED_FOR', request.environ.get('REMOTE_ADDR', ''))
        user_agent = request.headers.get('User-Agent', '')
        
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            # Insert registration
            cursor.execute('''
                INSERT INTO registrations (email, name, ip_address, user_agent)
                VALUES (?, ?, ?, ?)
            ''', (email, name, ip_address, user_agent))
            
            conn.commit()
            registration_id = cursor.lastrowid
            
            # Send notification email
            email_sent = send_notification_email(email, name, ip_address)
            
            logger.info(f"New registration: {email} (ID: {registration_id})")
            
            return jsonify({
                'success': True,
                'message': 'Thank you for registering! We\'ll notify you when we launch.',
                'email_sent': email_sent
            })
            
        except sqlite3.IntegrityError:
            return jsonify({'success': False, 'message': 'Email already registered'}), 409
            
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'message': 'Registration failed. Please try again.'}), 500
        
    finally:
        conn.close()

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get registration statistics (admin only)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get total registrations
        cursor.execute('SELECT COUNT(*) FROM registrations')
        total = cursor.fetchone()[0]
        
        # Get recent registrations (last 24 hours)
        cursor.execute('''
            SELECT COUNT(*) FROM registrations 
            WHERE timestamp > datetime('now', '-1 day')
        ''')
        recent = cursor.fetchone()[0]
        
        conn.close()
        
        return jsonify({
            'total_registrations': total,
            'recent_registrations': recent
        })
        
    except Exception as e:
        logger.error(f"Stats error: {str(e)}")
        return jsonify({'error': 'Failed to get statistics'}), 500

# Admin authentication decorator
def admin_required(f):
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        # Hash the provided password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if username == ADMIN_USERNAME and password_hash == ADMIN_PASSWORD_HASH:
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
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Get pagination parameters
        page = int(request.args.get('page', 1))
        per_page = 20
        offset = (page - 1) * per_page
        
        # Get total count
        cursor.execute('SELECT COUNT(*) FROM registrations')
        total_count = cursor.fetchone()[0]
        
        # Get registrations with pagination
        cursor.execute('''
            SELECT id, email, name, timestamp, ip_address, user_agent
            FROM registrations
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        ''', (per_page, offset))
        
        registrations = cursor.fetchall()
        
        # Calculate pagination info
        total_pages = (total_count + per_page - 1) // per_page
        has_prev = page > 1
        has_next = page < total_pages
        
        # Get statistics
        cursor.execute('SELECT COUNT(*) FROM registrations')
        total_registrations = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM registrations 
            WHERE timestamp > datetime('now', '-1 day')
        ''')
        recent_registrations = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT COUNT(*) FROM registrations 
            WHERE timestamp > datetime('now', '-7 days')
        ''')
        weekly_registrations = cursor.fetchone()[0]
        
        conn.close()
        
        return render_template('admin_dashboard.html',
                             registrations=registrations,
                             total_registrations=total_registrations,
                             recent_registrations=recent_registrations,
                             weekly_registrations=weekly_registrations,
                             page=page,
                             total_pages=total_pages,
                             has_prev=has_prev,
                             has_next=has_next)
        
    except Exception as e:
        logger.error(f"Admin dashboard error: {str(e)}")
        flash('Error loading dashboard data', 'error')
        return render_template('admin_dashboard.html', registrations=[], error=True)

@app.route('/admin/export')
@admin_required
def admin_export():
    """Export registrations as CSV"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT email, name, timestamp, ip_address
            FROM registrations
            ORDER BY timestamp DESC
        ''')
        
        registrations = cursor.fetchall()
        conn.close()
        
        # Create CSV content
        csv_content = "Email,Name,Timestamp,IP Address\n"
        for reg in registrations:
            csv_content += f"{reg[0]},{reg[1] or ''},{reg[2]},{reg[3]}\n"
        
        from flask import Response
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=registrations.csv'}
        )
        
    except Exception as e:
        logger.error(f"Export error: {str(e)}")
        flash('Error exporting data', 'error')
        return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete/<int:reg_id>')
@admin_required
def admin_delete(reg_id):
    """Delete a registration"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM registrations WHERE id = ?', (reg_id,))
        conn.commit()
        conn.close()
        
        flash('Registration deleted successfully!', 'success')
        
    except Exception as e:
        logger.error(f"Delete error: {str(e)}")
        flash('Error deleting registration', 'error')
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    # Initialize database
    init_database()
    
    # Run the app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    logger.info(f"Starting Teknoledge backend on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
