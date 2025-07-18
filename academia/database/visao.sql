CREATE VIEW View_Treino_Detalhes AS
SELECT
    T.codigotr AS treino_id,
    T.nome AS nome_treino,
    T.data_criacao,
    T.usuario_id,
    E.codigoex AS exercicio_id,
    E.nome AS exercicio_nome,
    E.descricao,
    E.equipamento,
    E.tp_treino AS grupo_muscular,
    E.video
FROM Treino T
JOIN Treino_Exercicio TE ON T.id = TE.treino_id
JOIN Exercicios E ON TE.exercicio_id = E.id;