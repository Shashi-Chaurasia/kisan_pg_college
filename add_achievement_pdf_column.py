#!/usr/bin/env python3
"""
Script to add achievement_pdf column to faculty table
Run this on cPanel: python3 add_achievement_pdf_column.py
"""
import sqlite3
import os
import sys

# Find the database file
db_path = os.path.join('instance', 'kishanpgcollege.db')
if not os.path.exists(db_path):
    # Try alternative paths
    db_path = 'kishanpgcollege.db'
    if not os.path.exists(db_path):
        db_path = os.path.join('..', 'instance', 'kishanpgcollege.db')
        if not os.path.exists(db_path):
            print("Error: Could not find database file")
            print("Please specify the database path manually")
            sys.exit(1)

print(f"Connecting to database: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(faculty)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'achievement_pdf' in columns:
        print("Column 'achievement_pdf' already exists!")
    else:
        print("Adding 'achievement_pdf' column...")
        cursor.execute("ALTER TABLE faculty ADD COLUMN achievement_pdf VARCHAR(200)")
        print("✓ Column 'achievement_pdf' added successfully!")
    
    if 'research_pdf' in columns:
        print("Column 'research_pdf' already exists!")
    else:
        print("Adding 'research_pdf' column...")
        cursor.execute("ALTER TABLE faculty ADD COLUMN research_pdf VARCHAR(200)")
        print("✓ Column 'research_pdf' added successfully!")
    
    if 'created_at' in columns:
        print("Column 'created_at' already exists!")
    else:
        print("Adding 'created_at' column...")
        cursor.execute("ALTER TABLE faculty ADD COLUMN created_at DATETIME")
        print("✓ Column 'created_at' added successfully!")
    
    conn.commit()
    print("\n✓ Database migration completed successfully!")
    
    # Show current columns
    cursor.execute("PRAGMA table_info(faculty)")
    print("\nCurrent faculty table columns:")
    for column in cursor.fetchall():
        print(f"  - {column[1]} ({column[2]})")
    
    conn.close()
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

