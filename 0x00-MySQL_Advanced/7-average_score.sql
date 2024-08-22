-- script that creates a stored procedure ComputeAverageScoreForUser
-- that computes and store the average score for a student
DELIMITER //
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    DECLARE count INT DEFAULT 0;
    DECLARE total INT DEFAULT 0;
    DECLARE average FLOAT DEFAULT 0;
    -- number of projects of a user
    SELECT COUNT(*) INTO count
    FROM corrections
    WHERE user_id = user_id;
    -- total of scores of a student
    SELECT COALESCE(SUM(score), 0) INTO total
    FROM corrections
    WHERE user_id = user_id;
    -- updating new average score of the user

    IF count > 0 THEN
        SET average = total / count;
    ELSE
        SET average = 0;
    END IF;

    UPDATE users
    SET average_score = average
    WHERE id = user_id;
END //

DELIMITER ;