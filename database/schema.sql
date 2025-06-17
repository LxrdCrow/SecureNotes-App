CREATE TABLE notes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title TEXT NOT NULL,        -- criptato
    content TEXT NOT NULL,      -- criptato
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE settings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    theme VARCHAR(50) DEFAULT 'light',
    language VARCHAR(50) DEFAULT 'en'
);

CREATE TABLE master_key (
    id INT PRIMARY KEY AUTO_INCREMENT,
    password_hash TEXT NOT NULL
);

CREATE TABLE encryption_keys (
    id INT PRIMARY KEY AUTO_INCREMENT,
    key_data TEXT NOT NULL,  -- criptato o codificato
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    action VARCHAR(255) NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);





