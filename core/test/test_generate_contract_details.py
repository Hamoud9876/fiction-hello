from core.src.generate_contract_details import generate_contract_details
from core.data.data import customers_status
from datetime import date


class TestGeneratContractDetails:
    def test_handles_wrong_input(self):
        result = generate_contract_details("1",2,[])
        assert result == "Not a valid Value"

        result = generate_contract_details(2,0,[])
        assert result == "Not a valid contract type"

        result = generate_contract_details(2,2,{})
        assert result == "Not a valid invalid history"

    def test_returns_list(self):
        result = generate_contract_details(1,1,[])
        assert isinstance(result, list)

    def test_generate_one_commitment(self):
        join_date = date(day=1, month=1,year=2024)
        result = generate_contract_details(
            1,
            1,
             [
            {
                "customer_status": customers_status[0],
                "customer_id": 1,
                "change_date": join_date,
            }
        ])
        for i in result:
            assert "contract_title" in i
            assert "num_of_sims" in i
            assert "num_of_devices" in i
            assert "con_period" in i
            assert "devices" in i
            assert "price" in i
            assert isinstance(i["contract_title"], str)
            assert isinstance(i["num_of_sims"], int)
            assert isinstance(i["num_of_devices"], int)
            assert isinstance(i["con_period"], int)
            assert isinstance(i["devices"], list)
            assert isinstance(i["price"], float)

    def test_generate_multiple_commitments(self):
        join_date = date(day=1, month=1,year=2022)
        s2_date = date(day=2, month=1,year=2023)
        s3_date = date(day=3, month=1,year=2024)
        result = generate_contract_details(
            1,
            1,
             [
            {
                "customer_status": customers_status[0],
                "customer_id": 1,
                "change_date": join_date,
            },
            {
                "customer_status": customers_status[1],
                "customer_id": 1,
                "change_date": s2_date,
            },
            {
                "customer_status": customers_status[0],
                "customer_id": 1,
                "change_date": s3_date,
            },
        ])

        assert len(result) == 2
        

    def test_expected_outpot_multiple_commitment(self):
        join_date = date(day=1, month=1,year=2022)
        s2_date = date(day=2, month=1,year=2023)
        s3_date = date(day=3, month=1,year=2024)
        result = generate_contract_details(
            1,
            1,
             [
            {
                "customer_status": customers_status[0],
                "customer_id": 1,
                "change_date": join_date,
            },
            {
                "customer_status": customers_status[1],
                "customer_id": 1,
                "change_date": s2_date,
            },
            {
                "customer_status": customers_status[0],
                "customer_id": 1,
                "change_date": s3_date,
            },
        ])

        for i in result:
            assert "contract_title" in i
            assert "num_of_sims" in i
            assert "num_of_devices" in i
            assert "con_period" in i
            assert "devices" in i
            assert "price" in i
            assert isinstance(i["contract_title"], str)
            assert isinstance(i["num_of_sims"], int)
            assert isinstance(i["num_of_devices"], int)
            assert isinstance(i["con_period"], int)
            assert isinstance(i["devices"], list)
            assert isinstance(i["price"], float)

    def test_generate_commitment_with_long_years(self):
        join_date = date(day=1, month=1,year=2020)
        result = generate_contract_details(
            1,
            1,
             [
            {
                "customer_status": customers_status[0],
                "customer_id": 1,
                "change_date": join_date,
            },])
        
        assert len(result) <=5

        join_date = date(day=1, month=1,year=2018)
        result = generate_contract_details(
            1,
            1,
             [
            {
                "customer_status": customers_status[0],
                "customer_id": 1,
                "change_date": join_date,
            },])
        
        assert len(result) <=7