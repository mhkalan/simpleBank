from fastapi import FastAPI, Depends
import models
import serializer
from utils import *
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime
import random

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/account')
async def get_all_account(db: Session = Depends(get_db)):
    try:
        db.flush()
        accounts = db.query(models.Account).all()
        return accounts, custom_200_exception_handler()
    except:
        await custom_500_exception_handler()


@app.post('/account')
async def create_account(account: serializer.Account, db: Session = Depends(get_db)):
    try:
        account_model = models.Account()
        account_model.id = random.getrandbits(32)
        account_model.owner = account.owner
        account_model.balance = account.balance
        account_model.currency = account.currency
        account_model.created_at = datetime.datetime.now()

        db.add(account_model)
        db.commit()
        return custom_201_exception_handler()
    except:
        return custom_500_exception_handler()


@app.get('/account/{account_id}')
async def account_detail(account_id: int, db: Session = Depends(get_db)):
    try:
        if not db.query(models.Account).filter(models.Account.id == account_id).exists():
            return custom_404_exception_handler()
        account_model = db.query(models.Account).filter(models.Account.id == account_id).first()
        return custom_200_exception_handler(), account_model
    except:
        return custom_500_exception_handler()


@app.post('/account/{account_id}')
async def account_update(account_id: int, account: serializer.Account, db: Session = Depends(get_db)):
    try:
        if not db.query(models.Account).filter(models.Account.id == account_id).exists():
            return custom_404_exception_handler()
        account_model = db.query(models.Account).filter(models.Account.id == account_id).first()
        account_model.id = account_id
        account_model.owner = account.owner
        account_model.balance = account.balance
        account_model.currency = account.currency
        account_model.created_at = account_model.created_at

        db.commit()
        return custom_201_exception_handler()
    except:
        return custom_500_exception_handler()


@app.get('/entry')
async def get_entries(db: Session = Depends(get_db)):
    try:
        db.flush()
        return db.query(models.Entries).all(), custom_200_exception_handler()
    except:
        await custom_500_exception_handler()


@app.post('/entry')
async def create_entry(entry: serializer.Entry, db: Session = Depends(get_db)):
    try:
        if not db.query(models.Account).filter(models.Account.id == entry.account_id).exists():
            return custom_404_exception_handler()
        entry_model = models.Entries()
        account_model = db.query(models.Account).filter(models.Account.id == entry.account_id).first()
        entry_model.id = random.getrandbits(32)
        entry_model.amount = entry.amount
        entry_model.account_id = entry.account_id
        entry_model.created_at = datetime.datetime.now()
        db.add(entry_model)
        db.commit()
        account_model.balance -= entry.amount
        db.commit()
        return custom_201_exception_handler()
    except:
        return custom_500_exception_handler()


@app.get('/entry/{entry_id}')
async def entry_detail(entry_id: int, db: Session = Depends(get_db)):
    try:
        if not db.query(models.Entries).filter(models.Entries.id == entry_id).exists():
            return custom_404_exception_handler()
        entry_model = db.query(models.Entries).filter(models.Entries.id == entry_id).first()
        return entry_model, custom_200_exception_handler()
    except:
        return custom_500_exception_handler()


@app.post('/entry/{entry_id}')
async def entry_update(entry_id: int, entry: serializer.Entry, db: Session = Depends(get_db)):
    try:
        if not db.query(models.Entries).filter(models.Entries.id == entry_id).exists():
            return custom_404_exception_handler()
        entry_model = db.query(models.Entries).filter(models.Entries.id == entry_id).first()
        entry_model.id = entry_id
        entry_model.account_id = entry.account_id
        entry_model.amount = entry.amount
        entry_model.created_at = entry_model.created_at
        db.commit()
        return custom_201_exception_handler()
    except:
        return custom_500_exception_handler()


@app.get('/transfer')
async def get_transfers(db: Session = Depends(get_db)):
    try:
        db.flush()
        return db.query(models.Transfers).all(), custom_200_exception_handler()
    except:
        return custom_500_exception_handler()


@app.post('/transfer')
async def create_transfer(transfer: serializer.Transfer, db: Session = Depends(get_db)):
    try:
        if not db.query(models.Account).filter(models.Account.id == transfer.from_account_id).exists():
            return custom_404_exception_handler()
        if not db.query(models.Account).filter(models.Account.id == transfer.to_account_id).exists():
            return custom_404_exception_handler()
        transfer_model = models.Transfers()
        from_account = db.query(models.Account).filter(models.Account.id == transfer.from_account_id).first()
        to_account = db.query(models.Account).filter(models.Account.id == transfer.to_account_id).first()
        transfer_model.id = random.getrandbits(32)
        transfer_model.from_account_id = transfer.from_account_id
        transfer_model.to_account_id = transfer.to_account_id
        transfer_model.amount = transfer.amount
        transfer_model.created_at = datetime.datetime.now()
        db.add(transfer_model)
        db.commit()
        from_account.balance -= transfer.amount
        to_account.balance += transfer.amount
        db.commit()
        return custom_201_exception_handler()
    except:
        return custom_500_exception_handler()


@app.get('/transfer/{transfer_id}')
async def transfer_detail(transfer_id: int, db: Session = Depends(get_db)):
    try:
        if not db.query(models.Transfers).filter(models.Transfers.id == transfer_id).exists():
            return custom_404_exception_handler()
        transfer_model = db.query(models.Transfers).filter(models.Transfers.id == transfer_id).first()
        return transfer_model, custom_200_exception_handler()
    except:
        return custom_500_exception_handler()


@app.post('/transfer/{transfer_id}')
async def transfer_update(transfer_id: int, transfer: serializer.Transfer, db: Session = Depends(get_db)):
    try:
        if not db.query(models.Transfers).filter(models.Transfers.id == transfer_id).exists():
            return custom_404_exception_handler()
        transfer_model = db.query(models.Transfers).filter(models.Transfers.id == transfer_id).first()
        transfer_model.id = transfer_id
        transfer_model.from_account_id = transfer.from_account_id
        transfer_model.to_account_id = transfer.to_account_id
        transfer_model.amount = transfer.amount
        transfer_model.created_at = transfer_model.created_at
        db.commit()
        return custom_201_exception_handler()
    except:
        return custom_500_exception_handler()