PRAGMA foreign_keys = ON;


-- =========================================================
-- TEACHING STRATEGIES GOLD DIMENSIONS
-- Representative full classroom-development structure
-- based on the objectives currently being modeled.
-- =========================================================


-- ---------------------------------------------------------
-- SOCIAL-EMOTIONAL
-- ---------------------------------------------------------

INSERT OR IGNORE INTO gold_dimensions
    (dimension_id, dimension_code, domain, dimension_name, score_min, score_max)
VALUES
    (1, '1a', 'Social-Emotional', 'Manages feelings', 0, 13),
    (2, '1b', 'Social-Emotional', 'Follows limits and expectations', 0, 13),
    (3, '1c', 'Social-Emotional', 'Takes care of own needs appropriately', 0, 13),
    (4, '2a', 'Social-Emotional', 'Forms relationships with adults', 0, 13),
    (5, '2b', 'Social-Emotional', 'Responds to emotional cues', 0, 13),
    (6, '2c', 'Social-Emotional', 'Interacts with peers', 0, 13),
    (9, '2d', 'Social-Emotional', 'Makes friends', 0, 13),
    (10, '3a', 'Social-Emotional', 'Balances needs and rights of self and others', 0, 13),
    (11, '3b', 'Social-Emotional', 'Solves social problems', 0, 13);


-- ---------------------------------------------------------
-- PHYSICAL
-- ---------------------------------------------------------

INSERT OR IGNORE INTO gold_dimensions
    (dimension_id, dimension_code, domain, dimension_name, score_min, score_max)
VALUES
    (12, '4', 'Physical', 'Demonstrates traveling skills', 0, 13),
    (13, '5', 'Physical', 'Demonstrates balancing skills', 0, 13),
    (14, '6', 'Physical', 'Demonstrates gross-motor manipulative skills', 0, 13),
    (15, '7a', 'Physical', 'Uses fingers and hands', 0, 13),
    (16, '7b', 'Physical', 'Uses writing and drawing tools', 0, 13);


-- ---------------------------------------------------------
-- LANGUAGE
-- ---------------------------------------------------------

INSERT OR IGNORE INTO gold_dimensions
    (dimension_id, dimension_code, domain, dimension_name, score_min, score_max)
VALUES
    (7, '8a', 'Language', 'Comprehends language', 0, 13),
    (17, '8b', 'Language', 'Follows directions', 0, 13),
    (8, '9a', 'Language', 'Uses an expanding expressive vocabulary', 0, 13),
    (18, '9b', 'Language', 'Speaks clearly', 0, 13),
    (19, '9c', 'Language', 'Uses conventional grammar', 0, 13),
    (20, '9d', 'Language', 'Tells about another time or place', 0, 13),
    (21, '10a', 'Language', 'Engages in conversations', 0, 13),
    (22, '10b', 'Language', 'Uses social rules of language', 0, 13);


-- ---------------------------------------------------------
-- COGNITIVE
-- ---------------------------------------------------------

INSERT OR IGNORE INTO gold_dimensions
    (dimension_id, dimension_code, domain, dimension_name, score_min, score_max)
VALUES
    (23, '11a', 'Cognitive', 'Attends and engages', 0, 13),
    (24, '11b', 'Cognitive', 'Persists', 0, 13),
    (25, '11c', 'Cognitive', 'Solves problems', 0, 13),
    (26, '11d', 'Cognitive', 'Shows curiosity and motivation', 0, 13),
    (27, '11e', 'Cognitive', 'Shows flexibility and inventiveness in thinking', 0, 13),
    (28, '12a', 'Cognitive', 'Recognizes and recalls', 0, 13),
    (29, '12b', 'Cognitive', 'Makes connections', 0, 13),
    (30, '13', 'Cognitive', 'Uses classification skills', 0, 13),
    (31, '14a', 'Cognitive', 'Thinks symbolically', 0, 13),
    (32, '14b', 'Cognitive', 'Engages in sociodramatic play', 0, 13);


-- ---------------------------------------------------------
-- LITERACY
-- ---------------------------------------------------------

INSERT OR IGNORE INTO gold_dimensions
    (dimension_id, dimension_code, domain, dimension_name, score_min, score_max)
VALUES
    (33, '15a', 'Literacy', 'Notices and discriminates rhyme', 0, 13),
    (34, '15b', 'Literacy', 'Notices and discriminates alliteration', 0, 13),
    (35, '15c', 'Literacy', 'Notices and discriminates discrete units of sound', 0, 13),
    (36, '15d', 'Literacy', 'Applies phonics concepts and knowledge of word structure', 0, 13),
    (37, '16a', 'Literacy', 'Identifies and names letters', 0, 13),
    (38, '16b', 'Literacy', 'Identifies letter-sound correspondences', 0, 13),
    (39, '17a', 'Literacy', 'Uses and appreciates books and other texts', 0, 13),
    (40, '17b', 'Literacy', 'Uses print concepts', 0, 13),
    (41, '18a', 'Literacy', 'Interacts during reading experiences and book conversations', 0, 13),
    (42, '18b', 'Literacy', 'Uses emergent reading skills', 0, 13),
    (43, '18c', 'Literacy', 'Retells stories and recounts details from informational texts', 0, 13),
    (44, '18d', 'Literacy', 'Uses context clues to read and comprehend texts', 0, 13),
    (45, '18e', 'Literacy', 'Reads fluently', 0, 13),
    (46, '19a', 'Literacy', 'Writes name', 0, 13),
    (47, '19b', 'Literacy', 'Writes to convey ideas and information', 0, 13),
    (48, '19c', 'Literacy', 'Writes using conventions', 0, 13);


-- =========================================================
-- REMOVE EXISTING MOCK GOLD SCORES FOR CLIENT A
-- This makes the script safe to re-run.
-- =========================================================

DELETE FROM gold_checkpoint_scores
WHERE client_id = 1001;


-- =========================================================
-- GENERATE FOUR MOCK CHECKPOINT SCORES FOR EVERY DIMENSION
--
-- Instead of manually writing ~160 rows, generate realistic
-- synthetic developmental growth automatically.
--
-- Each dimension begins around levels 3–5 and generally
-- increases across Fall -> Winter -> Spring -> Summer.
-- =========================================================

INSERT INTO gold_checkpoint_scores
(
    client_id,
    dimension_id,
    checkpoint_id,
    score,
    source,
    imported_at
)

SELECT
    1001,
    gd.dimension_id,
    gp.checkpoint_id,

    MIN(
        13,

        (
            3 + (gd.dimension_id % 3)
        )

        +

        CASE gp.checkpoint_number
            WHEN 1 THEN 0
            WHEN 2 THEN 1
            WHEN 3 THEN 3
            WHEN 4 THEN 4
        END
    ),

    'Teaching Strategies GOLD',
    datetime('now')

FROM gold_dimensions gd

CROSS JOIN gold_checkpoint_periods gp

ORDER BY
    gd.dimension_id,
    gp.checkpoint_number;