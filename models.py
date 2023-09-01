from sqlalchemy import Column, String, Integer, DATE, ForeignKey

from database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    owner = Column(String)
    balance = Column(Integer)
    currency = Column(String)
    created_at = Column(DATE)


class Entries(Base):
    __tablename__ = 'enteries'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'))
    amount = Column(Integer)
    created_at = Column(DATE)


class Transfers(Base):
    __tablename__ = 'transfers'

    id = Column(Integer, primary_key=True, index=True)
    from_account_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'))
    to_account_id = Column(Integer, ForeignKey('accounts.id', ondelete='CASCADE'))
    amount = Column(Integer)
    created_at = Column(DATE)

