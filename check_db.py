#!/usr/bin/env python3
"""
Script to check and recreate database tables
"""
import sqlite3
import asyncio
from app.config.database import create_tables

def check_sqlite_tables():
    """Check what tables exist in SQLite database"""
    try:
        conn = sqlite3.connect('techsophy_keystone.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        print(f"Tables found in SQLite database: {len(tables)}")
        for table in tables:
            print(f"  - {table[0]}")
        return len(tables) > 0
    except Exception as e:
        print(f"Error checking SQLite tables: {e}")
        return False

async def recreate_tables():
    """Recreate all database tables"""
    try:
        print("Creating database tables...")
        await create_tables()
        print("✓ Database tables created successfully")
        return True
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        return False

async def main():
    print("Checking current database state...")
    has_tables = check_sqlite_tables()
    
    if not has_tables:
        print("\nNo tables found. Creating tables...")
        success = await recreate_tables()
        if success:
            print("\nVerifying tables were created...")
            check_sqlite_tables()
        else:
            print("Failed to create tables")
    else:
        print("Database already has tables!")

if __name__ == "__main__":
    asyncio.run(main())
