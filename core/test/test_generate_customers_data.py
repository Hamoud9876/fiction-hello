from core.src.generate_customers_data import generate_customers_data
from core.utils.customers_status_data import customers_status_data
from core.utils.cust_hist_active import cust_hist_active
from core.utils.cust_hist_inactive import cust_hist_inactive
from core.utils.cust_hist_long_changes import cust_hist_long_changes
from core.data.data import customers_status
import pytest
from datetime import datetime, date

class TestGenerateCustomerData:
    def test_handle_wrong_input(self):
        result = generate_customers_data("nna")
        assert result == "Value is not valid"

        result = generate_customers_data({"nna": "hamoud"})
        assert result == "Value is not valid"


    def test_output_seccessful(self):
        result = generate_customers_data(1)
        assert isinstance(result, dict)
        assert isinstance(result["customers"], list)


    def test_create_1_customer(self):
        result = generate_customers_data(1)
        assert len(result["customers"]) == 1

    @pytest.mark.skip
    def test_create_multiple_customers(self):
        result = generate_customers_data(2)
        assert len(result["customers"]) == 2

        result = generate_customers_data(13)
        assert len(result["customers"]) == 13

        result = generate_customers_data(50)
        assert len(result["customers"]) == 50

        result = generate_customers_data(600)
        assert len(result["customers"]) == 600



class TestCustomerStatus:
    def test_handle_wrong_input(self):
        date = "10/11/2025"
        result = customers_status_data(join_date= date,cust_id=1)
        assert result == "Not a valid input"

        date_obj = datetime.strptime(date,'%d/%m/%Y')
        date_obj = date_obj.date()
        result = customers_status_data(
            join_date=date_obj
            ,cust_id="hi")
        assert result == "Not a valid input"

    def test_return_dict(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date,'%d/%m/%Y')
        date_obj = date_obj.date()
        result = customers_status_data(
            join_date=date_obj
            ,cust_id=1)

        assert isinstance(result , dict)

    def test_output_contains_cust_sts(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date,'%d/%m/%Y')
        date_obj = date_obj.date()
        result = customers_status_data(
            join_date=date_obj
            ,cust_id=1)

        assert "customer_status" in result
        assert isinstance(result["customer_status"], str)


class TestCustHistActive:
    def test_handles_wrong_input(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date,'%d/%m/%Y')
        result = cust_hist_active({},date_obj,1)
        assert result == "Not a valid customer status input"

        result = cust_hist_active(customers_status,date,1)
        assert result == "Not a valid date input"

        result = cust_hist_active(customers_status,date_obj,"1")
        assert result == "Not a valid customer id"

        result = cust_hist_active(customers_status,date,"1")
        assert result == "Not a valid date input"

    def test_return_dict(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date,'%d/%m/%Y')
        result = cust_hist_active(customers_status,date_obj,1)

        assert isinstance(result, dict) 

    def test_return_expected_output(self):
        join_date = "10/2/2025"
        date_obj = datetime.strptime(join_date,'%d/%m/%Y')
        result = cust_hist_active(customers_status,date_obj,1)

        assert "customer_status" in result
        assert "cust_sts_hist" in result
        assert isinstance(result["cust_sts_hist"], list)
        assert isinstance(result["cust_sts_hist"][0]["customer_status"],str)
        assert isinstance(result["cust_sts_hist"][0]["customer_id"], int)
        assert isinstance(result["cust_sts_hist"][0]["change_date"], date)



class TestCustHistInactive:
    def test_handles_wrong_input(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date,'%d/%m/%Y')
        result = cust_hist_inactive({},date_obj,1)
        assert result == "Not a valid customer status input"

        result = cust_hist_inactive(customers_status,date,1)
        assert result == "Not a valid date input"

        result = cust_hist_inactive(customers_status,date_obj,"1")
        assert result == "Not a valid customer id"

        result = cust_hist_inactive(customers_status,date,"1")
        assert result == "Not a valid date input"

    def test_return_dict(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date,'%d/%m/%Y')
        result = cust_hist_inactive(customers_status,date_obj,1)

        assert isinstance(result, dict) 


    def test_return_expected_output(self):
        join_date = "10/2/2025"
        date_obj = datetime.strptime(join_date,'%d/%m/%Y')
        result = cust_hist_active(customers_status,date_obj,1)

        assert "customer_status" in result
        assert "cust_sts_hist" in result
        assert isinstance(result["cust_sts_hist"], list)
        assert isinstance(result["cust_sts_hist"][0]["customer_status"],str)
        assert isinstance(result["cust_sts_hist"][0]["customer_id"], int)
        assert isinstance(result["cust_sts_hist"][0]["change_date"], date)



        
class TestCustHistLongChanges:
    def test_handle_wrong_input(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date,'%d/%m/%Y')
        date_obj = date_obj.date()
        result = cust_hist_long_changes({},date_obj,1)
        assert result == "Not a valid customer status input"

        result = cust_hist_long_changes(customers_status,date,1)
        assert result == "Not a valid date input"

        result = cust_hist_long_changes(customers_status,date_obj,"1")
        assert result == "Not a valid customer id"

        result = cust_hist_long_changes(customers_status,date,"1")
        assert result == "Not a valid date input"

    def test_return_dict(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date,'%d/%m/%Y')
        date_obj = date_obj.date()
        result = cust_hist_long_changes(customers_status,date_obj,1)

        assert isinstance(result, dict) 

    

    def test_return_expected_output(self):
        join_date = "10/2/2010"
        date_obj = datetime.strptime(join_date,'%d/%m/%Y')
        date_obj = date_obj.date()
        result = cust_hist_long_changes(customers_status,date_obj,1)

        assert "customer_status" in result
        assert "cust_sts_hist" in result
        assert isinstance(result["cust_sts_hist"], list)
        assert isinstance(result["cust_sts_hist"][0]["customer_status"],str)
        assert isinstance(result["cust_sts_hist"][0]["customer_id"], int)
        assert isinstance(result["cust_sts_hist"][0]["change_date"], date)








