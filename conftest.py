import pytest
from lib.Utils import get_spark_session

@pytest.fixture
def spark():
    "Create a Spark session for testing"
    spark_session = get_spark_session("LOCAL")
    yield spark_session
    spark_session.stop()

@pytest.fixture
def expected_result(spark):
    "Give the expected result for the count_orders_state function"
    results_schema = "state string, count int"
    return spark.read \
    .format("csv") \
    .schema(results_schema) \
    .load("data/test_result/state_aggregate.csv")



