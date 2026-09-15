-- Fictional, illustrative longitudinal data for the prototype.
PRAGMA foreign_keys = ON;

UPDATE clients SET admission_date='2023-09-11', status='Active' WHERE client_id=1001;
UPDATE clients SET admission_date='2025-06-16', status='Active' WHERE client_id=1002;
UPDATE clients SET admission_date='2024-01-08', status='Discharged' WHERE client_id=1003;
UPDATE clients SET admission_date='2026-03-05', status='Active' WHERE client_id=1004;
UPDATE clients SET admission_date='2026-08-18', status='Active' WHERE client_id=1005;
UPDATE clients SET admission_date='2026-09-02', status='Active' WHERE client_id=1006;

DELETE FROM client_programs WHERE client_id BETWEEN 1001 AND 1006;

INSERT OR IGNORE INTO client_programs VALUES
 (1001,1,'2023-09-11','2024-08-30'), (1001,2,'2024-09-03','2025-02-14'),
 (1001,1,'2025-02-18',NULL), (1002,3,'2025-06-16','2025-07-11'),
 (1002,2,'2025-07-14',NULL), (1003,1,'2024-01-08','2024-08-02'),
 (1003,2,'2024-08-05','2025-01-17'), (1004,1,'2026-03-05',NULL),
 (1005,3,'2026-08-18',NULL), (1006,2,'2026-09-02',NULL);

INSERT OR IGNORE INTO caregivers (caregiver_id,client_id,caregiver_name,relationship,primary_contact) VALUES
 (10,1001,'Eleanor Norton','Parent',1),(11,1001,'Thomas Norton','Parent',0),
 (12,1002,'Margaret Anning','Grandparent',1),(13,1003,'Helen Pankhurst','Parent',1),
 (14,1004,'Charles Lovelace','Parent',1),(15,1005,'Beatrice Bland','Guardian',1),
 (16,1006,'Sarah Sampson','Parent',1);

INSERT OR IGNORE INTO goals (goal_id,client_id,goal_text,goal_category,start_date,status,progress_percent) VALUES
 (101,1001,'Use coping strategies during transitions','Self-regulation','2023-09-11','In Progress',78),
 (102,1001,'Participate in peer activities twice weekly','Social skills','2024-09-03','Achieved',100),
 (103,1002,'Follow a visual routine with one prompt','Daily living','2025-07-14','In Progress',55),
 (104,1003,'Practice safe communication at home','Communication','2024-01-08','Completed',100),
 (105,1004,'Remain engaged in structured activities for 15 minutes','Attention','2026-03-05','In Progress',35),
 (106,1005,'Identify two trusted adults','Safety','2026-08-18','In Progress',20),
 (107,1006,'Complete intake and establish treatment goals','Care planning','2026-09-02','Pending',5);

INSERT OR IGNORE INTO services (service_id,client_id,staff_id,service_type,service_date,duration_minutes) VALUES
 (101,1002,2,'Case Management','2025-07-15',45),(102,1002,1,'Individual Therapy','2025-07-22',50),
 (103,1003,3,'Family Therapy','2024-02-01',60),(104,1003,1,'Individual Therapy','2024-03-12',50),
 (105,1004,2,'Case Management','2026-03-06',30),(106,1004,1,'Individual Therapy','2026-03-13',45),
 (107,1005,2,'Intake Coordination','2026-08-19',45),(108,1005,3,'Family Therapy','2026-08-26',60),
 (109,1006,2,'Intake Coordination','2026-09-03',30),(110,1006,1,'Individual Therapy','2026-09-09',45);

-- A small but varied attendance history for each client.
INSERT OR IGNORE INTO attendance (attendance_id,client_id,attendance_date,attendance_code,notes) VALUES
 (301,1001,'2023-09-12','P',NULL),(302,1001,'2024-01-18','03','Routine appointment'),(303,1001,'2025-06-04','P',NULL),(304,1001,'2026-09-08','P',NULL),
 (305,1002,'2025-06-17','P',NULL),(306,1002,'2025-07-03','05','Reported illness'),(307,1002,'2026-09-04','P',NULL),
 (308,1003,'2024-01-09','P',NULL),(309,1003,'2024-07-22','P',NULL),(310,1003,'2025-01-17','DC','Program discharge'),
 (311,1004,'2026-03-06','P',NULL),(312,1004,'2026-04-02','NT','No transportation'),(313,1004,'2026-09-07','P',NULL),
 (314,1005,'2026-08-19','P',NULL),(315,1005,'2026-08-28','03','Routine appointment'),
 (316,1006,'2026-09-03','P',NULL),(317,1006,'2026-09-09','P',NULL);

INSERT OR IGNORE INTO meals (meal_id,client_id,service_date,meal_type,served,notes) VALUES
 (401,1002,'2025-07-15','Breakfast',1,NULL),(402,1002,'2025-07-15','Lunch',1,NULL),
 (403,1003,'2024-03-12','Lunch',1,NULL),(404,1004,'2026-03-13','Snack',1,NULL),
 (405,1005,'2026-08-19','Breakfast',1,NULL),(406,1006,'2026-09-03','Lunch',1,NULL);
