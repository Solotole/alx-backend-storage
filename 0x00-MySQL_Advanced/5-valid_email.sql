-- updating valid_email when email is updated
DELIMITER //

CREATE TRIGGER update_valid_email_before_email_updated
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.email <> OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END //

DELIMITER ;