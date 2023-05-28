import os
import time
from typing import Union
from fastapi import FastAPI, HTTPException
from tinydb import TinyDB, Query

from classes import Transaction
from entity_handler import fetch_splitwise_transactions

app = FastAPI()
DB_PATH = "db.json"
ENTITY_TO_HANDLER = {
    "splitwise": fetch_splitwise_transactions,
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/initialize_database")
def new_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    db = TinyDB("db.json")
    db.insert({"created_on": time.time()})


@app.post("/initialize_bank_table")
def new_bank_table(bank_name):
    if os.path.exists(DB_PATH):
        db = TinyDB(DB_PATH)
        table = db.table(bank_name)
        if len(table.all()) == 0:
            # Create only if the table is empty
            table.insert({"curr_balance": 0})
            table.insert({"last_updated": 0})
        else:
            raise HTTPException(
                status_code=404, detail="Trying to initialize a pre-existing DB"
            )
    else:
        raise HTTPException(
            status_code=404, detail="Initialize DB before creating table"
        )


@app.post("/delete_entity_table")
def delete_bank_table(entity_name):
    if os.path.exists(DB_PATH):
        db = TinyDB(DB_PATH)
        table = db.table(entity_name)
        if len(table.all()) == 0:
            # Create only if the table is empty
            raise HTTPException(
                status_code=404, detail="Trying to delete an empty table"
            )
        else:
            db.drop_table(entity_name)
    else:
        raise HTTPException(status_code=404, detail="DB doesn't exist")


@app.post("/register_api_key")
def register_api_key(api_key_name, api_key_secret):
    if os.path.exists(DB_PATH):
        db = TinyDB(DB_PATH)
        db.remove(Query()[api_key_name].exists())
        db.insert({api_key_name: api_key_secret})
    else:
        raise HTTPException(
            status_code=404, detail="Initialize DB before creating table"
        )


def return_transactions_for_entity(entity_name, last_update_time, maybe_key):
    if entity_name not in ENTITY_TO_HANDLER:
        raise HTTPException(
            status_code=404,
            detail="Entity doesn't have a handler!",
        )
    else:
        return ENTITY_TO_HANDLER[entity_name](
            last_updated=last_update_time, maybe_key=maybe_key
        )


@app.post("/update_entity_transactions")
def update_entity_transactions(entity_name):
    if os.path.exists(DB_PATH):
        db = TinyDB(DB_PATH)
        table = db.table(entity_name)
        if len(table.all()) == 0:
            # Create only if the table is empty
            raise HTTPException(status_code=404, detail="Entity Table doesn't exist")
        else:
            last_updated_time = table.search((Query().last_updated.exists()))
            if len(last_updated_time) > 1:
                raise HTTPException(
                    status_code=500,
                    detail="Multiple updated times exist. This shouldn't happen",
                )
            else:
                maybe_key = db.search(Query()[entity_name].exists())
                maybe_key = maybe_key[0][entity_name] if len(maybe_key) > 0 else None
                last_updated_time = last_updated_time[0]["last_updated"]
                curr_balance, latest_transactions = return_transactions_for_entity(
                    entity_name, last_updated_time, maybe_key
                )
                for transaction in latest_transactions:
                    print(transaction.jsonify())
                    table.insert(transaction.jsonify())

                table.update(
                    {"curr_balance": curr_balance}, Query().curr_balance.exists()
                )
                table.update(
                    {"last_updated": time.time()}, Query().last_updated.exists()
                )

    else:
        raise HTTPException(
            status_code=404, detail="Initialize DB before creating table"
        )
