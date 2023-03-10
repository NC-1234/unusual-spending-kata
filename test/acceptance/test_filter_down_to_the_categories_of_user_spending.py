from src.domain.credit_history import MonthlyExpenditure
from src.domain.month_status import MonthStatus
from src.domain.payment import Category, Payment
from src.interfaces.presenters.email_service import EmailPresenter
from src.credit_repository.credit_repository import CreditRepository
from src.usecase.payment_usecase import PaymentUsecase

USER_ID = "test-user-id"
EMAIL = """Hello card user!

We have detected unusually high spending on your card in these categories:

* You spent $148.00 on groceries
* You spent $928.00 on travel

Love,

The Credit Card Company"""


def test_compose_an_e_mail_message_to_the_user_that_lists_the_categories_for_which_spending_was_50_per_cent_more():
    credit_repository = CreditRepository()
    email_service = EmailPresenter()
    payment_usecase = PaymentUsecase(credit_repository, email_service)

    payment_usecase.add_payment(user_id=USER_ID,
                                payment=Payment(price=70.00,
                                                description="Groceries",
                                                category=Category.GROCERIES),
                                month=MonthStatus.PREVIOUS)

    payment_usecase.add_payment(user_id=USER_ID,
                                payment=Payment(price=400.00,
                                                description="Travel",
                                                category=Category.TRAVEL),
                                month=MonthStatus.PREVIOUS)

    payment_usecase.add_payment(user_id=USER_ID,
                                payment=Payment(price=148.00,
                                                description="Groceries",
                                                category=Category.GROCERIES),
                                month=MonthStatus.CURRENT)

    payment_usecase.add_payment(user_id=USER_ID,
                                payment=Payment(price=928.00,
                                                description="Travel",
                                                category=Category.TRAVEL),
                                month=MonthStatus.CURRENT)

    current_monthly_spending: MonthlyExpenditure = payment_usecase.fetch_payment(user_id=USER_ID, month=MonthStatus.CURRENT)
    previous_monthly_spending: MonthlyExpenditure = payment_usecase.fetch_payment(user_id=USER_ID, month=MonthStatus.PREVIOUS)

    overspent_categories = payment_usecase.calculate_over_spending(
        current_monthly_spending=current_monthly_spending, previous_monthly_spending=previous_monthly_spending)
    result = payment_usecase.compose_email(overspent_categories=overspent_categories)

    assert type(current_monthly_spending) is MonthlyExpenditure
    assert type(previous_monthly_spending) is MonthlyExpenditure
    assert type(overspent_categories) is dict
    assert result == EMAIL


