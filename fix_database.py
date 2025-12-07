#!/usr/bin/env python3
"""
Script to add missing columns to faculty table
Run this on cPanel: python3 fix_database.py
"""
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    from models import db
    
    app = create_app()
    
    with app.app_context():
        # Get the database connection
        from sqlalchemy import text
        
        print("Connecting to database...")
        
        # Check current columns
        result = db.session.execute(text("PRAGMA table_info(faculty)"))
        columns = [row[1] for row in result.fetchall()]
        print(f"Current columns: {', '.join(columns)}")
        
        # Add missing columns
        if 'achievement_pdf' not in columns:
            print("Adding 'achievement_pdf' column...")
            db.session.execute(text("ALTER TABLE faculty ADD COLUMN achievement_pdf VARCHAR(200)"))
            print("✓ Added 'achievement_pdf'")
        else:
            print("✓ 'achievement_pdf' already exists")
        
        if 'research_pdf' not in columns:
            print("Adding 'research_pdf' column...")
            db.session.execute(text("ALTER TABLE faculty ADD COLUMN research_pdf VARCHAR(200)"))
            print("✓ Added 'research_pdf'")
        else:
            print("✓ 'research_pdf' already exists")
        
        if 'created_at' not in columns:
            print("Adding 'created_at' column...")
            db.session.execute(text("ALTER TABLE faculty ADD COLUMN created_at DATETIME"))
            print("✓ Added 'created_at'")
        else:
            print("✓ 'created_at' already exists")
        
        db.session.commit()
        print("\n✓ Database migration completed successfully!")
        
        # Verify
        result = db.session.execute(text("PRAGMA table_info(faculty)"))
        print("\nUpdated columns:")
        for row in result.fetchall():
            print(f"  - {row[1]} ({row[2]})")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

