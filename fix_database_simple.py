#!/usr/bin/env python3
"""
Simple script to add missing columns using direct SQLite connection
Run this on cPanel: python3 fix_database_simple.py
"""
import sqlite3
import os
import sys

def find_database():
    """Find the database file in common locations"""
    possible_paths = [
        'instance/kishanpgcollege.db',
        'kishanpgcollege.db',
        '../instance/kishanpgcollege.db',
        os.path.join(os.path.dirname(__file__), 'instance', 'kishanpgcollege.db'),
        os.path.join(os.path.dirname(__file__), 'kishanpgcollege.db'),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return os.path.abspath(path)
    
    return None

# Find database
db_path = find_database()

if not db_path:
    print("Error: Could not find database file")
    print("Please run this script from your project directory")
    print("Or specify the database path manually")
    sys.exit(1)

print(f"Found database: {db_path}")
print("Connecting...")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check current columns
    cursor.execute("PRAGMA table_info(faculty)")
    columns = [row[1] for row in cursor.fetchall()]
    print(f"\nCurrent columns: {', '.join(columns)}")
    
    # Add missing columns
    changes_made = False
    
    if 'achievement_pdf' not in columns:
        print("\nAdding 'achievement_pdf' column...")
        cursor.execute("ALTER TABLE faculty ADD COLUMN achievement_pdf VARCHAR(200)")
        changes_made = True
        print("✓ Added 'achievement_pdf'")
    else:
        print("✓ 'achievement_pdf' already exists")
    
    if 'research_pdf' not in columns:
        print("Adding 'research_pdf' column...")
        cursor.execute("ALTER TABLE faculty ADD COLUMN research_pdf VARCHAR(200)")
        changes_made = True
        print("✓ Added 'research_pdf'")
    else:
        print("✓ 'research_pdf' already exists")
    
    if 'created_at' not in columns:
        print("Adding 'created_at' column...")
        cursor.execute("ALTER TABLE faculty ADD COLUMN created_at DATETIME")
        changes_made = True
        print("✓ Added 'created_at'")
    else:
        print("✓ 'created_at' already exists")
    
    if changes_made:
        conn.commit()
        print("\n✓ Database updated successfully!")
    else:
        print("\n✓ All columns already exist - no changes needed!")
    
    # Show updated columns
    cursor.execute("PRAGMA table_info(faculty)")
    print("\nUpdated table structure:")
    for row in cursor.fetchall():
        nullable = "NULL" if row[3] == 0 else "NOT NULL"
        default = f" DEFAULT {row[4]}" if row[4] else ""
        print(f"  - {row[1]} ({row[2]}) {nullable}{default}")
    
    conn.close()
    print("\n✓ Done!")
    
except sqlite3.Error as e:
    print(f"\n✗ Database error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

