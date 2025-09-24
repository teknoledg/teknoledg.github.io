/*
 * Teknoledge Registrations API
 * Purpose: Fetch all registrations for admin panel
 * Last Modified: 2024-09-24
 * By: AI Assistant
 * Completeness: 95%
 */

const { sql } = require('@vercel/postgres');

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (req.method === 'OPTIONS') {
    res.status(200).end();
    return;
  }

  if (req.method !== 'GET') {
    return res.status(405).json({ success: false, message: 'Method not allowed' });
  }

  try {
    // Fetch all registrations
    const result = await sql`
      SELECT id, email, name, ip_address, user_agent, created_at
      FROM registrations 
      ORDER BY created_at DESC
    `;

    res.status(200).json({ 
      success: true, 
      data: result.rows 
    });

  } catch (error) {
    console.error('Fetch registrations error:', error);
    res.status(500).json({ 
      success: false, 
      message: 'Failed to fetch registrations' 
    });
  }
}
