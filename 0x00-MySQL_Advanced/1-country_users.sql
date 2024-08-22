-- creating a table
-- considering constraints and ENUM datatype
CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    country ENUM('US', 'C0', 'TN') NOT NULL DEFAULT 'US'
);