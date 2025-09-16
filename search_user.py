#!/usr/bin/env python3
"""
Search for younus user across all database files
"""
import sqlite3
import os

def search_user_across_databases():
    """Search for younus user in all database files"""
    db_files = ['keystone.db', 'techsophy_keystone.db', 'techsophy_keystone_new.db']

    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"\n=== {db_file} ===")
            try:
                conn = sqlite3.connect(db_file)
                cursor = conn.cursor()

                # Search for younus or mailinator users
                cursor.execute("""
                    SELECT email, username, first_name, last_name, created_at 
                    FROM users 
                    WHERE email LIKE '%younus%' OR email LIKE '%mailinator%'
                    ORDER BY created_at DESC
                """)
                users = cursor.fetchall()

                if users:
                    print(f"  Found {len(users)} matching user(s):")
                    for user in users:
                        print(f"    Email: {user[0]}")
                        print(f"    Username: {user[1]}")
                        print(f"    Name: {user[2]} {user[3]}")
                        print(f"    Created: {user[4]}")
                        print("    ---")
                else:
                    print("  No younus/mailinator users found")

                # Also show total user count
                cursor.execute("SELECT COUNT(*) FROM users")
                total_users = cursor.fetchone()[0]
                print(f"  Total users in this database: {total_users}")

                conn.close()

            except Exception as e:
                print(f"  Error reading {db_file}: {e}")
        else:
            print(f"  {db_file} does not exist")

if __name__ == "__main__":
    search_user_across_databases()
