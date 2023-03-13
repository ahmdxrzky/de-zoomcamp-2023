# Answer for Homework Week 6
Disclaimer: code script used to answer these questions is available [here](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week5/homework.ipynb).

## Question 1
- Install Java, Spark, and PySpark by following this [installation guide](https://github.com/ahmdxrzky/de-zoomcamp-2023/blob/main/week5/installation_guide.md).
- Create a jupyter notebook (.ipynb) file.
- Import PySpark so it can be used in the notebook.
  ```python3
  from from pyspark.sql import SparkSession
  ```
- Create a local spark session by running this query below:
  ```python3
  spark = SparkSession.builder \
      .master("local[*]") \
      .appName('test') \
      .getOrCreate()
  ```
- Execute this to see what version of spark being used.
  ```python3
  spark.version
  ```
  
Result:
![image](https://user-images.githubusercontent.com/99194827/222944034-3dab97a8-bc92-4c9a-b7a0-831dcfc38975.png)
From image above, it can be clearly seen that version of spark being used is _3.3.2_.
