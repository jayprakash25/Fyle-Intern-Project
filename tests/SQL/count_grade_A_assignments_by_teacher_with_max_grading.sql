-- Write query to find the number of grade A's given by the teacher who has graded the most assignments
WITH teacher_graded_counts AS (
    SELECT teacher_id, COUNT(*) AS graded_count
    FROM assignments
    WHERE state = 'GRADED'
    GROUP BY teacher_id
)
SELECT t.id AS teacher_id, COUNT(*) AS grade_a_count
FROM assignments a
JOIN teacher_graded_counts tgc ON a.teacher_id = tgc.teacher_id
JOIN teachers t ON a.teacher_id = t.id
WHERE tgc.graded_count = (
  SELECT MAX(graded_count) FROM teacher_graded_counts
) AND a.grade = 'A'
GROUP BY t.id;