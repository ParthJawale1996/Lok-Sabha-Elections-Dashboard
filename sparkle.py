from sparkly import SparklySession

class MySession(SparklySession):
    packages = [
        'datastax:spark-cassandra-connector:2.0.0-M2-s_2.11',
        'org.elasticsearch:elasticsearch-spark-20_2.11:5.1.1',
        'org.apache.spark:spark-sql_2.11:2.3.3'
    ]

if __name__ == '__main__':
    spark = MySession()
    df = spark.read_ext.cassandra('localhost','tweets','tweet_table')

print(df.head(10))
print('a')
