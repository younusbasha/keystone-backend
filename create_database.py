#!/usr/bin/env python3
"""
Direct SQLite database creation script
"""
import sqlite3
import os

def create_sqlite_database():
    """Create SQLite database with tables directly"""
    db_path = 'techsophy_keystone_new.db'

    # Remove existing file if it exists
    if os.path.exists(db_path):
        os.remove(db_path)

    # Create new database connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create all tables based on the SQLAlchemy schema
    tables_sql = [
        """
        CREATE TABLE roles (
            id TEXT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            display_name VARCHAR(255) NOT NULL,
            description TEXT,
            parent_role_id TEXT,
            level INTEGER,
            is_system_role BOOLEAN,
            is_active BOOLEAN,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_deleted BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY(parent_role_id) REFERENCES roles (id)
        )
        """,
        """
        CREATE TABLE permissions (
            id TEXT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            display_name VARCHAR(255) NOT NULL,
            description TEXT,
            resource_type VARCHAR(50) NOT NULL,
            permission_type VARCHAR(20) NOT NULL,
            scope TEXT,
            is_system_permission BOOLEAN,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_deleted BOOLEAN NOT NULL DEFAULT 0
        )
        """,
        """
        CREATE TABLE users (
            id TEXT PRIMARY KEY,
            email VARCHAR(255) NOT NULL UNIQUE,
            username VARCHAR(100) NOT NULL UNIQUE,
            first_name VARCHAR(100) NOT NULL,
            last_name VARCHAR(100) NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            is_active BOOLEAN NOT NULL DEFAULT 1,
            is_verified BOOLEAN NOT NULL DEFAULT 0,
            avatar_url VARCHAR(500),
            bio TEXT,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_deleted BOOLEAN NOT NULL DEFAULT 0
        )
        """,
        """
        CREATE TABLE projects (
            id TEXT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            status VARCHAR(20) NOT NULL,
            priority VARCHAR(20) NOT NULL,
            start_date DATETIME,
            end_date DATETIME,
            budget FLOAT,
            owner_id TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_deleted BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY(owner_id) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE requirements (
            id TEXT PRIMARY KEY,
            title VARCHAR(200) NOT NULL,
            description TEXT NOT NULL,
            type VARCHAR(20) NOT NULL,
            priority VARCHAR(20) NOT NULL,
            status VARCHAR(20) NOT NULL,
            acceptance_criteria TEXT,
            tags TEXT,
            ai_analysis TEXT,
            project_id TEXT NOT NULL,
            created_by TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_deleted BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY(project_id) REFERENCES projects (id),
            FOREIGN KEY(created_by) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE tasks (
            id TEXT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            status VARCHAR(20),
            priority VARCHAR(20),
            task_type VARCHAR(20),
            project_id TEXT NOT NULL,
            requirement_id TEXT,
            assigned_to TEXT,
            created_by TEXT NOT NULL,
            estimated_hours FLOAT,
            actual_hours FLOAT,
            complexity_score FLOAT,
            ai_confidence FLOAT,
            due_date DATETIME,
            started_at DATETIME,
            completed_at DATETIME,
            ai_generated BOOLEAN DEFAULT 0,
            ai_suggestions TEXT,
            acceptance_criteria TEXT,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_deleted BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY(project_id) REFERENCES projects (id),
            FOREIGN KEY(requirement_id) REFERENCES requirements (id),
            FOREIGN KEY(assigned_to) REFERENCES users (id),
            FOREIGN KEY(created_by) REFERENCES users (id)
        )
        """,
        """
        CREATE TABLE ai_agents (
            id TEXT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            agent_type VARCHAR(20) NOT NULL,
            status VARCHAR(20),
            version VARCHAR(50),
            capabilities TEXT,
            configuration TEXT,
            permissions TEXT,
            success_rate FLOAT,
            average_confidence FLOAT,
            total_actions INTEGER,
            successful_actions INTEGER,
            max_concurrent_actions INTEGER,
            current_load INTEGER,
            project_id TEXT,
            created_at DATETIME NOT NULL,
            updated_at DATETIME NOT NULL,
            is_deleted BOOLEAN NOT NULL DEFAULT 0,
            FOREIGN KEY(project_id) REFERENCES projects (id)
        )
        """
    ]

    try:
        for sql in tables_sql:
            cursor.execute(sql)

        conn.commit()

        # Verify tables were created
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        print(f"✓ Successfully created {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")

        conn.close()
        return db_path

    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        conn.close()
        return None

if __name__ == "__main__":
    db_file = create_sqlite_database()
    if db_file:
        print(f"\n✅ Database created successfully: {db_file}")
        print(f"📁 Full path: {os.path.abspath(db_file)}")
        print("\n🔧 For DBeaver connection:")
        print(f"   Database file: {os.path.abspath(db_file)}")
    else:
        print("❌ Failed to create database")
