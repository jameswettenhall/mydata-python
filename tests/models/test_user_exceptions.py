"""
Test ability to handle user-related exceptions.
"""
import pytest
import requests_mock

from requests.exceptions import HTTPError

from tests.fixtures import set_exp_dataset_config
from tests.mocks import EMPTY_LIST_RESPONSE, MOCK_USER_RESPONSE


def test_user_exceptions(set_exp_dataset_config):
    """Test ability to handle user-related exceptions.
    """
    from mydata.conf import settings
    from mydata.models.user import User

    # Test retrieving default owner's user record (using the User model's
    # get_user_by_username method) and ensure that no exception is raised:
    with requests_mock.Mocker() as mocker:
        get_user_url = (
            "%s/api/v1/user/?format=json&username=testfacility"
            % settings.general.mytardis_url
        )
        mocker.get(get_user_url, text=MOCK_USER_RESPONSE)
        owner = settings.general.default_owner

    # Test retrieving default owner's user record (using the User model's
    # get_user_by_email method) and ensure that no exception is raised:
    with requests_mock.Mocker() as mocker:
        get_user_url = (
            "%s/api/v1/user/?format=json&email__iexact=testfacility%%40example.com"
        ) % settings.general.mytardis_url
        mocker.get(get_user_url, text=MOCK_USER_RESPONSE)
        owner = settings.general.default_owner
        _ = User.get_user_by_email(owner.email)

    # Try to look up user record by username with an invalid API key,
    # which should give 401 (Unauthorized).
    api_key = settings.general.api_key
    settings.general.api_key = "invalid"
    with requests_mock.Mocker() as mocker:
        get_user_url = (
            "%s/api/v1/user/?format=json&username=testfacility"
            % settings.general.mytardis_url
        )
        mocker.get(get_user_url, status_code=401)
        with pytest.raises(HTTPError) as excinfo:
            _ = User.get_user_by_username(owner.username)
        assert excinfo.value.response.status_code == 401
    settings.general.api_key = api_key

    # Try to look up user record by email with an invalid API key,
    # which should give 401 (Unauthorized).
    api_key = settings.general.api_key
    settings.general.api_key = "invalid"
    with requests_mock.Mocker() as mocker:
        get_user_url = (
            "%s/api/v1/user/?format=json&email__iexact=testfacility%%40example.com"
        ) % settings.general.mytardis_url
        mocker.get(get_user_url, status_code=401)
        with pytest.raises(HTTPError) as excinfo:
            _ = User.get_user_by_email(owner.email)
        assert excinfo.value.response.status_code == 401
    settings.general.api_key = api_key

    # Test Getters which act differently when the user folder name
    # can't be matched to a MyTardis user account:
    username = owner.username
    owner.username = None
    assert owner.username == User.user_not_found_string
    owner.username = username

    full_name = owner.full_name
    owner.full_name = None
    assert owner.full_name == User.user_not_found_string
    owner.full_name = full_name

    email = owner.email
    owner.email = None
    assert owner.email == User.user_not_found_string
    owner.email = email

    # get_value_for_key is used to display User field values
    # in the Users or Folders view:

    assert owner.get_value_for_key("email") == owner.email

    email = owner.email
    owner.email = None
    owner.user_not_found_in_mytardis = True
    assert owner.get_value_for_key("email") == User.user_not_found_string
    owner.user_not_found_in_mytardis = False
    owner.email = email

    assert not owner.get_value_for_key("invalid")

    with requests_mock.Mocker() as mocker:
        get_user_url = (
            "%s/api/v1/user/?format=json&username=INVALID_USER"
            % settings.general.mytardis_url
        )
        mocker.get(get_user_url, text=EMPTY_LIST_RESPONSE)
        user = User.get_user_by_username("INVALID_USER")
        assert not user

    with requests_mock.Mocker() as mocker:
        get_user_url = (
            "%s/api/v1/user/?format=json&email__iexact=invalid%%40email.com"
        ) % settings.general.mytardis_url
        mocker.get(get_user_url, text=EMPTY_LIST_RESPONSE)
        user = User.get_user_by_email("invalid@email.com")
        assert not user
