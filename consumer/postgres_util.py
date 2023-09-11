import psycopg2

class Postgres_DB:
    def __init__(self, dbname, user, password, host, port) -> None:
        self.conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()
    
    def create_table(self):
        # Define your table creation SQL query here
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS edits (
                id serial PRIMARY KEY,
                minute timestamp,
                wiki text,
                count integer
            )
        '''
        self.cur.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, minute, wiki, count):
        # Define your insert SQL query here
        insert_query = '''
            INSERT INTO edits (minute, wiki, count)
            VALUES (%s, %s, %s)
        '''
        data = (minute, wiki, count)
        self.cur.execute(insert_query, data)
        self.conn.commit()
    
    def close(self):
        if self.conn:
            self.cur.close()
            self.conn.close()

    

