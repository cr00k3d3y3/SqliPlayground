DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    password VARCHAR(100),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    content TEXT
);

INSERT INTO users (username, password, email) VALUES 
('admin', 'admin123', 'admin@example.com'),
('steveee79', 'ThE$qU!rR3L', 'steve@example.com'),
('jdoe', 'qwerty123', 'john.doe@example.com'),
('alice', 'alicePass!', 'alice@example.com'),
('bob', 'bobSecure2025', 'bob@example.com'),
('eve', 'ev3_hackz', 'eve@example.com'),
('carol', 'carolPass@321', 'carol@example.com'),
('mallory', 'm@llory!', 'mallory@example.com'),
('trent', 'tr3ntPass!', 'trent@example.com'),
('peggy', 'peggyRocks', 'peggy@example.com');
