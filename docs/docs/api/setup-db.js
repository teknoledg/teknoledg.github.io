/*
 * Database Setup Script
 * Purpose: Initialize the registrations table
 * Last Modified: 2024-09-24
 * By: AI Assistant
 * Completeness: 100%
 */

const { sql } = require('@vercel/postgres');

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    // Create the registrations table
    await sql`
      CREATE TABLE IF NOT EXISTS registrations (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        ip_address VARCHAR(45),
        user_agent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `;

    res.status(200).json({ 
      success: true, 
      message: 'Database table created successfully' 
    });

  } catch (error) {
    console.error('Database setup error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Database setup failed: ' + error.message 
    });
  }
}
