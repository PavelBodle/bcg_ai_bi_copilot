import pandas as pd
import sqlite3


def load_data(filepath: str):
    df = pd.read_csv(filepath, encoding="latin1")
    df.columns = [c.strip().replace(" ", "_").replace("-", "_") for c in df.columns]
    # conn = sqlite3.connect(":memory:")
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    df.to_sql("sales", conn, index=False, if_exists="replace")
    return conn, df


def run_query(conn, sql: str):
    try:
        result = pd.read_sql_query(sql, conn)
        return result
    except Exception as e:
        return str(e)


def get_schema(conn) -> str:
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(sales)")
    cols = cursor.fetchall()
    schema = ", ".join([f"{col[1]} ({col[2]})" for col in cols])
    return schema