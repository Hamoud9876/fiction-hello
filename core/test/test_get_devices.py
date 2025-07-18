from core.utils.get_devices import get_devices
from unittest.mock import patch
import pytest
from core.exceptions.invalid_input_exception import InvalidInput


class TestGetDevices:
    def test_handles_wrong_input(self):
        with pytest.raises(InvalidInput) as e:
            get_devices("2")
        assert "Invalid input in function 'get_devices': num_devices" in str(e.value)

        with pytest.raises(InvalidInput) as e:
            get_devices(0)
        assert "Invalid input in function 'get_devices': num_devices" in str(e.value)

    def test_return_list(self):
        result = get_devices(1)
        assert isinstance(result, list)

    def test_returns_one_item(self):
        result = get_devices(1)
        assert len(result) == 1

    def test_return_expected_num_devices(self):
        result = get_devices(2)
        assert len(result) == 2

        result = get_devices(23)
        assert len(result) == 23

        result = get_devices(12)
        assert len(result) == 12

    def test_output_content_correct(self):
        result = get_devices(1)
        for i in result:
            assert "device_model" in i
            assert "company" in i
            assert "screen_size" in i
            assert "ram" in i
            assert "storage" in i
            assert "price" in i

    @patch("core.utils.get_devices.randint")
    def test_return_phone(self, mock_randint):
        mock_randint.side_effect = [7, 0]
        result = get_devices(1)

        assert result[0]["device_model"] == "Phone 1"
        assert result[0]["company"] == "xoxo tech"
        assert result[0]["screen_size"] == 13.2
        assert result[0]["ram"] == 4
        assert result[0]["storage"] == 128
        assert result[0]["price"] == 329.98

        mock_randint.side_effect = [7, 1]
        result = get_devices(1)

        assert result[0]["device_model"] == "Phone 1"
        assert result[0]["company"] == "xoxo tech"
        assert result[0]["screen_size"] == 13.2
        assert result[0]["ram"] == 4
        assert result[0]["storage"] == 256
        assert result[0]["price"] == 399.98

    @patch("core.utils.get_devices.randint")
    def test_return_laptop(self, mock_randint):
        mock_randint.side_effect = [18, 0]
        result = get_devices(1)

        assert result[0]["device_model"] == "1"
        assert result[0]["company"] == "xoxo tech"
        assert result[0]["screen_size"] == 17.4
        assert result[0]["ram"] == 16
        assert result[0]["storage"] == 512
        assert result[0]["price"] == 450.00

    @patch("core.utils.get_devices.randint")
    def test_return_tablet(self, mock_randint):
        mock_randint.side_effect = [17, 0]
        result = get_devices(1)

        assert result[0]["device_model"] == "2000"
        assert result[0]["company"] == "xoxo tech"
        assert result[0]["screen_size"] == 16.3
        assert result[0]["ram"] == 8
        assert result[0]["storage"] == 1024
        assert result[0]["price"] == 799.99

    @patch("core.utils.get_devices.randint")
    def test_return_router(self, mock_randint):
        mock_randint.side_effect = [13, 0]
        result = get_devices(1)

        assert result[0]["device_model"] == "Spidre"
        assert result[0]["company"] == "xoxo tech"
        assert result[0]["screen_size"] == 0.0
        assert result[0]["ram"] == 128
        assert result[0]["storage"] == 0
        assert result[0]["price"] == 59.99

    @patch("core.utils.get_devices.randint")
    def test_return_watch(self, mock_randint):
        mock_randint.side_effect = [19, 0]
        result = get_devices(1)

        assert result[0]["device_model"] == "fit"
        assert result[0]["company"] == "xoxo tech"
        assert result[0]["screen_size"] == 40
        assert result[0]["ram"] == 512
        assert result[0]["storage"] == 4
        assert result[0]["price"] == 499.99
