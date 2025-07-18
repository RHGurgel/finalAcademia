-- Criar gatilhos
DELIMITER
$$
CREATE TRIGGER log_after_avaliacao_insert
    AFTER INSERT
    ON Avaliacao
    FOR EACH ROW
BEGIN
    INSERT INTO LogAvaliacoes (tipo_acao, id_avaliacao_afetada, id_usuario_autor, dados_antes, dados_depois)
    VALUES ('CRIAÇÃO', NEW.codigoav, @app_user_id, NULL,
            JSON_OBJECT('peso', NEW.peso, 'altura', NEW.altura, 'braco', NEW.braco, 'ombro', NEW.ombro, 'peito',
                        NEW.peito, 'cintura', NEW.cintura, 'quadril', NEW.quadril, 'abdominal', NEW.abdominal,
                        'coxaMedial', NEW.coxaMedial, 'panturrilha', NEW.panturrilha));
    END$$
    DELIMITER ;

-- GATILHO PARA EDIÇÃO (UPDATE) em Avaliacao
DELIMITER $$
    CREATE TRIGGER log_after_avaliacao_update
        AFTER UPDATE
        ON Avaliacao
        FOR EACH ROW
    BEGIN
        INSERT INTO LogAvaliacoes (tipo_acao, id_avaliacao_afetada, id_usuario_autor, dados_antes, dados_depois)
        VALUES ('EDIÇÃO', NEW.codigoav, @app_user_id,
                JSON_OBJECT('peso', OLD.peso, 'altura', OLD.altura, 'braco', OLD.braco, 'ombro', OLD.ombro, 'peito',
                            OLD.peito, 'cintura', OLD.cintura, 'quadril', OLD.quadril, 'abdominal', OLD.abdominal,
                            'coxaMedial', OLD.coxaMedial, 'panturrilha', OLD.panturrilha),
                JSON_OBJECT('peso', NEW.peso, 'altura', NEW.altura, 'braco', NEW.braco, 'ombro', NEW.ombro, 'peito',
                            NEW.peito, 'cintura', NEW.cintura, 'quadril', NEW.quadril, 'abdominal', NEW.abdominal,
                            'coxaMedial', NEW.coxaMedial, 'panturrilha', NEW.panturrilha));
        END$$
        DELIMITER ;