from ..models.user import UserCreate, User
from datetime import datetime
from typing import Optional

class UserRepo:
    def __init__(self):
        self.users = {}
        self.id_counter = 1
    
    def create_user(self, user_data: UserCreate) -> User:
        user_id = self.id_counter
        self.id_counter += 1
        
        user = User(
            user_id=user_id,
            name=user_data.name,
            email=user_data.email,
            role=user_data.role,
            status="active",
            created_at=datetime.now()
        )
        self.users[user_id] = user
        return user
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)
    
    def get_all_users(self):
        return list(self.users.values())
    
    def update_user_status(self, user_id: int, status: str) -> Optional[User]:
        user = self.users.get(user_id)
        if user:
            user.status = status
            self.users[user_id] = user
            return user
        return None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        for user in self.users.values():
            if user.email == email:
                return user
        return None
