import pytest
from lib.DataReader import read_customers, read_orders
from lib.DataManipulation import filter_closed_orders,count_orders_state,join_orders_customers,filter_orders_generic
from lib.ConfigReader import get_app_config

@pytest.mark.skip
def test_read_customers(spark):
    customers_count = read_customers(spark, "LOCAL").count()
    assert customers_count == 12435

@pytest.mark.skip
def test_read_orders(spark):
    orders_count = read_orders(spark, "LOCAL").count()
    assert orders_count == 68884

@pytest.mark.skip
def test_filter_closed_orders(spark):
    orders_df = read_orders(spark, "LOCAL")
    filtered_count = filter_closed_orders(orders_df).count()
    assert filtered_count == 7556

@pytest.mark.skip("work in progress")
def test_read_app_config():
    config = get_app_config("LOCAL")
    assert config["orders.file.path"] == "data/orders.csv"

@pytest.mark.skip
def test_count_orders_state(spark, expected_result):
    orders_df = read_orders(spark, "LOCAL")
    customers_df = read_customers(spark, "LOCAL")
    closed_orders_df = filter_closed_orders(orders_df)
    joined_df = join_orders_customers(closed_orders_df, customers_df)
    actual_results = count_orders_state(joined_df)
    assert sorted(actual_results.collect()) == sorted(expected_result.collect())

@pytest.mark.skip
def test_check_closed_count(spark):
    orders_df = read_orders(spark, "LOCAL")
    closed_orders_df = filter_orders_generic(orders_df,"CLOSED")
    filtered_count = closed_orders_df.count()
    assert filtered_count == 7556

@pytest.mark.skip
def test_check_pending_payment_count(spark):
    orders_df = read_orders(spark, "LOCAL")
    closed_orders_df = filter_orders_generic(orders_df,"PENDING_PAYMENT")
    filtered_count = closed_orders_df.count()
    assert filtered_count == 15030

@pytest.mark.skip
def test_check_complete_count(spark):
    orders_df = read_orders(spark, "LOCAL")
    closed_orders_df = filter_orders_generic(orders_df,"COMPLETE")
    filtered_count = closed_orders_df.count()
    assert filtered_count == 22900

# Defining generic test function to check counts for different order statuses and ignored skipped markers. 
@pytest.mark.parametrize(
        "status,count", 
        [("CLOSED", 7556), 
         ("PENDING_PAYMENT", 15030), 
         ("COMPLETE", 22900)])

def test_check_count(spark,status,count):
    orders_df = read_orders(spark, "LOCAL")
    closed_orders_df = filter_orders_generic(orders_df,status)
    filtered_count = closed_orders_df.count()
    assert filtered_count == count