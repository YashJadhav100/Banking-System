CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    balance NUMERIC DEFAULT 1000
);

CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    from_user TEXT,
    to_user TEXT,
    amount NUMERIC,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample users
INSERT INTO users (username, balance) VALUES
('alice', 1000),
('bob', 1000),
('charlie', 1000);
