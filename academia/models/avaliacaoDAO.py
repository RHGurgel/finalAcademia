class AvaliacaoDAO:
    def __init__(self, con):
        self.con = con

    def inserir(self, avaliacao):
        try:
            sql = "INSERT INTO avaliacao (peso, altura, braco, ombro, peito, cintura, quadril, abdominal, coxaMedial, panturrilha, Usuario_codigous) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

            cursor = self.con.cursor()
            cursor.execute(sql, (avaliacao.peso, avaliacao.altura, avaliacao.braco, avaliacao.ombro, avaliacao.peito, avaliacao.cintura, avaliacao.quadril, avaliacao.abdominal, avaliacao.coxaMedial, avaliacao.panturrilha, avaliacao.Usuario_codigous))
            self.con.commit()
            codigo = cursor.lastrowid
            return codigo
        except:
            return 0

    def listar(self, codigo=None):
        try:
            cursor = self.con.cursor()
            if codigo != None:
                # pegar somente uma planta (mantenha o existente)
                sql = "SELECT * FROM Avaliacao WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                avaliacao = cursor.fetchone()
                return avaliacao
            else:
                # pegar todas as plantas (mantenha o existente)
                sql = "SELECT * FROM Avaliacao WHERE Usuario_codigous IN (SELECT codigous FROM usuario)"
                cursor.execute(sql)
                ficha = cursor.fetchall()
                return ficha
        except:
            return None

    def atualizar(self, avaliacao, codigo):
        try:
            sql = """UPDATE avaliacao SET peso=%s, altura=%s, braco=%s, ombro=%s, peito=%s,
                     cintura=%s, quadril=%s, abdominal=%s, coxaMedial=%s, panturrilha=%s 
                     WHERE codigoav=%s"""
            cursor = self.con.cursor()
            cursor.execute(sql, (
                avaliacao.peso, avaliacao.altura, avaliacao.braco, avaliacao.ombro,
                avaliacao.peito, avaliacao.cintura, avaliacao.quadril, avaliacao.abdominal,
                avaliacao.coxaMedial, avaliacao.panturrilha, codigo
            ))
            self.con.commit()
            return True
        except Exception as e:
            print("Erro ao atualizar:", e)
            return False

    def deletar(self, codigo):
        try:
            sql = "DELETE FROM avaliacao WHERE codigoav=%s"
            cursor = self.con.cursor()
            cursor.execute(sql, (codigo,))
            self.con.commit()
            return True
        except Exception as e:
            print("Erro ao deletar:", e)
            return False

    # dao.py

    # IMPORTANTE: Garanta que você tem a biblioteca correta instalada.
    # No terminal, execute: pip install mysql-connector-python
    import mysql.connector

    class AvaliacaoDAO:
        def __init__(self, db_connection):
            self.db = db_connection
            # Este cursor é essencial para o HTML funcionar facilmente.
            self.cursor = self.db.cursor(dictionary=True)

        def buscar_todas_avaliacoes_com_log(self):
            sql = """
                  SELECT A.*, \
                         U.nome AS nome_aluno, \
                         U.sobrenome, \
                         LogInfo.ultima_data, \
                         LogInfo.ultimo_tipo
                  FROM Avaliacao AS A \
                           JOIN \
                       Usuarios AS U ON A.Usuario_codigous = U.codigous \
                           LEFT JOIN \
                       (SELECT id_avaliacao_afetada, \
                               MAX(data_acao)                                                           AS ultima_data, \
                               -- Pega o tipo de ação da linha que tem a data mais recente \
                               SUBSTRING_INDEX(GROUP_CONCAT(tipo_acao ORDER BY data_acao DESC), ',', 1) AS ultimo_tipo \
                        FROM LogAvaliacoes \
                        GROUP BY id_avaliacao_afetada) AS LogInfo ON A.codigoav = LogInfo.id_avaliacao_afetada
                  ORDER BY A.codigoav DESC; \
                  """
            try:
                self.cursor.execute(sql)
                resultados = self.cursor.fetchall()
                print(f"DAO: Encontradas {len(resultados)} avaliações.")  # Linha de debug
                return resultados
            except Exception as e:
                print(f"!!! ERRO NA DAO: {e} !!!")
                return []