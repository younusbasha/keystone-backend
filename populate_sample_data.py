#!/usr/bin/env python3
"""
Populate database with sample data for testing
"""
import asyncio
import sqlite3
from datetime import datetime, timedelta
import uuid
import hashlib

def create_sample_data():
    """Create sample data directly in SQLite"""
    conn = sqlite3.connect('techsophy_keystone.db')
    cursor = conn.cursor()
    
    try:
        # Create sample users
        users_data = [
            {
                'id': str(uuid.uuid4()),
                'email': 'admin@techsophy.com',
                'username': 'admin',
                'first_name': 'System',
                'last_name': 'Administrator',
                'hashed_password': hashlib.sha256('admin123'.encode()).hexdigest(),
                'is_active': True,
                'is_verified': True,
                'bio': 'System Administrator',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            },
            {
                'id': str(uuid.uuid4()),
                'email': 'john.doe@techsophy.com',
                'username': 'johndoe',
                'first_name': 'John',
                'last_name': 'Doe',
                'hashed_password': hashlib.sha256('password123'.encode()).hexdigest(),
                'is_active': True,
                'is_verified': True,
                'bio': 'Senior Developer',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            },
            {
                'id': str(uuid.uuid4()),
                'email': 'jane.smith@techsophy.com',
                'username': 'janesmith',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'hashed_password': hashlib.sha256('password123'.encode()).hexdigest(),
                'is_active': True,
                'is_verified': True,
                'bio': 'Project Manager',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            }
        ]
        
        # Insert users
        for user in users_data:
            cursor.execute("""
                INSERT INTO users (id, email, username, first_name, last_name, hashed_password, 
                                 is_active, is_verified, bio, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user['id'], user['email'], user['username'], user['first_name'], 
                user['last_name'], user['hashed_password'], user['is_active'], 
                user['is_verified'], user['bio'], user['created_at'], 
                user['updated_at'], user['is_deleted']
            ))
        
        # Create sample projects
        admin_id = users_data[0]['id']
        john_id = users_data[1]['id']
        
        projects_data = [
            {
                'id': str(uuid.uuid4()),
                'name': 'AI-Powered E-Commerce Platform',
                'description': 'Building a next-generation e-commerce platform with AI recommendations',
                'status': 'active',
                'priority': 'high',
                'start_date': datetime.now().isoformat(),
                'end_date': (datetime.now() + timedelta(days=90)).isoformat(),
                'budget': 150000.0,
                'owner_id': admin_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            },
            {
                'id': str(uuid.uuid4()),
                'name': 'Mobile Banking App',
                'description': 'Secure mobile banking application with biometric authentication',
                'status': 'planning',
                'priority': 'medium',
                'start_date': (datetime.now() + timedelta(days=30)).isoformat(),
                'end_date': (datetime.now() + timedelta(days=120)).isoformat(),
                'budget': 200000.0,
                'owner_id': john_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            }
        ]
        
        # Insert projects
        for project in projects_data:
            cursor.execute("""
                INSERT INTO projects (id, name, description, status, priority, start_date, 
                                    end_date, budget, owner_id, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                project['id'], project['name'], project['description'], project['status'],
                project['priority'], project['start_date'], project['end_date'], 
                project['budget'], project['owner_id'], project['created_at'], 
                project['updated_at'], project['is_deleted']
            ))
        
        # Create sample requirements
        project1_id = projects_data[0]['id']
        requirements_data = [
            {
                'id': str(uuid.uuid4()),
                'title': 'User Authentication System',
                'description': 'Implement secure user authentication with JWT tokens',
                'type': 'functional',
                'priority': 'high',
                'status': 'approved',
                'acceptance_criteria': '["User can login", "JWT tokens generated", "Password encryption"]',
                'tags': '["security", "authentication"]',
                'ai_analysis': '{"complexity": "medium", "effort": "5 days"}',
                'project_id': project1_id,
                'created_by': admin_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            },
            {
                'id': str(uuid.uuid4()),
                'title': 'Product Recommendation Engine',
                'description': 'AI-powered product recommendations based on user behavior',
                'type': 'functional',
                'priority': 'medium',
                'status': 'draft',
                'acceptance_criteria': '["ML model trained", "API endpoints", "Real-time recommendations"]',
                'tags': '["ai", "ml", "recommendations"]',
                'ai_analysis': '{"complexity": "high", "effort": "15 days"}',
                'project_id': project1_id,
                'created_by': john_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            }
        ]
        
        # Insert requirements
        for req in requirements_data:
            cursor.execute("""
                INSERT INTO requirements (id, title, description, type, priority, status,
                                        acceptance_criteria, tags, ai_analysis, project_id, 
                                        created_by, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                req['id'], req['title'], req['description'], req['type'], req['priority'],
                req['status'], req['acceptance_criteria'], req['tags'], req['ai_analysis'],
                req['project_id'], req['created_by'], req['created_at'], 
                req['updated_at'], req['is_deleted']
            ))
        
        # Create sample tasks
        req1_id = requirements_data[0]['id']
        tasks_data = [
            {
                'id': str(uuid.uuid4()),
                'title': 'Setup JWT Authentication',
                'description': 'Configure JWT token generation and validation',
                'status': 'in_progress',
                'priority': 'high',
                'task_type': 'development',
                'project_id': project1_id,
                'requirement_id': req1_id,
                'assigned_to': john_id,
                'created_by': admin_id,
                'estimated_hours': 8.0,
                'actual_hours': 6.0,
                'complexity_score': 0.7,
                'ai_confidence': 0.85,
                'due_date': (datetime.now() + timedelta(days=3)).isoformat(),
                'started_at': datetime.now().isoformat(),
                'ai_generated': True,
                'ai_suggestions': '{"approach": "Use FastAPI JWT", "libraries": ["python-jose"]}',
                'acceptance_criteria': '["JWT tokens work", "Secure endpoints", "Token refresh"]',
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            },
            {
                'id': str(uuid.uuid4()),
                'title': 'Create User Registration API',
                'description': 'Develop API endpoint for user registration',
                'status': 'completed',
                'priority': 'high',
                'task_type': 'development',
                'project_id': project1_id,
                'requirement_id': req1_id,
                'assigned_to': john_id,
                'created_by': admin_id,
                'estimated_hours': 4.0,
                'actual_hours': 3.5,
                'complexity_score': 0.5,
                'ai_confidence': 0.9,
                'due_date': (datetime.now() - timedelta(days=1)).isoformat(),
                'started_at': (datetime.now() - timedelta(days=2)).isoformat(),
                'completed_at': (datetime.now() - timedelta(hours=6)).isoformat(),
                'ai_generated': True,
                'ai_suggestions': '{"validation": "Pydantic schemas", "database": "SQLAlchemy"}',
                'acceptance_criteria': '["User can register", "Email validation", "Password hashing"]',
                'created_at': (datetime.now() - timedelta(days=3)).isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            }
        ]
        
        # Insert tasks
        for task in tasks_data:
            cursor.execute("""
                INSERT INTO tasks (id, title, description, status, priority, task_type,
                                 project_id, requirement_id, assigned_to, created_by,
                                 estimated_hours, actual_hours, complexity_score, ai_confidence,
                                 due_date, started_at, completed_at, ai_generated, ai_suggestions,
                                 acceptance_criteria, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task['id'], task['title'], task['description'], task['status'], task['priority'],
                task['task_type'], task['project_id'], task['requirement_id'], task['assigned_to'],
                task['created_by'], task['estimated_hours'], task['actual_hours'], 
                task['complexity_score'], task['ai_confidence'], task['due_date'], 
                task['started_at'], task.get('completed_at'), task['ai_generated'], 
                task['ai_suggestions'], task['acceptance_criteria'], task['created_at'], 
                task['updated_at'], task['is_deleted']
            ))
        
        # Create sample AI agents
        ai_agents_data = [
            {
                'id': str(uuid.uuid4()),
                'name': 'CodeGen AI Agent',
                'agent_type': 'code_generator',
                'status': 'active',
                'version': '1.0.0',
                'capabilities': '["code_generation", "testing", "documentation"]',
                'configuration': '{"model": "gpt-4", "max_tokens": 4000}',
                'permissions': '["read_requirements", "write_code", "run_tests"]',
                'success_rate': 0.92,
                'average_confidence': 0.88,
                'total_actions': 45,
                'successful_actions': 41,
                'max_concurrent_actions': 3,
                'current_load': 1,
                'project_id': project1_id,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'is_deleted': False
            }
        ]
        
        # Insert AI agents
        for agent in ai_agents_data:
            cursor.execute("""
                INSERT INTO ai_agents (id, name, agent_type, status, version, capabilities,
                                     configuration, permissions, success_rate, average_confidence,
                                     total_actions, successful_actions, max_concurrent_actions,
                                     current_load, project_id, created_at, updated_at, is_deleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                agent['id'], agent['name'], agent['agent_type'], agent['status'], agent['version'],
                agent['capabilities'], agent['configuration'], agent['permissions'], 
                agent['success_rate'], agent['average_confidence'], agent['total_actions'],
                agent['successful_actions'], agent['max_concurrent_actions'], agent['current_load'],
                agent['project_id'], agent['created_at'], agent['updated_at'], agent['is_deleted']
            ))
        
        conn.commit()
        
        # Verify data was inserted
        cursor.execute('SELECT COUNT(*) FROM users')
        users_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM projects')
        projects_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM requirements')
        requirements_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM tasks')
        tasks_count = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM ai_agents')
        agents_count = cursor.fetchone()[0]
        
        print("✅ Sample data created successfully!")
        print(f"📊 Data Summary:")
        print(f"   👥 Users: {users_count}")
        print(f"   📋 Projects: {projects_count}")
        print(f"   📝 Requirements: {requirements_count}")
        print(f"   ✅ Tasks: {tasks_count}")
        print(f"   🤖 AI Agents: {agents_count}")
        
        print(f"\n🔐 Sample Login Credentials:")
        print(f"   Username: admin | Password: admin123")
        print(f"   Username: johndoe | Password: password123")
        print(f"   Username: janesmith | Password: password123")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creating sample data: {e}")
        conn.rollback()
        conn.close()
        return False

if __name__ == "__main__":
    create_sample_data()
