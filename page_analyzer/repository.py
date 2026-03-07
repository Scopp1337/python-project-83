import psycopg2
from psycopg2.extras import RealDictCursor


class DatabaseConnection:
    def __init__(self, database_url):
        self.database_url = database_url

    def __enter__(self):
        self.conn = psycopg2.connect(
            self.database_url,
            cursor_factory=RealDictCursor
        )
        return self.conn.cursor()

    def __exit__(self, type, value, traceback):
        if type is None:
            self.conn.commit()
        else:
            self.conn.rollback()
        self.conn.close()


class UrlRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def add_url(self, url):
        with DatabaseConnection(self.db_url) as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) "
                "VALUES (%s, NOW()) RETURNING id",
                (url,)
            )
            result = cur.fetchone()
            return result['id']

    def get_all_urls(self):
        with DatabaseConnection(self.db_url) as cur:
            cur.execute("""
                SELECT 
                    u.*,
                    (
                        SELECT created_at 
                        FROM url_checks 
                        WHERE url_id = u.id 
                        ORDER BY id DESC 
                        LIMIT 1
                    ) as last_check,
                    (
                        SELECT status_code 
                        FROM url_checks 
                        WHERE url_id = u.id 
                        ORDER BY id DESC 
                        LIMIT 1
                    ) as last_status_code
                FROM urls AS u
                ORDER BY u.id DESC
            """)
            return [dict(row) for row in cur]

    def find_id(self, id):
        with DatabaseConnection(self.db_url) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def find_url(self, url):
        with DatabaseConnection(self.db_url) as cur:
            cur.execute("SELECT id, name FROM urls WHERE name = %s", (url,))
            row = cur.fetchone()
            return dict(row) if row else None

    def create_check(
            self,
            url_id,
            status_code,
            h1=None,
            title=None,
            description=None
    ):
        with DatabaseConnection(self.db_url) as cur:
            cur.execute("""
                INSERT INTO url_checks 
                (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                RETURNING id
            """, (url_id, status_code, h1, title, description))
            result = cur.fetchone()
            return result['id']

    def get_checks(self, url_id):
        with DatabaseConnection(self.db_url) as cur:
            cur.execute("""
                SELECT * FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
            """, (url_id,))
            return [dict(row) for row in cur]

    def get_last_check_for_urls(self):
        with DatabaseConnection(self.db_url) as cur:
            cur.execute("""
                SELECT url_id, status_code, created_at
                FROM url_checks
                ORDER BY url_id, id DESC
            """)

            result = {}
            for row in cur:
                row_dict = dict(row)
                url_id = row_dict['url_id']
                if url_id not in result:
                    result[url_id] = {
                        'status_code': row_dict['status_code'],
                        'created_at': row_dict['created_at']
                    }

            return result