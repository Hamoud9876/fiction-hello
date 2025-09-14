from core.utils.con_details import con_details
import pytest
from datetime import date
from core.exceptions.invalid_input_exception import InvalidInput

my_date = date(day=1, month=1, year=2025)


class TestConDetails:
    def test_handles_wrong_input(self):
        with pytest.raises(InvalidInput) as e:
            con_details(11.1, 1.2, my_date)
        assert "Invalid input in 'con_details': period" in str(e.value)

        with pytest.raises(InvalidInput) as e:
            con_details(12, 12, my_date)
        assert "Invalid input in 'con_details': weight" in str(e.value)

    def test_returns_dict(self):
        result = con_details(12, 1.3, my_date)
        assert isinstance(result, dict)

    def test_return_expected_output(self):
        result = con_details(12, 1.3, my_date)

        assert "contract_title" in result
        assert "num_of_sims" in result
        assert "num_of_devices" in result
        assert "devices" in result
        assert "price" in result
        assert isinstance(result["contract_title"], str)
        assert isinstance(result["num_of_sims"], int)
        assert isinstance(result["num_of_devices"], int)
        assert isinstance(result["devices"], list)
        assert isinstance(result["price"], float)
