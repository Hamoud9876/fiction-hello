from core.src.customer_usage import customer_usage
from core.exceptions.invalid_input_exception import InvalidInput
from datetime import datetime,date
import pytest

class TestCustomerUsage:
    def test_handles_wrong_input(self):
        date = "10/2/2025"
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        date_obj = date_obj.date()
        with pytest.raises(InvalidInput) as e:
            customer_usage("12",date_obj)
        assert "Invalid input in 'customer_usage': period" in str(e.value)
        with pytest.raises(InvalidInput) as e:
            customer_usage(13,date_obj)
        assert "Invalid input in 'customer_usage': period" in str(e.value)


        with pytest.raises(InvalidInput) as e:
            customer_usage(12,date)
        assert "Invalid input in 'customer_usage': start_date" in str(e.value)


    def test_generate_12_months_record(self):
        my_date = "10/2/2025"
        date_obj = datetime.strptime(my_date, "%d/%m/%Y")
        date_obj = date_obj.date()

        result = customer_usage(12,date_obj)

        for i in result:
            assert "used_cerllular_data" in i
            assert isinstance(i["used_cerllular_data"], float)
            assert "used_call_time" in i
            assert isinstance(i["used_call_time"], int)
            assert "used_roam_data" in i
            assert isinstance(i["used_roam_data"], float)
            assert "used_roam_call_time" in i
            assert isinstance(i["used_roam_call_time"], int)
            assert "start_date" in i
            assert isinstance(i["start_date"], date)
            assert "end_date" in i
            assert isinstance(i["end_date"], date)
    
    def test_generate_24_months_record(self):
        my_date = "10/2/2025"
        date_obj = datetime.strptime(my_date, "%d/%m/%Y")
        date_obj = date_obj.date()

        result = customer_usage(24,date_obj)

        for i in result:
            assert "used_cerllular_data" in i
            assert isinstance(i["used_cerllular_data"], float)
            assert "used_call_time" in i
            assert isinstance(i["used_call_time"], int)
            assert "used_roam_data" in i
            assert isinstance(i["used_roam_data"], float)
            assert "used_roam_call_time" in i
            assert isinstance(i["used_roam_call_time"], int)
            assert "start_date" in i
            assert isinstance(i["start_date"], date)
            assert "end_date" in i
            assert isinstance(i["end_date"], date)



    def test_generate_36_months_record(self):
        my_date = "10/2/2025"
        date_obj = datetime.strptime(my_date, "%d/%m/%Y")
        date_obj = date_obj.date()

        result = customer_usage(36,date_obj)

        for i in result:
            assert "used_cerllular_data" in i
            assert isinstance(i["used_cerllular_data"], float)
            assert "used_call_time" in i
            assert isinstance(i["used_call_time"], int)
            assert "used_roam_data" in i
            assert isinstance(i["used_roam_data"], float)
            assert "used_roam_call_time" in i
            assert isinstance(i["used_roam_call_time"], int)
            assert "start_date" in i
            assert isinstance(i["start_date"], date)
            assert "end_date" in i
            assert isinstance(i["end_date"], date)

