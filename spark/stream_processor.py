# from pyspark.sql import SparkSession
# from pyspark.sql.functions import explode, split

# spark = SparkSession.builder \
#     .appName("NewsKeywordAnalyzer") \
#     .getOrCreate()

# spark.sparkContext.setLogLevel("WARN")

# df = spark \
#     .readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("subscribe", "news-topic") \
#     .load()

# lines = df.selectExpr("CAST(value AS STRING)")
# words = lines.select(explode(split(lines.value, " ")).alias("word"))
# word_counts = words.groupBy("word").count()

# query = word_counts.writeStream \
#     .outputMode("complete") \
#     .format("console") \
#     .start()

# query.awaitTermination()


from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("AnomalyDetection").getOrCreate()

# Kafka에서 데이터 읽기
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "localhost:9093").option("subscribe", "transactions").load()

# 데이터를 처리하고 피처 추출 (예시)
df = df.selectExpr("CAST(value AS STRING)").select("value")
df.printSchema()


# from airflow import DAG
# from airflow.operators.bash import BashOperator
# from datetime import datetime

# with DAG('pipeline_dag',
#          start_date=datetime(2024, 1, 1),
#          schedule='@hourly',
#          catchup=False) as dag:

#     kafka_task = BashOperator(
#         task_id='start_kafka_producer',
#         bash_command='python3 kafka\kafka_producer.py'
#     )

#     spark_task = BashOperator(
#         task_id='start_spark_streaming',
#         bash_command='spark-submit spark\stream_processor.py'
#     )

#     kafka_task >> spark_task
    
