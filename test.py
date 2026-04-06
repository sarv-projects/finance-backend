from models.transaction import TransactionCreate
t=TransactionCreate(amount=100.0, description="Salary", category="Income", type="income")
print(t.model_dump())