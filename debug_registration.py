#!/usr/bin/env python3
"""
Debug registration issue
"""
import asyncio
import sys
sys.path.append('.')

from app.config.database import async_session_factory
from app.services.auth_service import auth_service
from app.schemas.user import UserCreate

async def debug_registration():
    """Debug user registration"""
    async with async_session_factory() as db:
        try:
            user_data = UserCreate(
                email="debug@example.com",
                username="debuguser",
                first_name="Debug",
                last_name="User",
                password="Password123"
            )
            
            print("Creating user with data:", user_data.dict())
            created_user = await auth_service.create_user(db, user_data)
            print("✅ User created successfully:", created_user.id)
            
        except Exception as e:
            print("❌ Registration failed with error:")
            print(f"Error type: {type(e)}")
            print(f"Error message: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_registration())
