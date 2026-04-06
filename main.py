from fastapi import FastAPI, HTTPException, Header, Query
from datetime import datetime
from models.transaction import TransactionCreate
from models.user import UserCreate, UserUpdate
from repositories.transaction_repo import TransactionRepo
from repositories.user_repo import UserRepo
from services.transaction_service import TransactionService
from services.user_service import UserService


app = FastAPI(title="Finance Backend API", version="1.0.0")

# Initialize the layers
transaction_repo = TransactionRepo()
user_repo = UserRepo()
transaction_service = TransactionService(transaction_repo)
user_service = UserService(user_repo)

# ============ USER ENDPOINTS ============

@app.post("/users")
def create_user(
    user: UserCreate,
    x_user_role: str = Header(..., alias="X-User-Role")
):
    """Create a new user. Only admins can create users."""
    result = user_service.create_user(user, x_user_role)
    if result is None:
        raise HTTPException(status_code=403, detail="Not authorized to create users")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@app.get("/users")
def get_all_users(
    x_user_role: str = Header(..., alias="X-User-Role")
):
    """Get all users. Only admins can view all users."""
    result = user_service.get_all_users(x_user_role)
    if result is None:
        raise HTTPException(status_code=403, detail="Not authorized to view users")
    return result

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    x_user_role: str = Header(..., alias="X-User-Role")
):
    """Get a specific user."""
    result = user_service.get_user(user_id, x_user_role)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result

@app.put("/users/{user_id}/status")
def update_user_status(
    user_id: int,
    status_data: UserUpdate,
    x_user_role: str = Header(..., alias="X-User-Role")
):
    """Update user status (active/inactive). Only admins can update user status."""
    result = user_service.update_user_status(user_id, status_data, x_user_role)
    if result is None:
        raise HTTPException(status_code=403, detail="Not authorized to update users")
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

# ============ TRANSACTION ENDPOINTS ============

@app.post("/transactions")
def create_transaction(
    transaction: TransactionCreate, 
    x_user_role: str = Header(..., alias="X-User-Role")
):
    """Create a new transaction. Only admins and analysts can create."""
    result = transaction_service.create_transaction(transaction, x_user_role)
    if result is None:
        raise HTTPException(status_code=403, detail="Not authorized to create transactions")
    return result

@app.get("/transactions")
def get_all_transactions(
    x_user_role: str = Header(..., alias="X-User-Role"),
    category: str = Query(None, description="Filter by category"),
    type: str = Query(None, description="Filter by type (income/expense)"),
    start_date: datetime = Query(None, description="Filter by start date"),
    end_date: datetime = Query(None, description="Filter by end date")
):
    """Get all transactions with optional filters."""
    result = transaction_service.get_all_transactions(
        x_user_role, 
        category=category,
        trans_type=type,
        start_date=start_date,
        end_date=end_date
    )
    if result is None:
        raise HTTPException(status_code=403, detail="Not authorized to view transactions")
    return result

@app.get("/transactions/{transaction_id}")
def get_transaction(
    transaction_id: int, 
    x_user_role: str = Header(..., alias="X-User-Role")
):
    """Get a specific transaction."""
    result = transaction_service.get_transaction_by_id(transaction_id, x_user_role)
    
    if result is None:
        if x_user_role not in ["admin", "analyst", "viewer"]:
            raise HTTPException(status_code=403, detail="Not authorized")
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return result

@app.put("/transactions/{transaction_id}")
def update_transaction(
    transaction_id: int,
    transaction: TransactionCreate,
    x_user_role: str = Header(..., alias="X-User-Role")
):
    """Update a transaction. Only admins and analysts can update."""
    result = transaction_service.update_transaction(transaction_id, transaction, x_user_role)
    
    if result is None:
        if x_user_role not in ["admin", "analyst"]:
            raise HTTPException(status_code=403, detail="Not authorized to update transactions")
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return result

@app.delete("/transactions/{transaction_id}")
def delete_transaction(
    transaction_id: int,
    x_user_role: str = Header(..., alias="X-User-Role")
):
    """Delete a transaction. Only admins can delete."""
    result = transaction_service.delete_transaction(transaction_id, x_user_role)
    
    if result is None:
        if x_user_role != "admin":
            raise HTTPException(status_code=403, detail="Not authorized to delete transactions")
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    return {"message": "Transaction deleted successfully", "deleted": result}

# ============ DASHBOARD ENDPOINTS ============

@app.get("/dashboard/summary")
def get_dashboard_summary(x_user_role: str = Header(..., alias="X-User-Role")):
    """
    Dashboard endpoint that returns:
    - Total income
    - Total expenses  
    - Net balance
    - Category-wise totals
    - Transaction count
    
    Accessible to: admin, analyst, viewer
    """
    result = transaction_service.get_dashboard_summary(x_user_role)
    
    if result is None:
        raise HTTPException(status_code=403, detail="Not authorized to view dashboard")
    
    return result
