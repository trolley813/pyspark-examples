from spark_submit import SparkJob
from datetime import datetime

spark_args = {
    "master": "spark://10.84.0.1:7077",
    "name": "my_spark_job_client",
    "files": "./data.csv",
    "spark_home": "./env/lib/python3.10/site-packages/pyspark"
}

app = SparkJob("./spark_job.py", **spark_args)
try:
    app.submit()
except:
    print(f"{datetime.now()} --- Error in Spark job, state is {app.get_state()}, {app.get_code()}")
print(f"{datetime.now()} --- Submitted Spark job, state is {app.get_state()}")

while not app.concluded:
    print(f"{datetime.now()} --- Waiting for job, state is {app.get_state()}")

print(f"{datetime.now()} --- Finished, state is {app.get_state()}")
