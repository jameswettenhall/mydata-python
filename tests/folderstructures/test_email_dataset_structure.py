"""
Test ability to scan the Email / Dataset folder structure.
"""
import requests_mock

from tests.fixtures import set_email_dataset_config

from tests.mocks import (
    mock_testfacility_user_response,
    mock_testusers_response,
    mock_test_facility_response,
    mock_test_instrument_response,
)


def test_scan_email_dataset_folders(set_email_dataset_config):
    """Test ability to scan the Email / Dataset folder structure.
    """
    from mydata.conf import settings
    from mydata.tasks.folders import scan_folders

    users = []
    folders = []

    def found_user(user):
        users.append(user)

    found_exp = None
    found_group = None

    def found_dataset(folder):
        folders.append(folder)

    with requests_mock.Mocker() as mocker:
        mock_testfacility_user_response(mocker, settings.general.mytardis_url)
        mock_testusers_response(mocker, settings, ["testuser1", "testuser2"])
        mock_test_facility_response(mocker, settings.general.mytardis_url)
        mock_test_instrument_response(mocker, settings.general.mytardis_url)

        scan_folders(found_user, found_group, found_exp, found_dataset)

    assert sorted([user.username for user in users]) == ["testuser1", "testuser2"]
    assert sorted([folder.name for folder in folders]) == ["Birds", "Flowers"]
    assert sum([folder.num_files for folder in folders]) == 5
