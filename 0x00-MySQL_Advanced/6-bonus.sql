-- script that creates a stored procedure AddBonus
-- adds a new correction for a student
DELIMITER //

CREATE PROCEDURE AddBonus(IN user_id INT, IN  project_name VARCHAR(255), IN score INT)
BEGIN
    DECLARE project_id INT DEFAULT NULL;

    -- checking if project name exists
    SELECT id INTO project_id
    FROM projects
    WHERE name = project_name
    LIMIT 1;

    IF project_id IS NULL THEN
        -- innserting the new peoject name
        INSERT INTO projects (name)
        VALUES (project_name);

        -- obtaining the newly made project name
        SELECT id INTO project_id
        FROM projects
        WHERE name = project_name
        LIMIT 1;
    END IF;
    -- inserting new corrction data
    INSERT INTO corrections (user_id, project_id, score)
    VALUES (user_id, project_id, score);
END //

DELIMITER ;