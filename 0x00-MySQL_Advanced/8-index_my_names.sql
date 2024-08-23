-- Drop the index if it exists to avoid duplication errors
DROP INDEX IF EXISTS idx_name_first ON names;

-- Create an index idx_name_first on the first letter of the name column
CREATE INDEX idx_name_first ON names (name(1));