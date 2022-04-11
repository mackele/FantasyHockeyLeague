import psycopg2
import traceback

class Postgres ():
    def __enter__(self, *args, **kwargs):
        try:
            self.con=psycopg2.connect(
                user="grupp2_onlinestore", 
                password="n8siil4c",
                host="pgserver.mau.se",
                port="5432",
                database="grupp2_onlinestore")
            self.cur=self.con.cursor()
            return self.cur

        except:
            traceback.print_exc()
    def __exit__(self, *args):
        if self.con:
            self.con.close()
        if self.cur:
            self.cur.close()

"""
används:

from connect import Postgres
with Postgres() as cursor:
    cursor.execute ( select )
    result=cursor.fetchall()

result kan användas var som (ej enbart i with)

Skrivs om och om igen


"""