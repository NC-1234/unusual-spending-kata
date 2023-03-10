import pytest

from src.interfaces.presenters.email_service import EmailPresenter
from src.credit_repository.credit_repository import CreditRepository
from src.usecase.payment_usecase import PaymentUsecase


@pytest.fixture
def mock_credit_repository(mocker):
    return mocker.Mock(CreditRepository)


@pytest.fixture()
def in_memory_credit_repository():
    return CreditRepository()


@pytest.fixture
def mock_email_service(mocker):
    return mocker.Mock(EmailPresenter)

@pytest.fixture
def in_memory_payment_usecase(mock_credit_repository, mock_email_service):
    return PaymentUsecase(mock_credit_repository, mock_email_service)