<?php
/*
 * Teknoledge API Backend
 * Purpose: Handle form submissions and admin panel
 * Last Modified: 2024-09-24
 * By: AI Assistant
 * Completeness: 95%
 */

// Enable CORS for frontend
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

// Include configuration
require_once 'config.php';

// Database connection
function getDBConnection() {
    global $db_config;
    
    try {
        $pdo = new PDO(
            "mysql:host={$db_config['host']};dbname={$db_config['dbname']};charset=utf8mb4",
            $db_config['username'],
            $db_config['password'],
            [
                PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
                PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
            ]
        );
        return $pdo;
    } catch (PDOException $e) {
        error_log("Database connection failed: " . $e->getMessage());
        return null;
    }
}

// Initialize database table
function initDatabase() {
    $pdo = getDBConnection();
    if (!$pdo) return false;
    
    $sql = "CREATE TABLE IF NOT EXISTS registrations (
        id INT AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        ip_address VARCHAR(45),
        user_agent TEXT
    )";
    
    try {
        $pdo->exec($sql);
        return true;
    } catch (PDOException $e) {
        error_log("Database initialization failed: " . $e->getMessage());
        return false;
    }
}

// Send email notification
function sendEmailNotification($email, $name) {
    global $email_config;
    
    $message = "
    New registration received:
    
    Name: $name
    Email: $email
    Date: " . date('Y-m-d H:i:s') . "
    IP: " . $_SERVER['REMOTE_ADDR'] . "
    
    ---
    Teknoledge Registration System
    ";
    
    $headers = "From: {$email_config['from']}\r\n";
    $headers .= "Reply-To: {$email_config['from']}\r\n";
    $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
    
    return mail($email_config['to'], $email_config['subject'], $message, $headers);
}

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    
    if ($action === 'register') {
        $email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
        $name = trim($_POST['name'] ?? '');
        
        if (!$email || !$name) {
            echo json_encode(['success' => false, 'message' => 'Invalid email or name']);
            exit;
        }
        
        // Initialize database
        if (!initDatabase()) {
            echo json_encode(['success' => false, 'message' => 'Database error']);
            exit;
        }
        
        $pdo = getDBConnection();
        if (!$pdo) {
            echo json_encode(['success' => false, 'message' => 'Database connection failed']);
            exit;
        }
        
        try {
            // Check if email already exists
            $stmt = $pdo->prepare("SELECT id FROM registrations WHERE email = ?");
            $stmt->execute([$email]);
            
            if ($stmt->fetch()) {
                echo json_encode(['success' => false, 'message' => 'Email already registered']);
                exit;
            }
            
            // Insert new registration
            $stmt = $pdo->prepare("
                INSERT INTO registrations (email, name, ip_address, user_agent) 
                VALUES (?, ?, ?, ?)
            ");
            $stmt->execute([
                $email,
                $name,
                $_SERVER['REMOTE_ADDR'],
                $_SERVER['HTTP_USER_AGENT'] ?? ''
            ]);
            
            // Send email notification
            sendEmailNotification($email, $name);
            
            echo json_encode(['success' => true, 'message' => 'Registration successful!']);
            
        } catch (PDOException $e) {
            error_log("Registration failed: " . $e->getMessage());
            echo json_encode(['success' => false, 'message' => 'Registration failed']);
        }
    }
    
    elseif ($action === 'admin_login') {
        $username = $_POST['username'] ?? '';
        $password = $_POST['password'] ?? '';
        
        // Admin authentication
        global $admin_config;
        if ($username === $admin_config['username'] && $password === $admin_config['password']) {
            session_start();
            $_SESSION['admin_logged_in'] = true;
            echo json_encode(['success' => true, 'message' => 'Login successful']);
        } else {
            echo json_encode(['success' => false, 'message' => 'Invalid credentials']);
        }
    }
    
    elseif ($action === 'get_registrations') {
        session_start();
        if (!isset($_SESSION['admin_logged_in']) || !$_SESSION['admin_logged_in']) {
            echo json_encode(['success' => false, 'message' => 'Not authenticated']);
            exit;
        }
        
        $pdo = getDBConnection();
        if (!$pdo) {
            echo json_encode(['success' => false, 'message' => 'Database connection failed']);
            exit;
        }
        
        try {
            $stmt = $pdo->query("SELECT * FROM registrations ORDER BY created_at DESC");
            $registrations = $stmt->fetchAll();
            echo json_encode(['success' => true, 'data' => $registrations]);
        } catch (PDOException $e) {
            echo json_encode(['success' => false, 'message' => 'Database error']);
        }
    }
    
    else {
        echo json_encode(['success' => false, 'message' => 'Invalid action']);
    }
}

// Handle GET requests
elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
    $action = $_GET['action'] ?? '';
    
    if ($action === 'admin') {
        // Serve admin panel
        ?>
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
                    const formData = new FormData();
                    formData.append('action', 'admin_login');
                    formData.append('username', document.getElementById('username').value);
                    formData.append('password', document.getElementById('password').value);
                    
                    fetch('api.php', {
                        method: 'POST',
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            document.getElementById('loginSection').classList.add('hidden');
                            document.getElementById('adminSection').classList.remove('hidden');
                            loadRegistrations();
                        } else {
                            alert('Login failed: ' + data.message);
                        }
                    });
                }
                
                function loadRegistrations() {
                    fetch('api.php?action=get_registrations')
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            displayRegistrations(data.data);
                        } else {
                            document.getElementById('registrationsContainer').innerHTML = '<p>Error loading registrations: ' + data.message + '</p>';
                        }
                    });
                }
                
                function displayRegistrations(registrations) {
                    let html = '<table class="registrations-table"><thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Date</th><th>IP</th></tr></thead><tbody>';
                    
                    registrations.forEach(reg => {
                        html += `<tr>
                            <td>${reg.id}</td>
                            <td>${reg.name}</td>
                            <td>${reg.email}</td>
                            <td>${reg.created_at}</td>
                            <td>${reg.ip_address}</td>
                        </tr>`;
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
        </html>
        <?php
    }
    
    else {
        echo json_encode(['success' => false, 'message' => 'Invalid action']);
    }
}

else {
    echo json_encode(['success' => false, 'message' => 'Method not allowed']);
}
?>
