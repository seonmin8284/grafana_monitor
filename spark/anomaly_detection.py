from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType

# 1. Spark 세션 생성
spark = SparkSession.builder \
    .appName("AnomalyDetection") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")  # 불필요한 로그 줄이기

# 2. Kafka에서 스트리밍 데이터 수신
raw_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9093") \
    .option("subscribe", "transactions") \
    .load()

# 3. 메시지의 value 부분을 JSON 문자열로 파싱
json_df = raw_df.selectExpr("CAST(value AS STRING) as json_string")

# 4. JSON 스키마 정의 (Kafka 메시지에 들어오는 구조에 맞게)
schema = StructType() \
    .add("transaction_id", StringType()) \
    .add("amount", DoubleType()) \
    .add("card_type", StringType()) \
    .add("timestamp", StringType())

parsed_df = json_df.select(from_json(col("json_string"), schema).alias("data")).select("data.*")

# 5. 이상 거래 탐지 로직 (예: 금액이 1000 이상인 경우 이상으로 간주)
anomaly_df = parsed_df.filter(col("amount") > 1000)

# 6. 콘솔 출력 or Kafka로 출력
query = anomaly_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
