/*
 * Teknoledge Admin API
 * Purpose: Admin panel for viewing registrations
 * Last Modified: 2024-09-24
 * By: AI Assistant
 * Completeness: 95%
 */

const { sql } = require('@vercel/postgres');

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method === 'GET') {
    // Serve admin panel HTML
    const html = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Teknoledge Admin Panel</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { text-align: center; margin-bottom: 30px; }
        .login-form { max-width: 400px; margin: 50px auto; padding: 20px; border: 1px solid #ddd; border-radius: 8px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007cba; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #005a87; }
        .registrations-table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        .registrations-table th, .registrations-table td { padding: 10px; text-align: left; border-bottom: 1px solid #ddd; }
        .registrations-table th { background: #f8f9fa; font-weight: bold; }
        .logout { float: right; margin-bottom: 20px; }
        .hidden { display: none; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Teknoledge Admin Panel</h1>
        </div>
        
        <div id="loginSection" class="login-form">
            <h2>Admin Login</h2>
            <form id="loginForm">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" required>
                </div>
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" required>
                </div>
                <button type="submit">Login</button>
            </form>
        </div>
        
        <div id="adminSection" class="hidden">
            <div class="logout">
                <button onclick="logout()">Logout</button>
            </div>
            <h2>Registrations</h2>
            <div id="registrationsContainer">
                <p>Loading registrations...</p>
            </div>
        </div>
    </div>
    
    <script>
        function login() {
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            if (username === 'admin' && password === 'teknoledg2024') {
                document.getElementById('loginSection').classList.add('hidden');
                document.getElementById('adminSection').classList.remove('hidden');
                loadRegistrations();
            } else {
                alert('Invalid credentials');
            }
        }
        
        async function loadRegistrations() {
            try {
                const response = await fetch('/api/registrations');
                const data = await response.json();
                
                if (data.success) {
                    displayRegistrations(data.data);
                } else {
                    document.getElementById('registrationsContainer').innerHTML = 
                        '<p>Error loading registrations: ' + data.message + '</p>';
                }
            } catch (error) {
                document.getElementById('registrationsContainer').innerHTML = 
                    '<p>Error loading registrations: ' + error.message + '</p>';
            }
        }
        
        function displayRegistrations(registrations) {
            let html = '<table class="registrations-table"><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Date</th><th>IP</th></tr></thead><tbody>';
            
            registrations.forEach(reg => {
                html += \`<tr>
                    <td>\${reg.id}</td>
                    <td>\${reg.name}</td>
                    <td>\${reg.email}</td>
                    <td>\${new Date(reg.created_at).toLocaleString()}</td>
                    <td>\${reg.ip_address}</td>
                </tr>\`;
            });
            
            html += '</tbody></table>';
            document.getElementById('registrationsContainer').innerHTML = html;
        }
        
        function logout() {
            document.getElementById('loginSection').classList.remove('hidden');
            document.getElementById('adminSection').classList.add('hidden');
        }
        
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            login();
        });
    </script>
</body>
</html>`;
    
    res.setHeader('Content-Type', 'text/html');
    res.status(200).send(html);
    return;
  }

  if (req.method === 'POST') {
    // Handle login
    const { username, password } = req.body;
    
    if (username === 'admin' && password === 'teknoledg2024') {
      res.status(200).json({ success: true, message: 'Login successful' });
    } else {
      res.status(401).json({ success: false, message: 'Invalid credentials' });
    }
    return;
  }

  res.status(405).json({ success: false, message: 'Method not allowed' });
}
