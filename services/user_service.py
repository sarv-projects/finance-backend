from ..repositories.user_repo import UserRepo
from ..models.user import UserCreate, UserUpdate
from typing import Optional

class UserService:
    def __init__(self, repository: UserRepo):
        self.repository = repository
    
    def create_user(self, user_data: UserCreate, admin_role: str):
        # Only admins can create users
        if admin_role != "admin":
            return None
        
        # Check if email already exists
        if self.repository.get_user_by_email(user_data.email):
            return {"error": "Email already exists"}
        
        return self.repository.create_user(user_data)
    
    def get_user(self, user_id: int, auth_role: str):
        # All roles can view users
        if auth_role not in ["admin", "analyst", "viewer"]:
            return None
        
        return self.repository.get_user_by_id(user_id)
    
    def get_all_users(self, auth_role: str):
        # Only admins can list all users
        if auth_role != "admin":
            return None
        
        return self.repository.get_all_users()
    
    def update_user_status(self, user_id: int, status_data: UserUpdate, admin_role: str):
        # Only admins can update user status
        if admin_role != "admin":
            return None
        
        user = self.repository.update_user_status(user_id, status_data.status)
        if not user:
            return {"error": "User not found"}
        
        return user
