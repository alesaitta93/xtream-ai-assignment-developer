CREATE DATABASE diamonds_db;

USE diamonds_db;

CREATE TABLE log_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    request_url VARCHAR(2048),
    response_json JSON,
    carat FLOAT,
    cut VARCHAR(10),
    color VARCHAR(1),
    clarity VARCHAR(4),
    depth FLOAT,
    tab FLOAT,
    x FLOAT,
    y FLOAT,
    z FLOAT
);

CREATE TABLE log_similarities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    request_url VARCHAR(2048),
    response_json JSON,
    n INTEGER,
    carat FLOAT,
    cut VARCHAR(10),
    color VARCHAR(1),
    clarity VARCHAR(4)
);