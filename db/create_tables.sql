DROP Table IF EXISTS mock_log_in;
CREATE TABLE IF NOT EXISTS mock_log_in (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL UNIQUE,
    password VARCHAR(16) NOT NULL
#     password_hash VARCHAR(255) NOT NULL  -- Enable this if hashing algorithm is implemented
);

DROP Table IF EXISTS pymes_trust;
CREATE TABLE IF NOT EXISTS pymes_trust (
                                           id INT AUTO_INCREMENT PRIMARY KEY,
                                           ruc VARCHAR(13) NOT NULL UNIQUE,
                                           pyme_name VARCHAR(35) NOT NULL,
                                           trust_score SMALLINT DEFAULT 0,
                                           tier ENUM( 'N/A', 'Plata', 'Oro', 'Platino') DEFAULT 'N/A'
);

ALTER TABLE mock_log_in
    ADD FOREIGN KEY (ruc) REFERENCES pymes_trust(ruc);