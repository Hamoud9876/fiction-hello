from core.src.generate_sim_data import generate_sims_data


class TestSimsData:
    def test_handles_wrong_input(self):
        result = generate_sims_data("1")
        assert result == "Invalid value input"

        result = generate_sims_data(0)
        assert result == "Invalid value input"

    def test_return_list(self):
        result = generate_sims_data(1)
        assert isinstance(result, list)

    def test_generate_one_number(self):
        result = generate_sims_data(1)
        assert len(result) == 1

    def test_output_int(self):
        result = generate_sims_data(1)
        assert isinstance(result[0], int)

    def test_generate_multiple_sims(self):
        result = generate_sims_data(13)
        assert len(result) == 13
