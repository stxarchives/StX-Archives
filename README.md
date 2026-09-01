# StX Archive

StX Archive is a web platform dedicated to securely and anonymously documenting school policies, infrastructure issues, fee discrepancies, and personal experiences.

## Features

- **Anonymous Submissions**: Users can post their experiences securely.
- **Ultimate Admin Dashboard**: 
  - Live Analytics
  - Bulk Actions (Verify/Delete)
  - Security Controls (In-dashboard Password Change)
  - "Kill Switch" (Maintenance Mode)
- **Live Search & Filtering**: Instantly search through submission queues.
- **Dynamic Categories**: Experiences are categorized automatically with live counts on the home page.
- **Dark Mode Support**: Beautiful and modern UI built with Tailwind CSS.

## Tech Stack

- **Backend**: Python / Flask
- **Frontend**: HTML / Tailwind CSS / Vanilla JS
- **Database**: Supabase (PostgreSQL)

## Local Development

1. Clone the repository.
2. Install dependencies (e.g., `pip install flask supabase python-dotenv`).
3. Rename `.env.example` to `.env` (if applicable) and add your Supabase credentials.
4. Run `python app.py` to start the local server on port 5000.
