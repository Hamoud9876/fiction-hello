from core.src.generate_billings import generate_bellings
from core.exceptions.invalid_input_exception import InvalidInput
from dateutil.relativedelta import relativedelta
from datetime import date
import pytest


class TestGeneratBillings:
    def test_handles_wrong_input(self):
        with pytest.raises(InvalidInput) as e:
            generate_bellings({}, 2)
        assert "Invalid input in 'generate_bellings': period" in str(e.value)

    def test_generat_one_bill(self):
        my_date = date(day=1, month=1, year=2025)
        usage = [
            {
                "used_cellular_data": 155.00,
                "used_call_time": 155,
                "used_roam_data": 55.00,
                "used_roam_call_time": 55,
                "start_date": my_date,
                "end_date": my_date + relativedelta(months=1),
            }
        ]
        result = generate_bellings(usage, 20)

        assert "amount" in result[0]
        assert "status" in result[0]
        assert "issue_date" in result[0]
        assert "complete_date" in result[0]
        assert "due_date" in result[0]

    def test_generate_multiple_bills(self):
        my_date = date(day=1, month=1, year=2025)
        usage = [
            {
                "used_cellular_data": 155.00,
                "used_call_time": 155,
                "used_roam_data": 55.00,
                "used_roam_call_time": 55,
                "start_date": my_date,
                "end_date": my_date + relativedelta(months=1),
            },
            {
                "used_cellular_data": 155.00,
                "used_call_time": 155,
                "used_roam_data": 55.00,
                "used_roam_call_time": 55,
                "start_date": my_date + relativedelta(months=1),
                "end_date": my_date + relativedelta(months=2),
            },
        ]

        result = generate_bellings(usage, 20)

        for i in result:
            assert "amount" in result[0]
            assert "status" in result[0]
            assert "issue_date" in result[0]
            assert "complete_date" in result[0]
            assert "due_date" in result[0]
            assert isinstance(i["amount"], float)
            assert isinstance(i["status"], str)
            assert isinstance(i["issue_date"], date)
            assert isinstance(i["complete_date"], (date, type(None)))
            assert isinstance(i["due_date"], date)

    def test_doesnot_generate_future_bills(self):
        my_date = date.today() - relativedelta(months=1)
        usage = [
            {
                "used_cellular_data": 155.00,
                "used_call_time": 155,
                "used_roam_data": 55.00,
                "used_roam_call_time": 55,
                "start_date": my_date,
                "end_date": my_date + relativedelta(months=1),
            },
            {
                "used_cellular_data": 155.00,
                "used_call_time": 155,
                "used_roam_data": 55.00,
                "used_roam_call_time": 55,
                "start_date": my_date + relativedelta(months=1),
                "end_date": my_date + relativedelta(months=2),
            },
        ]

        result = generate_bellings(usage, 20)

        assert len(result) < 2
