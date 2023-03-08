import pytest

from src.interfaces.presenters.email_service import EmailPresenter
from src.repository.credit_repository import CreditRepository


@pytest.fixture
def mock_credit_repository(mocker):
    return mocker.Mock(CreditRepository)


@pytest.fixture()
def in_memory_credit_repository():
    return CreditRepository()


@pytest.fixture
def mock_email_service(mocker):
    return mocker.Mock(EmailPresenter)