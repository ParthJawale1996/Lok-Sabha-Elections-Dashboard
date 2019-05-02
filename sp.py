from pyspark.sql import SparkSession
import os

os.environ["SPARK_HOME"] = "/usr/local/spark/"

spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value")\
    .config('spark.jars.packages',"org.elasticsearch:elasticsearch-spark-20_2.11:5.5.2")\
    .getOrCreate()

es_conf = {"es.read.metadata": "true","es.read.field.as.array.include" : "id, tweet"}

tweets = spark.read.format("org.elasticsearch.spark.sql").options(**es_conf).load("tweets/tweet_table")

tweets.count()
print('a')
