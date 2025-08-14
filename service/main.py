from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import os

DB_PATH = "/data/app.db"

# ensure data directory exists when running outside compose (optional)
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

app = FastAPI(title="SQLite Service")

class ItemIn(BaseModel):
    name: str
    value: int

class ItemOut(ItemIn):
    id: int


def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/init")
def init_db():
    """Create table if not exists"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            value INTEGER NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    return {"status": "ok"}

@app.post("/add", response_model=ItemOut)
def add_item(item: ItemIn):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO items (name, value) VALUES (?, ?)", (item.name, item.value))
    conn.commit()
    item_id = cur.lastrowid
    conn.close()
    return ItemOut(id=item_id, **item.dict())

@app.get("/items", response_model=List[ItemOut])
def list_items():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, value FROM items")
    rows = cur.fetchall()
    conn.close()
    return [ItemOut(id=r["id"], name=r["name"], value=r["value"]) for r in rows]

@app.get("/item/{item_id}", response_model=ItemOut)
def get_item(item_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, value FROM items WHERE id = ?", (item_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return ItemOut(id=row["id"], name=row["name"], value=row["value"])