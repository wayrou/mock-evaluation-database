-- Fictional placeholder names for the prototype client list.
PRAGMA foreign_keys = ON;

UPDATE clients SET name = 'Joshua Norton' WHERE client_id = 1001;
UPDATE clients SET name = 'Mary Anning' WHERE client_id = 1002;
UPDATE clients SET name = 'Emmeline Pankhurst' WHERE client_id = 1003;
UPDATE clients SET name = 'Ada Lovelace' WHERE client_id = 1004;
UPDATE clients SET name = 'Lilian Bland' WHERE client_id = 1005;

INSERT OR IGNORE INTO clients (client_id, name, admission_date, status)
VALUES (1006, 'Deborah Sampson', '2026-05-01', 'Active');
