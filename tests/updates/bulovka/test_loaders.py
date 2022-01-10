from unittest import TestCase
from unittest.mock import Mock, patch

from django.test import override_settings
from updates.bulovka.loaders import patient_loader


class PatientLoaderTest(TestCase):
    @patch("updates.bulovka.loaders.requests.get")
    @override_settings(REFERENCES_TOKEN="token")
    def test__add_params_to_url(self, mocked_get: Mock):
        mocked_get.side_effect = [
            Mock(
                json=Mock(return_value={"result": ["result1", "result2", "result3"]}),
                status_code=200,
            )
        ]
        list(
            patient_loader(
                url="http://api-url", use_token=True, url_parameters={"clinicId": 2}
            )
        )

        mocked_get.assert_called_once_with("http://api-url?clinicId=2&token=token")
