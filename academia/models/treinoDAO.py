class TreinoDAO:
    def __init__(self, con):
        self.con = con

    def inserir(self, treino):
        try:
            sql = "INSERT INTO Treino (nome, usuario_codigous) VALUES (%s, %s)"
            cursor = self.con.cursor()
            cursor.execute(sql, (treino.nome, treino.usuario_codigous))
            self.con.commit()
            return cursor.lastrowid
        except:
            return 0

    def listar_por_usuario(self, usuario_codigous):
        try:
            cursor = self.con.cursor()
            sql = "SELECT * FROM Treino WHERE usuario_codigous = %s"
            cursor.execute(sql, (usuario_codigous,))
            return cursor.fetchall()
        except:
            return []

    def deletar_treino(self, treino_id):
        try:
            cursor = self.con.cursor()

            # Primeiro deleta os exercícios associados
            sql_delete_exercicios = "DELETE FROM treino_has_exercicios WHERE Treino_codigotr = %s"
            cursor.execute(sql_delete_exercicios, (treino_id,))

            # Depois deleta o treino
            sql_delete_treino = "DELETE FROM Treino WHERE codigotr = %s"
            cursor.execute(sql_delete_treino, (treino_id,))

            self.con.commit()
            return cursor.rowcount > 0  # Retorna True se deletou algo
        except Exception as e:
            print(f"Erro ao deletar treino: {e}")
            self.con.rollback()
            return False

    def buscar_treino_por_id(self, treino_id):
        try:
            cursor = self.con.cursor(dictionary=True)
            sql = """
                SELECT t.*, GROUP_CONCAT(e.id) as exercicios_ids 
                FROM Treino t
                LEFT JOIN Treino_Exercicio te ON t.id = te.treino_id
                LEFT JOIN Exercicios e ON te.exercicio_id = e.id
                WHERE t.id = %s
                GROUP BY t.id
            """
            cursor.execute(sql, (treino_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Erro ao buscar treino: {e}")
            return None

    def atualizar_treino(self, treino_id, novo_nome, exercicios_ids):
        cursor = self.con.cursor()
        try:
            # Inicia transação
            cursor.execute("START TRANSACTION")

            # 1. Atualiza o nome do treino
            cursor.execute("UPDATE Treino SET nome = %s WHERE codigotr = %s",
                           (novo_nome, treino_id))

            # 2. Remove associações antigas
            cursor.execute("DELETE FROM treino_has_exercicios WHERE Treino_codigotr = %s",
                           (treino_id,))

            # 3. Adiciona novas associações
            for exercicio_id in exercicios_ids:
                cursor.execute(
                    "INSERT INTO treino_has_exercicios (Treino_codigotr, Exercicios_codigoex) VALUES (%s, %s)",
                    (treino_id, exercicio_id)
                )

            self.con.commit()
            return True
        except Exception as e:
            self.con.rollback()
            print(f"Erro ao atualizar treino: {e}")
            return False
        finally:
            cursor.close()