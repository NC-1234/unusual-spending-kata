from src.domain.credit_history import MonthlyExpenditure
from src.domain.month_status import MonthStatus
from src.domain.payment import Payment, Category
from src.usecase.payment_usecase import PaymentUsecase

TEST_USER_ID = 'test_user_id'
GOLF_PAYEMENT = Payment(399.99, "Golf Clubs", Category.GOLF)

def test_add_payment_for_user_should_add_payment_for_a_given_month(mock_credit_repository, mock_email_service):

    expected_expenditure = MonthlyExpenditure(month_status=MonthStatus.CURRENT,
                                              payments=[GOLF_PAYEMENT]
                                              )

    mock_credit_repository.fetch_payments_by_month.return_value = expected_expenditure

    PaymentUsecase(mock_credit_repository, mock_email_service).add_payment(TEST_USER_ID, payment=GOLF_PAYEMENT, month=MonthStatus.CURRENT)

    mock_credit_repository.add_payment_for_month.assert_called_once_with(user_id=TEST_USER_ID, payment=GOLF_PAYEMENT,
                                                                         month=MonthStatus.CURRENT)

    result = PaymentUsecase(mock_credit_repository, mock_email_service).fetch_payment(TEST_USER_ID, MonthStatus.CURRENT)

    assert result == expected_expenditure
    assert type(result) == MonthlyExpenditure

def test_fetch_payment_for_user_should_return_current_monthly_expenditure(mock_credit_repository, mock_email_service):
    expected_expenditure = MonthlyExpenditure(month_status=MonthStatus.CURRENT,
                                              payments=[GOLF_PAYEMENT]
                                              )
    mock_credit_repository.fetch_payments_by_month.return_value = expected_expenditure

    result = PaymentUsecase(mock_credit_repository, mock_email_service).fetch_payment(TEST_USER_ID, MonthStatus.CURRENT)

    mock_credit_repository.fetch_payments_by_month.assert_called_once_with(user_id=TEST_USER_ID,
                                                                           month=MonthStatus.CURRENT)

    assert result == expected_expenditure
    assert type(result) == MonthlyExpenditure


def test_return_all_categories_which_a_user_has_over_spent_by_50_per_cent(mock_credit_repository, mock_email_service):
    expected_categories = {Category.GOLF: 799.98}
    previous_month = MonthlyExpenditure(month_status=MonthStatus.PREVIOUS,
                                        payments=[GOLF_PAYEMENT]
                                        )

    current_month = MonthlyExpenditure(month_status=MonthStatus.CURRENT,
                                       payments=[GOLF_PAYEMENT,
                                                 GOLF_PAYEMENT])
    result = PaymentUsecase(mock_credit_repository, mock_email_service).calculate_over_spending(
        current_monthly_spending=current_month,
        previous_monthly_spending=previous_month)

    assert result == expected_categories


def test_compose_email_should_create_an_email_for_user_overspent_categories(mock_credit_repository, mock_email_service):
    expected_email = """Hello card user!

    We have detected unusually high spending on your card in these categories:

    * You spent $999.99 on golf

    Love,

    The Credit Card Company"""
    test_overspent_categories = {Category.GOLF: 999.99}

    mock_email_service.compose_email.return_value = expected_email

    result = PaymentUsecase(mock_credit_repository, mock_email_service).compose_email(test_overspent_categories)

    mock_email_service.compose_email.assert_called_once_with(test_overspent_categories)

    assert result == expected_email
