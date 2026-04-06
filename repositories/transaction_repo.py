from ..models.transaction import TransactionCreate


class TransactionRepo:
    def __init__(self):
        self._transactions = []
        self._next_id = 1

    def create_transaction(self, transaction_data:TransactionCreate)->dict:
        
        new_transaction={**transaction_data.model_dump(), "id": self._next_id}
        new_transaction["date"]=new_transaction["date"].isoformat()
        self._transactions.append(new_transaction)
        self._next_id+=1
        return new_transaction
    def get_all(self)->list:
        return self._transactions
    
    def get_by_id(self, transaction_id:int)->dict | None:
        for transaction in self._transactions:
            if transaction["id"]==transaction_id:
                return transaction
        return None     

    def delete(self, transaction_id: int) -> dict | None:
      """
      Delete a transaction by ID.
      Returns the deleted transaction, or None if not found.
      """
      for i, transaction in enumerate(self._transactions):
        if transaction["id"] == transaction_id:
            return self._transactions.pop(i)
      return None
    
    def update(self, transaction_id: int, transaction_data: TransactionCreate) -> dict | None:
      """
      Update a transaction by ID.
      Returns the updated transaction, or None if not found.
      """
      for i, transaction in enumerate(self._transactions):
        if transaction["id"] == transaction_id:
            updated_transaction = {**transaction_data.model_dump(), "id": transaction_id}
            updated_transaction["date"] = updated_transaction["date"].isoformat()
            self._transactions[i] = updated_transaction
            return updated_transaction
      return None    