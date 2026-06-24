WITH last_biz_day_a AS (
    SELECT *,
        ROW_NUMBER() OVER (
            PARTITION BY certificate_id, FORMAT(date, 'yyyyMM')
            ORDER BY date DESC
        ) AS rn
    FROM table_a
)
SELECT
    b.certificate_id,
    b.date      AS month_end_date,
    a.date      AS last_biz_day_date,
    b.some_col,
    a.some_col
FROM table_b b
JOIN last_biz_day_a a
    ON a.certificate_id = b.certificate_id
    AND FORMAT(a.date, 'yyyyMM') = FORMAT(b.date, 'yyyyMM')
    AND a.rn = 1
