-- Demonstration schema and synthetic examples only.
-- Review before running. This does not contain the original RiceStressDB records.
CREATE DATABASE IF NOT EXISTS rice_stress_demo;
USE rice_stress_demo;

CREATE TABLE IF NOT EXISTS gene (
  gene_id VARCHAR(64) PRIMARY KEY,
  gene_symbol VARCHAR(128),
  annotation TEXT
);

CREATE TABLE IF NOT EXISTS stress_condition (
  condition_id INT PRIMARY KEY,
  condition_name VARCHAR(128) NOT NULL,
  stress_type ENUM('biotic','abiotic') NOT NULL
);

CREATE TABLE IF NOT EXISTS gene_expression (
  gene_id VARCHAR(64) NOT NULL,
  condition_id INT NOT NULL,
  expression_value DECIMAL(12,4),
  measurement_unit VARCHAR(32) DEFAULT 'normalized_value',
  PRIMARY KEY (gene_id, condition_id),
  FOREIGN KEY (gene_id) REFERENCES gene(gene_id),
  FOREIGN KEY (condition_id) REFERENCES stress_condition(condition_id)
);

INSERT INTO gene (gene_id, gene_symbol, annotation) VALUES
('EXAMPLE_GENE_001', 'EXAMPLE1', 'Synthetic example record; replace with authorized annotation'),
('EXAMPLE_GENE_002', 'EXAMPLE2', 'Synthetic example record; replace with authorized annotation')
ON DUPLICATE KEY UPDATE gene_symbol=VALUES(gene_symbol), annotation=VALUES(annotation);

INSERT INTO stress_condition (condition_id, condition_name, stress_type) VALUES
(1, 'Example drought condition', 'abiotic'),
(2, 'Example pathogen challenge', 'biotic')
ON DUPLICATE KEY UPDATE condition_name=VALUES(condition_name), stress_type=VALUES(stress_type);

INSERT INTO gene_expression (gene_id, condition_id, expression_value) VALUES
('EXAMPLE_GENE_001', 1, 1.2500),
('EXAMPLE_GENE_001', 2, 0.7500),
('EXAMPLE_GENE_002', 1, 2.1000),
('EXAMPLE_GENE_002', 2, 1.0500)
ON DUPLICATE KEY UPDATE expression_value=VALUES(expression_value);
