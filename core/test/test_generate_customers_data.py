from core.src.generate_customers_data import generate_customers_data
from core.src.customers_status_data import customers_status_data
from core.src.cust_hist_active import cust_hist_active
from core.src.cust_hist_inactive import cust_hist_inactive
from core.src.cust_hist_long_changes import cust_hist_long_changes
from core.src.generate_address_data import generate_address_data
from core.data.data import customers_status
from core.utils.generate_post_code import generate_post_code
from core.utils.days_between import days_between
from core.utils.random_string import random_string
from unittest.mock import patch
from datetime import datetime, date
import pytest
from core.exceptions.invalid_input_exception import InvalidInput


class TestGenerateCustomerData:
    def test_handle_wrong_input(self):
        with pytest.raises(InvalidInput) as e:
            generate_customers_data("nna")
        assert "Invalid input in 'generate_customers_data': value" in str(e.value)

        with pytest.raises(InvalidInput) as e:
            generate_customers_data({"nna": "hamoud"})
        assert "Invalid input in 'generate_customers_data': value" in str(e.value)

    def test_output_seccessful(self):
        result = generate_customers_data(1)
        assert isinstance(result, list)
        assert isinstance(result[0], dict)

    def test_create_one_customer(self):
        result = generate_customers_data(1)
        assert len(result) == 1

    def test_create_multiple_customers(self):
        result = generate_customers_data(2)
        assert len(result) == 2

        result = generate_customers_data(13)
        assert len(result) == 13

        result = generate_customers_data(50)
        assert len(result) == 50

        result = generate_customers_data(600)
        assert len(result) == 600


class TestCustomerStatus:
    def test_handle_wrong_input(self):
        date = "10/1/2025"
        with pytest.raises(InvalidInput) as e:
            customers_status_data(join_date=date)
        assert "Invalid input in function 'customers_status_data': date" in str(e.value)

    def test_return_dict(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        date_obj = date_obj.date()
        result = customers_status_data(join_date=date_obj)

        assert isinstance(result, dict)

    def test_output_contains_cust_sts(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        date_obj = date_obj.date()
        result = customers_status_data(join_date=date_obj)

        assert "customer_status" in result
        assert isinstance(result["customer_status"], str)

    @patch("core.src.customers_status_data.randint")
    def test_returns_hist_active(self, mock_randint):
        mock_randint.return_value = 2

        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        date_obj = date_obj.date()
        result = customers_status_data(join_date=date_obj)

        assert result["customer_status"] == "Active"

    @patch("core.src.customers_status_data.randint")
    def test_returns_hist_inactive(self, mock_randint):
        mock_randint.return_value = 3

        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        date_obj = date_obj.date()
        result = customers_status_data(join_date=date_obj)

        assert result["customer_status"] == "Inactive"

    @patch("core.src.customers_status_data.randint")
    def test_returns_hist_long(self, mock_randint):
        mock_randint.return_value = 3

        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        date_obj = date_obj.date()
        result = customers_status_data(join_date=date_obj)

        assert result["customer_status"] in customers_status


class TestCustHistActive:
    def test_handles_wrong_input(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        with pytest.raises(InvalidInput) as e:
            cust_hist_active({}, date_obj)
        assert "Invalid input in function 'cust_hist_active': list" in str(e.value)

        with pytest.raises(InvalidInput) as e:
            cust_hist_active(customers_status, date)
        assert "Invalid input in function 'cust_hist_active': date" in str(e.value)

    def test_return_dict(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        result = cust_hist_active(customers_status, date_obj)

        assert isinstance(result, dict)

    def test_return_expected_output(self):
        join_date = "10/2/2025"
        date_obj = datetime.strptime(join_date, "%d/%m/%Y")
        result = cust_hist_active(customers_status, date_obj)

        assert "customer_status" in result
        assert "cust_sts_hist" in result
        assert isinstance(result["cust_sts_hist"], list)
        assert isinstance(result["cust_sts_hist"][0]["customer_status"], str)
        assert isinstance(result["cust_sts_hist"][0]["change_date"], date)


class TestCustHistInactive:
    def test_handles_wrong_input(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        with pytest.raises(InvalidInput) as e:
            cust_hist_inactive({}, date_obj)
        assert "Invalid input in function 'cust_hist_inactive': list" in str(e.value)

        with pytest.raises(InvalidInput) as e:
            cust_hist_inactive(customers_status, date)
        assert "Invalid input in function 'cust_hist_inactive': date" in str(e.value)

    def test_return_dict(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        result = cust_hist_inactive(customers_status, date_obj)

        assert isinstance(result, dict)

    def test_return_expected_output(self):
        join_date = "10/2/2025"
        date_obj = datetime.strptime(join_date, "%d/%m/%Y")
        result = cust_hist_active(customers_status, date_obj)

        assert "customer_status" in result
        assert "cust_sts_hist" in result
        assert isinstance(result["cust_sts_hist"], list)
        assert isinstance(result["cust_sts_hist"][0]["customer_status"], str)
        assert isinstance(result["cust_sts_hist"][0]["change_date"], date)


class TestCustHistLongChanges:
    def test_handle_wrong_input(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        date_obj = date_obj.date()
        with pytest.raises(InvalidInput) as e:
            cust_hist_long_changes({}, date_obj)
        assert "Invalid input in function 'cust_hist_long_changes': list" in str(
            e.value
        )

        with pytest.raises(InvalidInput) as e:
            cust_hist_long_changes(customers_status, date)
        assert "Invalid input in function 'cust_hist_long_changes': date" in str(
            e.value
        )

    def test_return_dict(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        date_obj = date_obj.date()
        result = cust_hist_long_changes(customers_status, date_obj)

        assert isinstance(result, dict)

    def test_return_expected_output(self):
        join_date = "10/2/2010"
        date_obj = datetime.strptime(join_date, "%d/%m/%Y")
        date_obj = date_obj.date()
        result = cust_hist_long_changes(customers_status, date_obj)

        assert "customer_status" in result
        assert "cust_sts_hist" in result
        assert isinstance(result["cust_sts_hist"], list)
        assert isinstance(result["cust_sts_hist"][0]["customer_status"], str)
        assert isinstance(result["cust_sts_hist"][0]["change_date"], date)


class TestAddressData:
    def test_return_dict(self):
        result = generate_address_data()
        assert isinstance(result, list)

    @patch("core.src.generate_address_data.randint")
    def test_generates_one_address(self, mock_rand_int):
        mock_rand_int.return_value = 2
        result = generate_address_data()
        assert len(result) == 1
        for i in result:
            assert isinstance(i["first_line"], str)
            assert isinstance(i["second_line"], str)
            assert isinstance(i["city"], str)
            assert isinstance(i["county"], str)
            assert isinstance(i["post_code"], str)
            assert i["address_type"] in ["Home", "Billing"]
            assert isinstance(i["address_type"], str)

    @patch("core.src.generate_address_data.randint")
    def test_generate_two_addresses(self, mock_rand_int):
        mock_rand_int.return_value = 1
        result = generate_address_data()
        assert len(result) == 2
        for i in result:
            assert isinstance(i["first_line"], str)
            assert isinstance(i["second_line"], str)
            assert isinstance(i["city"], str)
            assert isinstance(i["county"], str)
            assert isinstance(i["post_code"], str)
            assert i["address_type"] in ["Home", "Billing"]
            assert isinstance(i["address_type"], str)


class TestGeneratePostCode:
    def test_return_str(self):
        result = generate_post_code()
        assert isinstance(result, str)


class TestDaysBetween:
    def test_handle_wrong_input(self):
        join_date1 = "10/2/2010"
        join_date2 = "10/2/2010"
        date_obj2 = datetime.strptime(join_date2, "%d/%m/%Y")
        date_obj2 = date_obj2.date()

        with pytest.raises(InvalidInput) as e:
            days_between(join_date1, date_obj2)
        assert "Invalid input in function 'days_between': d1" in str(e.value)

        join_date1 = "10/2/2010"
        date_obj1 = datetime.strptime(join_date1, "%d/%m/%Y")
        date_obj1 = date_obj1.date()
        join_date2 = "10/2/2010"

        with pytest.raises(InvalidInput) as e:
            days_between(date_obj1, join_date2)
        assert "Invalid input in function 'days_between': d2" in str(e.value)

    def test_return_int(self):
        join_date1 = "10/2/2010"
        date_obj1 = datetime.strptime(join_date1, "%d/%m/%Y")
        date_obj1 = date_obj1.date()

        join_date2 = "12/2/2010"
        date_obj2 = datetime.strptime(join_date2, "%d/%m/%Y")
        date_obj2 = date_obj2.date()

        result = days_between(date_obj1, date_obj2)
        assert isinstance(result, int)

    def test_returns_correct_diff(self):
        join_date1 = "10/2/2010"
        date_obj1 = datetime.strptime(join_date1, "%d/%m/%Y")
        date_obj1 = date_obj1.date()

        join_date2 = "12/2/2010"
        date_obj2 = datetime.strptime(join_date2, "%d/%m/%Y")
        date_obj2 = date_obj2.date()

        result = days_between(date_obj1, date_obj2)
        assert result == 2

        join_date1 = "10/2/2010"
        date_obj1 = datetime.strptime(join_date1, "%d/%m/%Y")
        date_obj1 = date_obj1.date()

        join_date2 = "20/2/2010"
        date_obj2 = datetime.strptime(join_date2, "%d/%m/%Y")
        date_obj2 = date_obj2.date()

        result = days_between(date_obj1, date_obj2)
        assert result == 10

        join_date1 = "10/2/2010"
        date_obj1 = datetime.strptime(join_date1, "%d/%m/%Y")
        date_obj1 = date_obj1.date()

        join_date2 = "20/3/2010"
        date_obj2 = datetime.strptime(join_date2, "%d/%m/%Y")
        date_obj2 = date_obj2.date()

        result = days_between(date_obj1, date_obj2)
        assert result == 38


class TestRandomString:
    def test_handles_wrong_input(self):
        result = random_string("")
        assert result == "Not a valid length"

        result = random_string(7.1)
        assert result == "Not a valid length"

    def test_return_str(self):
        result = random_string(1)
        assert isinstance(result, str)

    def test_return_correct_len(self):
        result = random_string(1)
        assert len(result) == 1

        result = random_string(16)
        assert len(result) == 16

        result = random_string(123)
        assert len(result) == 123
