from fastapi import FastAPI, Query, HTTPException
from typing import Optional, List
import sqlite3
import datetime

app = FastAPI()

# Зависимость для подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect("traffic_db.sqlite")
    conn.row_factory = sqlite3.Row
    return conn

# Получение суммарного трафика с фильтрами
@app.get("/traffic")
def get_traffic(
    name: Optional[str] = None,
    ip: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Базовый запрос
    query = """
        SELECT c.id AS customer_id, c.name, SUM(t.received_traffic) AS total_traffic
        FROM customers c
        JOIN traffic t ON c.id = t.customer_id
        WHERE 1=1
    """
    params = []

    # Фильтры
    if name:
        query += " AND c.name LIKE ?"
        params.append(f"%{name}%")
    if ip:
        query += " AND t.ip = ?"
        params.append(ip)
    if date_from:
        query += " AND t.date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND t.date <= ?"
        params.append(date_to)

    query += " GROUP BY c.id, c.name"

    # Выполнение запроса
    cursor.execute(query, params)
    rows = cursor.fetchall()

    conn.close()

    # Формирование результата
    result = [{"customer_id": row["customer_id"], "name": row["name"], "total_traffic": row["total_traffic"]} for row in rows]
    return result