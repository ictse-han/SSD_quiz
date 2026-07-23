-- Q4(e): table for the common/breached password blocklist
CREATE TABLE IF NOT EXISTS common_passwords (
    password TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_common_passwords_password ON common_passwords (password);

-- Q4(i): log created users here -- username + creation time only, no password stored.
-- Table is named after the student ID, so it must be double-quoted (starts with a digit).
CREATE TABLE IF NOT EXISTS "2301483" (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
