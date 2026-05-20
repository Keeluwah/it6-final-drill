CREATE DATABASE IF NOT EXISTS it6_final_drill;
USE it6_final_drill;

CREATE TABLE IF NOT EXISTS actors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    birth_year INT NOT NULL,
    nationality VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO actors (first_name, last_name, birth_year, nationality) VALUES
('Marlon', 'Brando', 1924, 'American'),
('Audrey', 'Hepburn', 1929, 'British'),
('Toshiro', 'Mifune', 1920, 'Japanese'),
('Nora', 'Aunor', 1953, 'Filipino'),
('Viola', 'Davis', 1965, 'American'),
('Daniel', 'Day-Lewis', 1957, 'British'),
('Lea', 'Salonga', 1971, 'Filipino'),
('Denzel', 'Washington', 1954, 'American'),
('Song', 'Kang-ho', 1967, 'South Korean'),
('Meryl', 'Streep', 1949, 'American'),
('Christopher', 'Plummer', 1929, 'Canadian'),
('Olivia', 'Colman', 1974, 'British'),
('Isabelle', 'Huppert', 1953, 'French'),
('Gael', 'Garcia Bernal', 1978, 'Mexican'),
('Irrfan', 'Khan', 1967, 'Indian'),
('Cate', 'Blanchett', 1969, 'Australian'),
('Tilda', 'Swinton', 1960, 'British'),
('Choi', 'Min-sik', 1962, 'South Korean'),
('Penelope', 'Cruz', 1974, 'Spanish'),
('Sid', 'Lucero', 1981, 'Filipino'),
('Ken', 'Watanabe', 1959, 'Japanese'),
('Saoirse', 'Ronan', 1994, 'Irish');

