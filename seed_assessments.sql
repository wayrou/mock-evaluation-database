-- Fictional placeholder assessment data for the prototype dashboard.
PRAGMA foreign_keys = ON;

INSERT OR IGNORE INTO assessment_types
    (assessment_type_id, assessment_name, score_min, score_max, improvement_direction)
VALUES
    (20, 'ASQ:SE-2', 0, 100, 'lower'),
    (21, 'PSC-17', 0, 100, 'lower'),
    (22, 'Developmental Snapshot', 0, 100, 'higher');

INSERT OR IGNORE INTO assessment_measures
    (measure_id, assessment_type_id, measure_name, score_min, score_max, improvement_direction)
VALUES
    (201, 20, 'Social-Emotional Total', 0, 100, 'lower'),
    (202, 20, 'Self-Regulation', 0, 100, 'higher'),
    (211, 21, 'Attention Problems', 0, 100, 'lower'),
    (212, 21, 'Externalizing Problems', 0, 100, 'lower'),
    (213, 21, 'Internalizing Problems', 0, 100, 'lower'),
    (221, 22, 'Communication', 0, 100, 'higher'),
    (222, 22, 'Problem Solving', 0, 100, 'higher'),
    (223, 22, 'Personal-Social Skills', 0, 100, 'higher');

INSERT OR IGNORE INTO assessment_administrations
    (administration_id, client_id, assessment_type_id, assessment_date, respondent, source, notes)
VALUES
    (6001, 1001, 20, '2026-01-20', 'Caregiver', 'Placeholder Assessment', 'Fictional prototype data'),
    (6002, 1001, 20, '2026-07-20', 'Caregiver', 'Placeholder Assessment', 'Fictional prototype data'),
    (6011, 1001, 21, '2026-02-01', 'Caregiver', 'Placeholder Assessment', 'Fictional prototype data'),
    (6012, 1001, 21, '2026-08-01', 'Caregiver', 'Placeholder Assessment', 'Fictional prototype data'),
    (6021, 1001, 22, '2026-02-10', 'Provider', 'Placeholder Assessment', 'Fictional prototype data'),
    (6022, 1001, 22, '2026-08-10', 'Provider', 'Placeholder Assessment', 'Fictional prototype data');

INSERT OR IGNORE INTO assessment_scores
    (assessment_score_id, administration_id, measure_id, score)
VALUES
    (201, 6001, 201, 62), (202, 6001, 202, 41),
    (203, 6002, 201, 44), (204, 6002, 202, 68),
    (211, 6011, 211, 58), (212, 6011, 212, 52), (213, 6011, 213, 47),
    (214, 6012, 211, 36), (215, 6012, 212, 33), (216, 6012, 213, 31),
    (221, 6021, 221, 48), (222, 6021, 222, 44), (223, 6021, 223, 51),
    (224, 6022, 221, 71), (225, 6022, 222, 67), (226, 6022, 223, 74);
