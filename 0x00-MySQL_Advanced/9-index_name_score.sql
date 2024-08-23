-- Create an index idx_name_first on the first letter of the name column
-- and score
CREATE INDEX idx_name_first_score
ON names(name(1), score);