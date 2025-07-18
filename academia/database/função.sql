
    DELIMITER $$
        CREATE FUNCTION `Fn_CalcularIMC`(
            peso DECIMAL (5, 2),
            altura DECIMAL (3, 2)
        )
            RETURNS DECIMAL(5, 2)
            DETERMINISTIC
        BEGIN

    IF
        altura IS NULL OR altura <= 0 THEN
        RETURN 0;
    END IF;


    RETURN peso / (altura * altura);
    END$$
    DELIMITER ;