import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_url(self, url):
        with self.conn.cursor() as cur:
            cur.execute("INTO INSERT urls (name) VALUES (%s) RETURNING id")
            id = cur.fetchone()["id"]
            url["id"] = id
            return id
        self.conn.commit()

    def get_all_urls(self):
        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM urls ORDER BY id DESC")
            return [dict(row) for row in cur]

    def find_id(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def find_url(self, url):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT id, name FROM urls WHERE name = %s", (url,))
            row = cur.fetchone()
            return dict(row) if row else None