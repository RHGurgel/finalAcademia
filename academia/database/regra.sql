DELIMITER //

CREATE TRIGGER excluir_log
BEFORE DELETE ON avaliacao
FOR EACH ROW
BEGIN
    DELETE FROM logavaliacoes WHERE id_avaliacao_afetada = OLD.codigoav;

END;
//

DELIMITER ;