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
    pyme_name VARCHAR(250) NOT NULL,
    trust_score TINYINT  DEFAULT 0,
    tier ENUM( 'N/A', 'Plata', 'Oro', 'Platino') DEFAULT 'N/A'
    tier ENUM( 'N/A', 'Plata', 'Oro', 'Platino') DEFAULT 'N/A',
    next_tier TINYINT  DEFAULT 0
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
-- pymes_certificates table - a pyme can have many certificates
DROP Table IF EXISTS pymes_certificates;
CREATE TABLE IF NOT EXISTS pymes_certificates (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL UNIQUE,
    iess_compliance Boolean DEFAULT FALSE,
    sri_compliance Boolean DEFAULT FALSE,
    credit_score TINYINT DEFAULT 0,
    next_tier TINYINT  DEFAULT 0,
    certificate_name VARCHAR(250) NOT NULL,
    issuer VARCHAR(250) NOT NULL,
    issue_date DATE,
    expiration_date DATE
);

-- pymes_trust_score_peers
DROP Table IF EXISTS peer_pymes_trust_scores;
CREATE TABLE IF NOT EXISTS peer_pymes_trust_scores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    score_issuer VARCHAR(13) NOT NULL UNIQUE,
    score_receiver VARCHAR(13) DEFAULT FALSE,
    peer_trust_score TINYINT DEFAULT 0,
    peer_trust_score TINYINT DEFAULT 0
);

-- Table for PyME Connections
DROP Table IF EXISTS pyme_connections;
CREATE TABLE IF NOT EXISTS pyme_connections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    requester_ruc VARCHAR(13) NOT NULL,
    receiver_ruc VARCHAR(13) NOT NULL,
    status ENUM('Pending', 'Accepted', 'Rejected') DEFAULT 'Pending',
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    accepted_at TIMESTAMP NULL DEFAULT NULL,
    UNIQUE(requester_ruc, receiver_ruc) -- Avoid duplicate requests
);

DROP TABLE IF EXISTS credit_options;
CREATE TABLE IF NOT EXISTS credit_options (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    amount VARCHAR(50) NOT NULL,
    interest_rate VARCHAR(20) NOT NULL,
    term VARCHAR(50) NOT NULL,
    requirements VARCHAR(100) NOT NULL,
    recommended BOOLEAN DEFAULT FALSE,
    link VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS pyme_credits;
CREATE TABLE IF NOT EXISTS pyme_credits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ruc VARCHAR(13) NOT NULL,
    credit_type_id INT NOT NULL,
    amount_approved BIGINT NOT NULL,
    interest_rate FLOAT NOT NULL,
    term INT NOT NULL, -- Term in months
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    progress_percentage TINYINT DEFAULT 0 CHECK (progress_percentage BETWEEN 0 AND 100),
    status ENUM('Active', 'Completed', 'Cancelled') DEFAULT 'Active'
);