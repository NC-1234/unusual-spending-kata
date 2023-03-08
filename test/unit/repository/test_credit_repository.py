from src.domain.credit_history import MonthlyExpenditure
from src.domain.month_status import MonthStatus
from src.domain.payment import Payment, Category

TEST_USER_ID_BOB = 'Test_user_123'
TEST_USER_ID_DAVE = 'Test_user_456'
TEST_CURRENT_MONTH_STATUS = MonthStatus.CURRENT
TEST_PREVIOUS_MONTH_STATUS = MonthStatus.PREVIOUS
TEST_PAYMENT = Payment(price=399.99, description="Golf Clubs", category=Category.GOLF)
TEST_ENTERTAINMENT_PAYMENT = Payment(price=12.99, description="Cinema", category=Category.ENTERTAINMENT)


def test_should_fetch_empty_expenditure_for_user_when_no_payments_made_exist(
        in_memory_credit_repository,
):
    result = in_memory_credit_repository.fetch_payments_by_month(user_id=TEST_USER_ID_BOB, month=TEST_CURRENT_MONTH_STATUS)
    assert result is None


def test_credit_repository_should_fetch_expenditure_for_a_user(in_memory_credit_repository):
    in_memory_credit_repository.add_payment_for_month(user_id=TEST_USER_ID_BOB, payment=TEST_PAYMENT, month=TEST_CURRENT_MONTH_STATUS)
    result = in_memory_credit_repository.fetch_payments_by_month(user_id=TEST_USER_ID_BOB, month=MonthStatus.CURRENT)

    assert type(result) == MonthlyExpenditure
    assert len(result.payments) == 1
    assert result.month_status == TEST_CURRENT_MONTH_STATUS
    assert result.payments == [TEST_PAYMENT]


def test_credit_repository_should_add_payment_to_an_existing_monthly_expenditure_for_a_user(in_memory_credit_repository):
    in_memory_credit_repository.add_payment_for_month(user_id=TEST_USER_ID_BOB, payment=TEST_ENTERTAINMENT_PAYMENT, month=TEST_PREVIOUS_MONTH_STATUS)
    result = in_memory_credit_repository.fetch_payments_by_month(user_id=TEST_USER_ID_BOB, month=MonthStatus.PREVIOUS)

    assert type(result) == MonthlyExpenditure
    assert len(result.payments) == 1
    assert result.month_status == TEST_PREVIOUS_MONTH_STATUS
    assert TEST_ENTERTAINMENT_PAYMENT in result.payments

def test_credit_repository_should_add_monthly_expenditure_when_one_does_not_exist_for_a_user(in_memory_credit_repository):
    in_memory_credit_repository.add_payment_for_month(user_id=TEST_USER_ID_BOB, payment=TEST_ENTERTAINMENT_PAYMENT, month=TEST_CURRENT_MONTH_STATUS)
    result = in_memory_credit_repository.fetch_payments_by_month(user_id=TEST_USER_ID_BOB, month=MonthStatus.CURRENT)

    assert type(result) == MonthlyExpenditure
    assert len(result.payments) == 2
    assert TEST_ENTERTAINMENT_PAYMENT in result.payments

def test_should_add_user_with_expenditure_when_user_does_not_exist(
        in_memory_credit_repository,
):
    in_memory_credit_repository.add_payment_for_month(user_id=TEST_USER_ID_DAVE, payment=TEST_PAYMENT, month=TEST_CURRENT_MONTH_STATUS)
    result = in_memory_credit_repository.fetch_payments_by_month(user_id=TEST_USER_ID_DAVE, month=MonthStatus.CURRENT)

    assert TEST_USER_ID_DAVE in in_memory_credit_repository.credit_data
    assert type(result) == MonthlyExpenditure
    assert len(result.payments) == 1
    assert TEST_PAYMENT in result.payments

