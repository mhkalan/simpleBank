from pydantic import BaseModel


class Account(BaseModel):
    owner: str
    balance: int
    currency: str


class Entry(BaseModel):
    account_id: int
    amount: int


class Transfer(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: int
