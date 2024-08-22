-- script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE count INT DEFAULT 0;
    DECLARE total INT DEFAULT 0;
    -- DECLARE users_id INT DEFAULT 0;

    -- SET users_id = user_id
    -- number of projects of a user
    SELECT COUNT(*) INTO count
    FROM corrections
    WHERE user_id = user_id;
    -- total of scores of a student
    SELECT SUM(score) INTO total
    FROM corrections
    WHERE user_id = user_id;
    -- updating new average score of the user
    IF count > 0 THEN
        UPDATE users
        SET average_score = total / count
        WHERE id = user_id;
    ELSE
        UPDATE users
        SET average_score = 0
        WHERE id = user_id;
    END IF;
END //

DELIMITER ;