from core.src.generate_contracts_data import generate_customers_data


class TestGenerateContractsData:
    def test_handles_wrong_input(self):
        result = generate_customers_data({})
        assert result == "Not a valid dict"

        result = generate_customers_data("hi")
        assert result == "Not a valid dict"

        result = generate_customers_data({"customers": []})
        assert result == "Not a valid dict"

        result = generate_customers_data({"customers": 0})
        assert result == "Not a valid dict"


    def test_return_dict(self):
        result = generate_customers_data({"customers": [1,2,3,4]})

        assert isinstance(result, dict)
        assert isinstance(result["contracts"], list)


    def test_generates_contract(self):
        result = generate_customers_data({"customers": [1]})

        assert len(result["contracts"]) == 1