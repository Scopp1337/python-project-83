from psycopg2.extras import DictCursor


class UrlRepository:
    def __init__(self, conn):
        self.conn = conn

    def add_url(self, url):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, NOW()) RETURNING id",
                (url,)
            )
            id = cur.fetchone()["id"]
            self.conn.commit()
            return id

    def get_all_urls(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
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