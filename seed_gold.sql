PRAGMA foreign_keys = ON;

DELETE FROM gold_checkpoint_scores
WHERE client_id = 1001;

INSERT INTO gold_checkpoint_scores
(
    score_id,
    client_id,
    dimension_id,
    checkpoint_id,
    score,
    source,
    imported_at
)
VALUES
    (1, 1001, 1, 1, 4, 'Teaching Strategies GOLD', datetime('now')),
    (2, 1001, 2, 1, 4, 'Teaching Strategies GOLD', datetime('now')),
    (3, 1001, 3, 1, 5, 'Teaching Strategies GOLD', datetime('now')),
    (4, 1001, 4, 1, 5, 'Teaching Strategies GOLD', datetime('now')),
    (5, 1001, 5, 1, 4, 'Teaching Strategies GOLD', datetime('now')),
    (6, 1001, 6, 1, 3, 'Teaching Strategies GOLD', datetime('now')),
    (7, 1001, 7, 1, 5, 'Teaching Strategies GOLD', datetime('now')),
    (8, 1001, 8, 1, 4, 'Teaching Strategies GOLD', datetime('now')),

    (9, 1001, 1, 2, 6, 'Teaching Strategies GOLD', datetime('now')),
    (10, 1001, 2, 2, 6, 'Teaching Strategies GOLD', datetime('now')),
    (11, 1001, 3, 2, 6, 'Teaching Strategies GOLD', datetime('now')),
    (12, 1001, 4, 2, 7, 'Teaching Strategies GOLD', datetime('now')),
    (13, 1001, 5, 2, 6, 'Teaching Strategies GOLD', datetime('now')),
    (14, 1001, 6, 2, 5, 'Teaching Strategies GOLD', datetime('now')),
    (15, 1001, 7, 2, 6, 'Teaching Strategies GOLD', datetime('now')),
    (16, 1001, 8, 2, 6, 'Teaching Strategies GOLD', datetime('now')),

    (17, 1001, 1, 3, 8, 'Teaching Strategies GOLD', datetime('now')),
    (18, 1001, 2, 3, 8, 'Teaching Strategies GOLD', datetime('now')),
    (19, 1001, 3, 3, 8, 'Teaching Strategies GOLD', datetime('now')),
    (20, 1001, 4, 3, 8, 'Teaching Strategies GOLD', datetime('now')),
    (21, 1001, 5, 3, 7, 'Teaching Strategies GOLD', datetime('now')),
    (22, 1001, 6, 3, 7, 'Teaching Strategies GOLD', datetime('now')),
    (23, 1001, 7, 3, 8, 'Teaching Strategies GOLD', datetime('now')),
    (24, 1001, 8, 3, 7, 'Teaching Strategies GOLD', datetime('now')),

    (25, 1001, 1, 4, 9, 'Teaching Strategies GOLD', datetime('now')),
    (26, 1001, 2, 4, 9, 'Teaching Strategies GOLD', datetime('now')),
    (27, 1001, 3, 4, 9, 'Teaching Strategies GOLD', datetime('now')),
    (28, 1001, 4, 4, 9, 'Teaching Strategies GOLD', datetime('now')),
    (29, 1001, 5, 4, 8, 'Teaching Strategies GOLD', datetime('now')),
    (30, 1001, 6, 4, 8, 'Teaching Strategies GOLD', datetime('now')),
    (31, 1001, 7, 4, 9, 'Teaching Strategies GOLD', datetime('now')),
    (32, 1001, 8, 4, 8, 'Teaching Strategies GOLD', datetime('now'));