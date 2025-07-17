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
                # pegar somente uma planta
                sql = "SELECT * FROM Avaliacao WHERE codigo=%s"
                cursor.execute(sql, (codigo,))
                avaliacao = cursor.fetchone()
                return avaliacao
            else:
                # pegar todas as plantas
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
