from database.DB_connect import DBConnect
from model.interprete import Interprete


class DAO:
    @staticmethod
    def getNodes(minimo):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT n.id AS id, n.name AS nome, n.date_of_birth AS data, COUNT(DISTINCT(r.movie_id)) as numero
                FROM names n, role_mapping r
                WHERE r.name_id = n.id AND n.date_of_birth IS NOT NULL and n.date_of_birth > '1905-12-31'
                GROUP BY n.id, n.name, n.date_of_birth
                HAVING COUNT(DISTINCT(r.movie_id)) >= %s            
                 """

        cursor.execute(query,(minimo,))

        for row in cursor:
            results.append(Interprete(row["id"], row["nome"], row["data"], row["numero"]))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getCoppie():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
            return result

        cursor = cnx.cursor(dictionary=True)
        query = """SELECT r.name_id AS idP, r.movie_id AS idF
                   FROM role_mapping r"""
        cursor.execute(query)
        for row in cursor:
            result.append((row["idP"], row["idF"]))
        cursor.close()
        cnx.close()
        return result