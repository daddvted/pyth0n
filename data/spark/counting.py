import os
import sys
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("spark-nltk").getOrCreate()


text_file = spark.read.text("hdfs:///ted-test/1973-Nixon.txt")

print(text_file.count())
