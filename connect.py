import psycopg2
import traceback


# Emilia, Kod utifrån
class Postgres ():
    def __enter__(self, *args, **kwargs):
        '''
            Funktionen försöker ansluta till databasservern.

            return:
                returnerar möjligheten att använda cursor samt conn när klassen används.
        '''
        try:
            self.con=psycopg2.connect(
                user="grupp2_onlinestore", 
                password="n8siil4c",
                host="pgserver.mau.se",
                port="5432",
                database="grupp2_onlinestore")
            self.cur=self.con.cursor()
            return (self.cur, self.con)

        except:
            traceback.print_exc()

    def __exit__(self, *args):
        '''
            Funktionen stänger anvlutningen till databasen samt cursor och conn.
        '''
        if self.con:
            self.con.close()
        if self.cur:
            self.cur.close()