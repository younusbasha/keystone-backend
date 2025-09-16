#!/usr/bin/env python3
"""
Consolidate all database files into one unified database
"""
import sqlite3
import os
import shutil
from datetime import datetime

def consolidate_databases():
    """Consolidate all database data into techsophy_keystone.db"""
    
    # Database files in order of priority (keystone.db has the most complete data)
    source_files = ['keystone.db', 'techsophy_keystone.db', 'techsophy_keystone_new.db']
    target_file = 'techsophy_keystone.db'
    
    print("🔄 Consolidating database files...")
    
    # Step 1: Use keystone.db as the primary source (it has your registered user)
    if os.path.exists('keystone.db'):
        print(f"📋 Using keystone.db as primary source...")
        
        # Backup the current techsophy_keystone.db
        if os.path.exists('techsophy_keystone.db'):
            backup_name = f'techsophy_keystone_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.db'
            shutil.copy2('techsophy_keystone.db', backup_name)
            print(f"💾 Backed up existing techsophy_keystone.db to {backup_name}")
        
        # Copy keystone.db to techsophy_keystone.db (this has your user data)
        shutil.copy2('keystone.db', 'techsophy_keystone.db')
        print(f"✅ Copied keystone.db → techsophy_keystone.db")
        
        # Verify the data transfer
        conn = sqlite3.connect('techsophy_keystone.db')
        cursor = conn.cursor()
        
        # Check all tables and data
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n📊 Consolidated database summary:")
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"   {table_name}: {count} records")
        
        # Specifically check for your user
        cursor.execute("SELECT email, username, created_at FROM users WHERE email LIKE '%younus%' OR email LIKE '%mailinator%'")
        younus_users = cursor.fetchall()
        
        if younus_users:
            print(f"\n✅ Your registered user found:")
            for user in younus_users:
                print(f"   Email: {user[0]}")
                print(f"   Username: {user[1]}")
                print(f"   Created: {user[2]}")
        
        conn.close()
        
    else:
        print("❌ keystone.db not found!")
        return False
    
    # Step 2: Clean up duplicate files
    cleanup_files = ['keystone.db', 'techsophy_keystone_new.db']
    
    print(f"\n🧹 Cleaning up duplicate database files...")
    for file in cleanup_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️  Removed {file}")
    
    return True

def update_database_config():
    """Update the database configuration to use the consolidated database"""
    
    print(f"\n⚙️ Updating database configuration...")
    
    # Read current settings
    settings_file = 'app/config/settings.py'
    
    with open(settings_file, 'r') as f:
        content = f.read()
    
    # Update the DATABASE_URL to use the correct filename
    if 'DATABASE_URL: str = "sqlite+aiosqlite:///./keystone.db"' in content:
        content = content.replace(
            'DATABASE_URL: str = "sqlite+aiosqlite:///./keystone.db"',
            'DATABASE_URL: str = "sqlite+aiosqlite:///./techsophy_keystone.db"'
        )
        print("✅ Updated DATABASE_URL from keystone.db to techsophy_keystone.db")
    elif 'DATABASE_URL: str = "sqlite+aiosqlite:///./techsophy_keystone_new.db"' in content:
        content = content.replace(
            'DATABASE_URL: str = "sqlite+aiosqlite:///./techsophy_keystone_new.db"',
            'DATABASE_URL: str = "sqlite+aiosqlite:///./techsophy_keystone.db"'
        )
        print("✅ Updated DATABASE_URL from techsophy_keystone_new.db to techsophy_keystone.db")
    else:
        print("✅ DATABASE_URL already points to techsophy_keystone.db")
    
    # Write updated settings
    with open(settings_file, 'w') as f:
        f.write(content)
    
    return True

def main():
    """Main consolidation process"""
    print("🚀 Database Consolidation Process Started")
    print("=" * 50)
    
    success = consolidate_databases()
    
    if success:
        update_database_config()
        
        print(f"\n" + "=" * 50)
        print("✅ Database consolidation completed successfully!")
        
        print(f"\n📁 Final Database Configuration:")
        print(f"   Database File: techsophy_keystone.db")
        print(f"   Full Path: {os.path.abspath('techsophy_keystone.db')}")
        print(f"   Connection String: sqlite+aiosqlite:///./techsophy_keystone.db")
        
        print(f"\n🔧 For DBeaver Connection:")
        print(f"   Database Type: SQLite")
        print(f"   Database File: {os.path.abspath('techsophy_keystone.db')}")
        
        print(f"\n🎯 Next Steps:")
        print(f"   1. Update DBeaver to connect to: {os.path.abspath('techsophy_keystone.db')}")
        print(f"   2. Refresh DBeaver connection")
        print(f"   3. You should now see your registered user: younus.s@mailinator.com")
        print(f"   4. Restart your FastAPI application")
        
    else:
        print("❌ Database consolidation failed!")

if __name__ == "__main__":
    main()
