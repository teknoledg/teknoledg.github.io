/*
 * Teknoledge Registration API
 * Purpose: Handle form submissions with Vercel Postgres
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

  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    const { email, name } = req.body;

    // Validate input
    if (!email || !name) {
      return res.status(400).json({ 
        success: false, 
        message: 'Email and name are required' 
      });
    }

    // Check if email already exists
    const existingUser = await sql`
      SELECT id FROM registrations WHERE email = ${email}
    `;

    if (existingUser.rows.length > 0) {
      return res.status(400).json({ 
        success: false, 
        message: 'Email already registered' 
      });
    }

    // Insert new registration
    const result = await sql`
      INSERT INTO registrations (email, name, ip_address, user_agent, created_at)
      VALUES (${email}, ${name}, ${req.headers['x-forwarded-for'] || req.connection.remoteAddress}, ${req.headers['user-agent']}, NOW())
      RETURNING id
    `;

    // Send email notification (using Vercel's email service or external service)
    await sendEmailNotification(email, name);

    res.status(200).json({ 
      success: true, 
      message: 'Registration successful!',
      id: result.rows[0].id
    });

  } catch (error) {
    console.error('Registration error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Registration failed. Please try again.' 
    });
  }
}

async function sendEmailNotification(email, name) {
  // For now, just log the notification
  // In production, integrate with SendGrid, Resend, or similar
  console.log(`New registration: ${name} (${email})`);
  
  // TODO: Implement actual email sending
  // You can use Vercel's email integrations or external services
}
