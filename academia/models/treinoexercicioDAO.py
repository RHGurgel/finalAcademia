class TreinoExercicioDAO:
    def __init__(self, con):
        self.con = con

    def inserir(self, Treino_codigotr, Exercicios_codigoex):
        try:
            sql = "INSERT INTO treino_has_exercicios (Treino_codigotr, Exercicios_codigoex) VALUES (%s, %s)"
            cursor = self.con.cursor()
            cursor.execute(sql, (Treino_codigotr, Exercicios_codigoex))
            self.con.commit()
            return True
        except:
            return False

    def listar_exercicios_por_treino(self, treino_id):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM View_Treino_Detalhes WHERE treino_id = %s"
            cursor.execute(sql, (treino_id,))
            return cursor.fetchall()
        except:
            return []