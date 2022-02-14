from pyspark.sql import SparkSession
from pyspark.sql.types import StructType
from pyspark import SparkFiles


if __name__ == "__main__":
    spark = (SparkSession.builder
             .master("spark://10.84.0.1:7077")
             .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.3.1")
             .appName("test")
             .getOrCreate())

    sc = spark.sparkContext
    sc._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    sc._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "http://10.84.0.3:9000")
    sc._jsc.hadoopConfiguration().set("fs.s3a.access.key", "minio_access_key")
    sc._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "minio_secret_key")
    sc._jsc.hadoopConfiguration().set("fs.s3`a`.path.style.access", "true")
    sc._jsc.hadoopConfiguration().set("fs.s3a.connection.ssl.enabled","false")

    userSchema = StructType().add("name", "string").add("value", "integer")

    df = (spark.readStream
          .option("sep", ";")
          .option("header", "false")
          .schema(userSchema)
          .csv("s3a://testbucket/*.csv"))

    df.createOrReplaceTempView("my_data")

    totalByFirstLetter = spark.sql(
        "select substring(name, 1, 1) as first_letter, sum(value) from my_data group by first_letter")

    query = totalByFirstLetter.writeStream.outputMode("complete").format("console").start()

    query.awaitTermination()
