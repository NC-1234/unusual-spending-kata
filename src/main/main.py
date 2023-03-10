from lagom import Container

from src.domain.month_status import MonthStatus
from src.domain.payment import Payment, Category
from src.interfaces.presenters.email_service import EmailOutputBoundary, EmailPresenter
from src.credit_repository.credit_repository import CreditRepository, Repository
from src.usecase.payment_usecase import PaymentInputBoundary, PaymentUsecase


def main():

    container = Container(log_undefined_deps=True)
    container[Repository] = CreditRepository()
    container[EmailOutputBoundary] = EmailPresenter()
    container[PaymentInputBoundary] = PaymentUsecase(credit_repository=container[Repository],
                                                     email_service=container[EmailOutputBoundary])

    app = container[PaymentInputBoundary]

    app.add_payment(user_id="123", payment=Payment(price=10.00, description="Cinema", category=Category.ENTERTAINMENT),
                    month=MonthStatus.PREVIOUS)
    app.add_payment(user_id="123", payment=Payment(price=10.00, description="Cinema", category=Category.ENTERTAINMENT),
                    month=MonthStatus.CURRENT)
    app.add_payment(user_id="123", payment=Payment(price=10.00, description="Cinema", category=Category.ENTERTAINMENT),
                    month=MonthStatus.CURRENT)
    app.add_payment(user_id="123", payment=Payment(price=10.00, description="Cinema", category=Category.ENTERTAINMENT),
                    month=MonthStatus.CURRENT)
    app.add_payment(user_id="123", payment=Payment(price=10.00, description="Cinema", category=Category.ENTERTAINMENT),
                    month=MonthStatus.CURRENT)

    current_monthly_spending = app.fetch_payment(user_id="123", month=MonthStatus.CURRENT)
    previous_monthly_spending = app.fetch_payment(user_id="123", month=MonthStatus.PREVIOUS)

    overspent_categories = app.calculate_over_spending(
        current_monthly_spending=current_monthly_spending, previous_monthly_spending=previous_monthly_spending)

    print(app.compose_email(overspent_categories=overspent_categories))


if __name__ == "__main__":
    main()
