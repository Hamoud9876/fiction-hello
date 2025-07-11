from core.utils.con_period import con_period


class TestOnePeriodGenerator:
    def test_handles_wrong_input(self):
        result = con_period(11, 1.2)
        assert result == "Invalid input for period"

        result = con_period("11", 1.2)
        assert result == "Invalid input for period"

        result = con_period(12, 12)
        assert result == "Invalid input for weight"

    def test_returns_dict(self):
        result = con_period(12, 1.3)
        assert isinstance(result, dict)

    def test_return_expected_output(self):
        result = con_period(12, 1.3)

        assert "contract_title" in result
        assert "num_of_sims" in result
        assert "num_of_devices" in result
        assert "con_period" in result
        assert "devices" in result
        assert "price" in result
        assert isinstance(result["contract_title"], str)
        assert isinstance(result["num_of_sims"], int)
        assert isinstance(result["num_of_devices"], int)
        assert isinstance(result["con_period"], int)
        assert isinstance(result["devices"], list)
        assert isinstance(result["price"], float)
