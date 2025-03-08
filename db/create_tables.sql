DROP Table IF EXISTS pymes_trust;
CREATE TABLE IF NOT EXISTS pymes_trust (
                        id INT AUTO_INCREMENT PRIMARY KEY,  -- New column ID autoincremental as PK
                        ruc VARCHAR(13) NOT NULL UNIQUE,
                        pyme_name VARCHAR(35) NOT NULL,  -- This can be eliminated only for "academic purposes".
                        trust_score SMALLINT NOT NULL
);

DROP Table IF EXISTS mock_log_in;
CREATE TABLE IF NOT EXISTS mock_log_in (
                                     id INT AUTO_INCREMENT PRIMARY KEY,  -- New column ID autoincremental as PK
                                     ruc VARCHAR(50) NOT NULL UNIQUE,
                                     password VARCHAR(16) NOT NULL
#                                      password_hash VARCHAR(255) NOT NULL  -- Enable this when hashing algorithm is implemented
);

ALTER TABLE mock_log_in
    ADD FOREIGN KEY (ruc) REFERENCES pymes_trust(ruc);