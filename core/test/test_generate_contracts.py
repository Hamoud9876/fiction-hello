from core.src.generate_contracts import generate_contracts
from core.data.data import customers_status
from datetime import date
import pytest
from core.exceptions.invalid_input_exception import InvalidInput


class TestGeneratContracts:
    def test_handles_wrong_input(self):
        with pytest.raises(InvalidInput) as e:
            generate_contracts("1", 2, {})
        assert "Invalid input in 'generate_contracts': value" in str(e.value)

        with pytest.raises(InvalidInput) as e:
            generate_contracts(2, 0, {})
        assert "Invalid input in 'generate_contracts': con_type" in str(e.value)

        with pytest.raises(InvalidInput) as e:
            generate_contracts(2, 2, [])
        assert "Invalid input in 'generate_contracts': sts_hist" in str(e.value)

    def test_returns_list(self):
        result = generate_contracts(1, 1, {"cust_sts_hist": []})
        assert isinstance(result, list)

    def test_generate_one_commitment(self):
        join_date = date(day=1, month=1, year=2024)
        result = generate_contracts(
            1,
            1,
            {
                "cust_sts_hist": [
                    {
                        "customer_status": customers_status[0],
                        "change_date": join_date,
                    }
                ]
            },
        )
        for i in result:
            assert "contract_title" in i
            assert "num_of_sims" in i
            assert "num_of_devices" in i
            assert "con_period" in i
            assert "devices" in i
            assert "price" in i
            assert "available_data" in i
            assert isinstance(i["contract_title"], str)
            assert isinstance(i["num_of_sims"], int)
            assert isinstance(i["num_of_devices"], int)
            assert isinstance(i["con_period"], int)
            assert isinstance(i["devices"], list)
            assert isinstance(i["price"], float)
            assert isinstance(i["available_data"], dict)
            assert isinstance(i["available_data"]["calls_times"], int)
            assert isinstance(i["available_data"]["cellular_data"], float)
            assert isinstance(i["available_data"]["roam_data"], float)
            assert isinstance(i["available_data"]["roam_call_time"], int)

    def test_generate_multiple_commitments(self):
        join_date = date(day=1, month=1, year=2022)
        s2_date = date(day=2, month=1, year=2023)
        s3_date = date(day=3, month=1, year=2024)
        result = generate_contracts(
            1,
            1,
            {
                "cust_sts_hist": [
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
                ],
            },
        )

        assert len(result) == 2

    def test_expected_outpot_multiple_commitment(self):
        join_date = date(day=1, month=1, year=2022)
        s2_date = date(day=2, month=1, year=2023)
        s3_date = date(day=3, month=1, year=2024)
        result = generate_contracts(
            1,
            1,
            {
                "cust_sts_hist": [
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
                ],
            },
        )

        for i in result:
            assert "contract_title" in i
            assert "num_of_sims" in i
            assert "num_of_devices" in i
            assert "con_period" in i
            assert "devices" in i
            assert "price" in i
            assert "available_data" in i
            assert isinstance(i["contract_title"], str)
            assert isinstance(i["num_of_sims"], int)
            assert isinstance(i["num_of_devices"], int)
            assert isinstance(i["con_period"], int)
            assert isinstance(i["devices"], list)
            assert isinstance(i["price"], float)
            assert isinstance(i["available_data"], dict)
            assert isinstance(i["available_data"]["calls_times"], int)
            assert isinstance(i["available_data"]["cellular_data"], float)
            assert isinstance(i["available_data"]["roam_data"], float)
            assert isinstance(i["available_data"]["roam_call_time"], int)

    def test_generate_commitment_with_long_years(self):
        join_date = date(day=1, month=1, year=2020)
        result = generate_contracts(
            1,
            1,
            {
                "cust_sts_hist": [
                    {
                        "customer_status": customers_status[0],
                        "customer_id": 1,
                        "change_date": join_date,
                    },
                ],
            },
        )

        assert len(result) <= 5

        join_date = date(day=1, month=1, year=2018)
        result = generate_contracts(
            1,
            1,
            {
                "cust_sts_hist": [
                    {
                        "customer_status": customers_status[0],
                        "customer_id": 1,
                        "change_date": join_date,
                    },
                ],
            },
        )

        assert len(result) <= 7
