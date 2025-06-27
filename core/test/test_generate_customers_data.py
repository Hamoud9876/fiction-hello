from core.utils.generate_customers_data import generate_customers_data


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

    def test_create_multiple_customers(self):
        result = generate_customers_data(2)
        assert len(result["customers"]) == 2

        result = generate_customers_data(13)
        assert len(result["customers"]) == 13

        result = generate_customers_data(50)
        assert len(result["customers"]) == 50

        result = generate_customers_data(600)
        assert len(result["customers"]) == 600



