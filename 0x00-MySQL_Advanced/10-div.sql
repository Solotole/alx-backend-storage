-- creating a function that divides first from second
-- argument and returns result. if second equals 0 then return 0
DELIMITER //

CREATE FUNCTION SafeDiv(a INT, b INT)
RETURN FLOAT
DETERMINISTIC
BEGIN
    IF b = 0 THEN
        RETURN 0;
    ELSE
        RETURN a / b;
    END IF; 
END //

DELIMITER ;