-- Fictional longitudinal outcomes for every prototype client.
PRAGMA foreign_keys = ON;

DELETE FROM gold_checkpoint_scores WHERE client_id BETWEEN 1001 AND 1006;

WITH eligible AS (
    SELECT c.client_id, g.checkpoint_id, g.checkpoint_number, d.dimension_id
    FROM clients c
    CROSS JOIN gold_checkpoint_periods g
    CROSS JOIN gold_dimensions d
    WHERE c.client_id BETWEEN 1001 AND 1006
      AND date(g.checkpoint_date) >= date(c.admission_date)
      AND (c.status <> 'Discharged' OR date(g.checkpoint_date) <= '2025-01-17')
), numbered AS (
    SELECT *, ROW_NUMBER() OVER (ORDER BY client_id, checkpoint_id, dimension_id) AS score_id
    FROM eligible
)
INSERT INTO gold_checkpoint_scores
    (score_id, client_id, dimension_id, checkpoint_id, score, source, imported_at)
SELECT score_id, client_id, dimension_id, checkpoint_id,
       MIN(12, 3 + checkpoint_number * 2 + ((dimension_id + client_id) % 3)),
       'Teaching Strategies GOLD', datetime('now')
FROM numbered;

DELETE FROM assessment_scores
WHERE administration_id IN (SELECT administration_id FROM assessment_administrations WHERE client_id BETWEEN 1001 AND 1006);
DELETE FROM assessment_administrations WHERE client_id BETWEEN 1001 AND 1006;

WITH admins AS (
    SELECT 7000 + ROW_NUMBER() OVER (ORDER BY c.client_id, t.assessment_type_id, n.visit_no) AS administration_id,
           c.client_id, t.assessment_type_id,
           date(c.admission_date, CASE WHEN n.visit_no=0 THEN '+0 day' WHEN n.visit_no=1 THEN '+30 day' ELSE '+180 day' END) AS assessment_date,
           n.visit_no
    FROM clients c
    CROSS JOIN (SELECT 10 AS assessment_type_id UNION ALL SELECT 20 UNION ALL SELECT 21 UNION ALL SELECT 22) t
    CROSS JOIN (SELECT 0 AS visit_no UNION ALL SELECT 1 UNION ALL SELECT 2) n
    WHERE c.client_id BETWEEN 1001 AND 1006
      AND date(c.admission_date, CASE WHEN n.visit_no=0 THEN '+0 day' WHEN n.visit_no=1 THEN '+30 day' ELSE '+180 day' END) <=
          CASE WHEN c.status='Discharged' THEN date('2025-01-17') ELSE date('2026-09-11') END
), inserted AS (
    SELECT * FROM admins
)
INSERT INTO assessment_administrations
    (administration_id, client_id, assessment_type_id, assessment_date, respondent, source, notes)
SELECT administration_id, client_id, assessment_type_id, assessment_date,
       CASE WHEN assessment_type_id IN (10,20,21) THEN 'Caregiver' ELSE 'Provider' END,
       'Placeholder Assessment', 'Fictional prototype data'
FROM inserted;

WITH admin_rows AS (
    SELECT aa.administration_id, aa.client_id, aa.assessment_type_id,
           ROW_NUMBER() OVER (ORDER BY aa.administration_id) AS admin_no
    FROM assessment_administrations aa
    WHERE aa.client_id BETWEEN 1001 AND 1006
), measures AS (
    SELECT a.administration_id, a.client_id, a.admin_no, m.measure_id
    FROM admin_rows a JOIN assessment_measures m
      ON m.assessment_type_id = a.assessment_type_id
)
INSERT INTO assessment_scores (assessment_score_id, administration_id, measure_id, score)
SELECT 8000 + ROW_NUMBER() OVER (ORDER BY administration_id, measure_id),
       administration_id, measure_id,
       MIN(95, 30 + ((client_id + measure_id + admin_no) * 7) % 55)
FROM measures;
