-- mock_log_in table is a mock table to simulate a log in table
DROP Table IF EXISTS mock_log_in;
CREATE TABLE IF NOT EXISTS mock_log_in (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL UNIQUE,
    password VARCHAR(16) NOT NULL
);

-- pymes_trust table has the score given by BG to the companies
DROP Table IF EXISTS pymes_trust;
CREATE TABLE IF NOT EXISTS pymes_trust (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL UNIQUE,
    pyme_name VARCHAR(250) NOT NULL, -- ToDo - delete this ?
    trust_score TINYINT  DEFAULT 0,
    tier ENUM( 'N/A', 'Plata', 'Oro', 'Platino') DEFAULT 'N/A'
);

-- mock_pymes table has data of the PyMEs
-- Mock data created using https://www.kaggle.com/datasets/carlosmmuozebratt/pymes-smbs-in-bolvar-colombia
DROP Table IF EXISTS mock_pymes;
CREATE TABLE IF NOT EXISTS mock_pymes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL UNIQUE,
    person_type ENUM('Jurídica', 'Natural'),
    business_type VARCHAR(50) NOT NULL,
    pyme_name VARCHAR(250) NOT NULL,
    province VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    division VARCHAR(350),
    section VARCHAR(350),
    est_date DATE,
    total_assets BIGINT,
    size ENUM('Mediana', 'Pequeña')
);

-- pymes_certificates table has goals progress of each PyME
DROP Table IF EXISTS pymes_certificates;
CREATE TABLE IF NOT EXISTS pymes_certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL UNIQUE,
    iess_compliance Boolean DEFAULT FALSE,
    sri_compliance Boolean DEFAULT FALSE,
    credit_score TINYINT DEFAULT 0,
    next_tier TINYINT  DEFAULT 0,
    FOREIGN KEY (ruc) REFERENCES mock_pymes(ruc)
);

-- pymes_trust_score_peers
DROP Table IF EXISTS peer_pymes_trust_scores;
CREATE TABLE IF NOT EXISTS peer_pymes_trust_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    score_issuer VARCHAR(13) NOT NULL UNIQUE,
    score_receiver VARCHAR(13) DEFAULT FALSE,
    peer_trust_score TINYINT DEFAULT 0,
    FOREIGN KEY (score_issuer) REFERENCES mock_pymes(ruc),
    FOREIGN KEY (score_receiver) REFERENCES mock_pymes(ruc)
);