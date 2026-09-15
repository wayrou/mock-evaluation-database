-- Fictional, illustrative data only. Names are borrowed from historical figures;
-- all enrollment, caregiver, service, attendance, and outcome details are invented.
-- Run after the existing schema and seed files.
PRAGMA foreign_keys = ON;

CREATE TEMP TABLE historical_client_seed (
    client_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    admission_date TEXT NOT NULL,
    status TEXT NOT NULL,
    discharge_date TEXT,
    caregiver_name TEXT NOT NULL,
    relationship TEXT NOT NULL,
    program_id INTEGER NOT NULL
);

INSERT INTO historical_client_seed VALUES
 (1007,'Harriet Tubman','2023-10-02','Active',NULL,'Rosa Parks','Parent',1),
 (1008,'Katherine Johnson','2023-11-13','Active',NULL,'Dorothy Vaughan','Parent',1),
 (1009,'George Washington Carver','2024-01-22','Discharged','2024-10-18','Booker T. Washington','Guardian',1),
 (1010,'Ida B. Wells','2024-02-12','Active',NULL,'Mary Church Terrell','Parent',2),
 (1011,'Cesar Chavez','2024-03-18','Discharged','2025-02-14','Dolores Huerta','Parent',1),
 (1012,'Frida Kahlo','2024-04-08','Active',NULL,'Georgia O''Keeffe','Parent',2),
 (1013,'Alan Turing','2024-05-20','Active',NULL,'Joan Clarke','Guardian',1),
 (1014,'Maya Angelou','2024-06-10','Discharged','2025-01-10','Toni Morrison','Parent',2),
 (1015,'Nikola Tesla','2024-07-15','Active',NULL,'Thomas Edison','Parent',1),
 (1016,'Shirley Chisholm','2024-08-05','Active',NULL,'Barbara Jordan','Parent',2),
 (1017,'Louis Armstrong','2024-09-09','Discharged','2025-05-23','Duke Ellington','Grandparent',1),
 (1018,'Grace Hopper','2024-10-14','Active',NULL,'Annie Easley','Parent',1),
 (1019,'James Baldwin','2024-11-04','Active',NULL,'Langston Hughes','Guardian',2),
 (1020,'Rachel Carson','2024-12-02','Discharged','2025-07-18','Jane Goodall','Parent',1),
 (1021,'Wangari Maathai','2025-01-13','Active',NULL,'Ellen Johnson Sirleaf','Parent',2),
 (1022,'Srinivasa Ramanujan','2025-02-03','Active',NULL,'C. V. Raman','Parent',1),
 (1023,'Eleanor Roosevelt','2025-02-24','Discharged','2025-11-21','Frances Perkins','Grandparent',1),
 (1024,'Amelia Earhart','2025-03-17','Active',NULL,'Bessie Coleman','Parent',2),
 (1025,'Frederick Douglass','2025-04-07','Active',NULL,'Sojourner Truth','Guardian',1),
 (1026,'Marie Curie','2025-04-28','Discharged','2026-01-16','Lise Meitner','Parent',2),
 (1027,'Nelson Mandela','2025-05-19','Active',NULL,'Desmond Tutu','Parent',1),
 (1028,'Susan B. Anthony','2025-06-09','Active',NULL,'Elizabeth Cady Stanton','Parent',2),
 (1029,'Thurgood Marshall','2025-06-30','Discharged','2026-02-27','Pauli Murray','Guardian',1),
 (1030,'Sally Ride','2025-07-21','Active',NULL,'Mae Jemison','Parent',1),
 (1031,'Leonardo da Vinci','2025-08-11','Active',NULL,'Galileo Galilei','Parent',2),
 (1032,'Mary Seacole','2025-09-08','Active',NULL,'Florence Nightingale','Parent',1),
 (1033,'Martin Luther King Jr.','2025-09-29','Discharged','2026-03-20','Coretta Scott King','Parent',1),
 (1034,'Hedy Lamarr','2025-10-20','Active',NULL,'Marlene Dietrich','Guardian',2),
 (1035,'Benjamin Banneker','2025-11-10','Active',NULL,'Olaudah Equiano','Parent',1),
 (1036,'Jane Addams','2025-12-01','Active',NULL,'Lillian Wald','Parent',2),
 (1037,'Pablo Picasso','2026-01-12','Active',NULL,'Diego Rivera','Parent',1),
 (1038,'Simone Biles','2026-02-02','Active',NULL,'Alice Coachman','Parent',2),
 (1039,'Duke Kahanamoku','2026-02-23','Active',NULL,'Jesse Owens','Guardian',1),
 (1040,'Hypatia of Alexandria','2026-03-16','Active',NULL,'Theon of Alexandria','Parent',2),
 (1041,'Gabriela Mistral','2026-04-06','Active',NULL,'Sor Juana Inés de la Cruz','Parent',1),
 (1042,'Sun Yat-sen','2026-04-27','Active',NULL,'Qiu Jin','Guardian',1),
 (1043,'Rosa Parks','2026-05-18','Active',NULL,'Claudette Colvin','Parent',2),
 (1044,'Vera Rubin','2026-06-08','Active',NULL,'Cecilia Payne-Gaposchkin','Parent',1),
 (1045,'Oscar Romero','2026-06-29','Active',NULL,'Dorothy Day','Parent',2),
 (1046,'Octavia Butler','2026-07-20','Active',NULL,'N. K. Jemisin','Guardian',1),
 (1047,'Ibn Sina','2026-08-03','Active',NULL,'Al-Razi','Parent',1),
 (1048,'Sacagawea','2026-08-17','Active',NULL,'Sarah Winnemucca','Parent',2),
 (1049,'Malala Yousafzai','2026-08-31','Active',NULL,'Fatima al-Fihri','Parent',1),
 (1050,'Yuri Gagarin','2026-09-07','Active',NULL,'Valentina Tereshkova','Parent',3);

INSERT OR IGNORE INTO clients (client_id, name, admission_date, status)
SELECT client_id, name, admission_date, status FROM historical_client_seed;

INSERT OR IGNORE INTO caregivers
    (caregiver_id, client_id, caregiver_name, relationship, primary_contact)
SELECT 100 + client_id - 1007, client_id, caregiver_name, relationship, 1
FROM historical_client_seed;

-- Day-treatment clients generally transition to outpatient care after a sustained episode.
INSERT OR IGNORE INTO client_programs (client_id, program_id, start_date, end_date)
SELECT client_id, program_id, admission_date,
       CASE WHEN program_id = 1 THEN date(admission_date, '+180 day')
            WHEN status = 'Discharged' THEN discharge_date END
FROM historical_client_seed;

INSERT OR IGNORE INTO client_programs (client_id, program_id, start_date, end_date)
SELECT client_id, 2, date(admission_date, '+181 day'),
       CASE WHEN status = 'Discharged' THEN discharge_date ELSE NULL END
FROM historical_client_seed
WHERE program_id = 1 AND date(admission_date, '+181 day') <= COALESCE(discharge_date, '2026-09-11');

INSERT OR IGNORE INTO goals
    (goal_id, client_id, goal_text, goal_category, start_date, status, progress_percent)
SELECT 2000 + (client_id - 1007) * 2, client_id,
       CASE (client_id - 1007) % 5
           WHEN 0 THEN 'Use a practiced coping strategy during changes in routine'
           WHEN 1 THEN 'Follow a visual schedule with decreasing adult prompts'
           WHEN 2 THEN 'Participate in a structured peer activity each week'
           WHEN 3 THEN 'Communicate needs using an agreed-upon support strategy'
           ELSE 'Remain engaged in a preferred and non-preferred activity for 15 minutes'
       END,
       CASE (client_id - 1007) % 5
           WHEN 0 THEN 'Self-regulation' WHEN 1 THEN 'Daily living' WHEN 2 THEN 'Social skills'
           WHEN 3 THEN 'Communication' ELSE 'Attention' END,
       admission_date,
       CASE WHEN status = 'Discharged' THEN 'Completed' ELSE 'In Progress' END,
       CASE WHEN status = 'Discharged' THEN 100 ELSE 35 + ((client_id - 1007) * 9) % 55 END
FROM historical_client_seed;

INSERT OR IGNORE INTO goals
    (goal_id, client_id, goal_text, goal_category, start_date, status, progress_percent)
SELECT 2001 + (client_id - 1007) * 2, client_id,
       'Caregiver will review progress and practice the home support plan monthly',
       'Care coordination', date(admission_date, '+30 day'),
       CASE WHEN status = 'Discharged' THEN 'Completed' ELSE 'In Progress' END,
       CASE WHEN status = 'Discharged' THEN 100 ELSE 45 + ((client_id - 1007) * 7) % 45 END
FROM historical_client_seed;

-- Core encounters document intake, a 30-day review, and a later progress review.
INSERT OR IGNORE INTO services
    (service_id, client_id, staff_id, service_type, service_date, duration_minutes)
SELECT 3000 + (client_id - 1007) * 3, client_id, 2, 'Intake Coordination', admission_date, 45
FROM historical_client_seed;

INSERT OR IGNORE INTO services
    (service_id, client_id, staff_id, service_type, service_date, duration_minutes)
SELECT 3001 + (client_id - 1007) * 3, client_id,
       CASE WHEN (client_id - 1007) % 3 = 0 THEN 3 ELSE 1 END,
       CASE WHEN (client_id - 1007) % 3 = 0 THEN 'Family Therapy' ELSE 'Individual Therapy' END,
       date(admission_date, '+30 day'),
       CASE WHEN (client_id - 1007) % 3 = 0 THEN 60 ELSE 50 END
FROM historical_client_seed
WHERE date(admission_date, '+30 day') <= COALESCE(discharge_date, '2026-09-11');

INSERT OR IGNORE INTO services
    (service_id, client_id, staff_id, service_type, service_date, duration_minutes)
SELECT 3002 + (client_id - 1007) * 3, client_id, 2, 'Case Management',
       date(admission_date, '+120 day'), 45
FROM historical_client_seed
WHERE date(admission_date, '+120 day') <= COALESCE(discharge_date, '2026-09-11');

-- Weekly scheduled attendance, with occasional believable excused absences.
WITH RECURSIVE attendance_dates(client_id, attendance_date, end_date, visit_no) AS (
    SELECT client_id, admission_date, COALESCE(discharge_date, '2026-09-11'), 1
    FROM historical_client_seed
    UNION ALL
    SELECT client_id, date(attendance_date, '+7 day'), end_date, visit_no + 1
    FROM attendance_dates WHERE date(attendance_date, '+7 day') <= end_date
)
INSERT OR IGNORE INTO attendance (attendance_id, client_id, attendance_date, attendance_code, notes)
SELECT 20000 + ROW_NUMBER() OVER (ORDER BY client_id, attendance_date), client_id, attendance_date,
       CASE WHEN visit_no % 17 = 0 THEN 'NT'
            WHEN visit_no % 13 = 0 THEN '05'
            WHEN visit_no % 11 = 0 THEN '03'
            WHEN visit_no % 29 = 0 THEN '04'
            ELSE 'P' END,
       CASE WHEN visit_no % 17 = 0 THEN 'No transportation reported'
            WHEN visit_no % 13 = 0 THEN 'Reported illness'
            WHEN visit_no % 11 = 0 THEN 'Routine appointment'
            WHEN visit_no % 29 = 0 THEN 'Family visit'
            ELSE NULL END
FROM attendance_dates;

INSERT OR IGNORE INTO meals (meal_id, client_id, service_date, meal_type, served, notes)
SELECT 1000 + ROW_NUMBER() OVER (ORDER BY client_id), client_id, date(admission_date, '+14 day'),
       CASE WHEN program_id = 1 THEN 'Lunch' ELSE 'Snack' END, 1, NULL
FROM historical_client_seed
WHERE date(admission_date, '+14 day') <= COALESCE(discharge_date, '2026-09-11');

-- Three assessment administrations provide a modest baseline-to-follow-up history.
WITH assessment_visits AS (
    SELECT client_id, admission_date, status, discharge_date, 0 AS visit_no FROM historical_client_seed
    UNION ALL SELECT client_id, admission_date, status, discharge_date, 1 FROM historical_client_seed
    UNION ALL SELECT client_id, admission_date, status, discharge_date, 2 FROM historical_client_seed
), eligible AS (
    SELECT v.client_id, t.assessment_type_id, v.visit_no,
           date(v.admission_date, CASE v.visit_no WHEN 0 THEN '+7 day' WHEN 1 THEN '+90 day' ELSE '+180 day' END) AS assessment_date
    FROM assessment_visits v
    CROSS JOIN (SELECT 20 AS assessment_type_id UNION ALL SELECT 21 UNION ALL SELECT 22) t
    WHERE date(v.admission_date, CASE v.visit_no WHEN 0 THEN '+7 day' WHEN 1 THEN '+90 day' ELSE '+180 day' END)
          <= COALESCE(v.discharge_date, '2026-09-11')
)
INSERT OR IGNORE INTO assessment_administrations
    (administration_id, client_id, assessment_type_id, assessment_date, respondent, source, notes)
SELECT 9000 + ROW_NUMBER() OVER (ORDER BY client_id, assessment_type_id, visit_no),
       client_id, assessment_type_id, assessment_date,
       CASE WHEN assessment_type_id IN (20,21) THEN 'Caregiver' ELSE 'Provider' END,
       'Mock EHR', 'Fictional prototype data'
FROM eligible;

INSERT OR IGNORE INTO assessment_scores (assessment_score_id, administration_id, measure_id, score)
SELECT 12000 + ROW_NUMBER() OVER (ORDER BY aa.administration_id, am.measure_id),
       aa.administration_id, am.measure_id,
       CASE WHEN am.improvement_direction = 'lower'
              THEN MAX(8, 67 - ((aa.client_id + am.measure_id) % 20) - ((aa.administration_id - 9000) % 3) * 8)
            ELSE MIN(92, 35 + ((aa.client_id + am.measure_id) % 25) + ((aa.administration_id - 9000) % 3) * 9)
       END
FROM assessment_administrations aa
JOIN assessment_measures am ON am.assessment_type_id = aa.assessment_type_id
WHERE aa.client_id BETWEEN 1007 AND 1050;

-- GOLD checkpoints are included only when the client was enrolled on the checkpoint date.
WITH eligible AS (
    SELECT h.client_id, h.admission_date, gp.checkpoint_id, gp.checkpoint_number, gd.dimension_id
    FROM historical_client_seed h
    CROSS JOIN gold_checkpoint_periods gp
    CROSS JOIN gold_dimensions gd
    WHERE date(gp.checkpoint_date) >= date(h.admission_date)
      AND date(gp.checkpoint_date) <= COALESCE(h.discharge_date, '2026-09-11')
)
INSERT OR IGNORE INTO gold_checkpoint_scores
    (score_id, client_id, dimension_id, checkpoint_id, score, source, imported_at)
SELECT 2000 + ROW_NUMBER() OVER (ORDER BY client_id, checkpoint_id, dimension_id),
       client_id, dimension_id, checkpoint_id,
       MIN(13, 3 + checkpoint_number * 2 + ((client_id + dimension_id) % 4)),
       'Teaching Strategies GOLD', datetime('now')
FROM eligible;

DROP TABLE historical_client_seed;
