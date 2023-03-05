# Answer for Homework Week 4

## Question 1
Question: fact_trips records for 2019 and 2020 (test run variable disable) <br>
Logic: Count total record on fact_trips (make sure that the test run variable has been disabled or set to False). <br>
Query:
```
SELECT COUNT(1) AS total_fact_trips FROM `de-zoomcamp-375916.dbt_test.fact_trips`;
```
Result:
![image](https://user-images.githubusercontent.com/99194827/221353824-5a0156a3-11e9-45de-8a0d-adb74e617138.png)

From image above, it can be clearly seen that there are _61622271_ rows on fact_trips table (when test_run variable disabled). Choose _61648442_ as answer since it's the closest one.
