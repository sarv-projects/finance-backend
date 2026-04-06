
from ..repositories.transaction_repo import TransactionRepo
from ..models.transaction import TransactionCreate
from datetime import datetime
from typing import Optional

class TransactionService:
    def __init__(self, repository: TransactionRepo):
        self.repository = repository
    
    def create_transaction(self, transaction_data: TransactionCreate, user_role: str):
        # Only Admins and Analysts can create transactions
        if user_role not in ["admin", "analyst"]:
            return None
        
        return self.repository.create_transaction(transaction_data)
    
    def get_all_transactions(self, user_role: str, category: Optional[str] = None, trans_type: Optional[str] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        # All authenticated roles (Admin, Analyst, Viewer) can view all
        if user_role not in ["admin", "analyst", "viewer"]:
            return None
        
        transactions = self.repository.get_all()
        
        # Filter by category
        if category:
            transactions = [t for t in transactions if t["category"].lower() == category.lower()]
        
        # Filter by type
        if trans_type:
            transactions = [t for t in transactions if t["type"].lower() == trans_type.lower()]
        
        # Filter by date range
        if start_date:
            transactions = [t for t in transactions if t["date"] >= start_date]
        if end_date:
            transactions = [t for t in transactions if t["date"] <= end_date]
        
        return transactions
    
    def get_transaction_by_id(self, transaction_id: int, user_role: str):
        # All authenticated roles can view a specific transaction
        if user_role not in ["admin", "analyst", "viewer"]:
            return None
            
        return self.repository.get_by_id(transaction_id)
    
    def get_dashboard_summary(self, user_role: str) -> dict | None:
        if user_role not in ["admin", "analyst", "viewer"]:
            return None
        
        transactions = self.repository.get_all()
        
        total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
        total_expense = sum(t["amount"] for t in transactions if t["type"] == "expense")
        net_balance = total_income - total_expense
        
        # Category-wise totals
        category_totals = {}
        for t in transactions:
            cat = t["category"]
            if cat not in category_totals:
                category_totals[cat] = 0
            category_totals[cat] += t["amount"]
        
        return {
            "total_income": total_income,
            "total_expense": total_expense,
            "net_balance": net_balance,
            "category_totals": category_totals,
            "transaction_count": len(transactions)
        }
    
    def delete_transaction(self, transaction_id: int, user_role: str) -> dict | None:
        """
        Delete a transaction. Only Admin can delete.
        Returns the deleted transaction, or None if not allowed or not found.
        """
        # Only Admin can delete
        if user_role != "admin":
            return None
        
        return self.repository.delete(transaction_id)
    
    def update_transaction(self, transaction_id: int, transaction_data: TransactionCreate, user_role: str):
        """
        Update a transaction. Only Admin and Analyst can update.
        """
        if user_role not in ["admin", "analyst"]:
            return None
        
        return self.repository.update(transaction_id, transaction_data)