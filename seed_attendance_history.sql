-- Generate fictional weekday attendance histories for the prototype.
-- Codes are intentionally varied; this is not real clinical or school data.
PRAGMA foreign_keys = ON;

DELETE FROM attendance WHERE client_id BETWEEN 1001 AND 1006;

WITH RECURSIVE
client_ranges(client_id, start_date, end_date) AS (
    SELECT client_id, admission_date,
        CASE WHEN status = 'Discharged' THEN '2025-01-17' ELSE '2026-09-11' END
    FROM clients
    WHERE client_id BETWEEN 1001 AND 1006
),
days(client_id, attendance_date, end_date) AS (
    SELECT client_id, start_date, end_date FROM client_ranges
    UNION ALL
    SELECT client_id, date(attendance_date, '+1 day'), end_date
    FROM days
    WHERE attendance_date < end_date
),
weekdays AS (
    SELECT client_id, attendance_date,
           ROW_NUMBER() OVER (ORDER BY client_id, attendance_date) AS sequence_no
    FROM days
    WHERE CAST(strftime('%w', attendance_date) AS INTEGER) BETWEEN 1 AND 5
),
coded AS (
    SELECT client_id, attendance_date,
        CASE
            WHEN sequence_no % 37 = 0 THEN 'NT'
            WHEN sequence_no % 29 = 0 THEN '05'
            WHEN sequence_no % 23 = 0 THEN '03'
            WHEN sequence_no % 41 = 0 THEN '04'
            WHEN sequence_no % 67 = 0 THEN '02'
            ELSE 'P'
        END AS attendance_code
    FROM weekdays
)
INSERT INTO attendance (attendance_id, client_id, attendance_date, attendance_code, notes)
SELECT
    10000 + ROW_NUMBER() OVER (ORDER BY client_id, attendance_date),
    client_id,
    attendance_date,
    attendance_code,
    CASE attendance_code
        WHEN 'NT' THEN 'No transportation reported'
        WHEN '05' THEN 'Reported illness'
        WHEN '03' THEN 'Routine appointment'
        WHEN '04' THEN 'Family visit'
        WHEN '02' THEN 'DFS meeting'
        ELSE NULL
    END
FROM coded;
