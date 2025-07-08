from core.data.data import devices
from core.data.data import laptops_details
from core.data.data import watchs_details
from core.data.data import tablets_details
from core.data.data import router_details
from core.data.data import phones_details
from core.utils.get_devices import get_devices



class TestGetDevices:
    def test_handles_wrong_input(self):
        result = get_devices("2")
        assert result == "Invalid value for number of devices"

        result = get_devices(0)
        assert result == "Invalid value for number of devices"


    def test_return_list(self):
        result = get_devices(1)
        assert isinstance(result, list)

    def test_returns_one_item(self):
        result = get_devices(1)
        assert len(result) == 1
    

    def test_return_expected_num_devices(self):
        result = get_devices(2)
        assert len(result) ==2

        result = get_devices(23)
        assert len(result) ==23

        result = get_devices(12)
        assert len(result) ==12

    def test_output_content_correct(self):
        result = get_devices(1)
        for i in result:
            assert "device_model" in i
            assert "company" in i
            assert "screen_size" in i
            assert "ram" in i
            assert "storage" in i
            assert "price" in i
