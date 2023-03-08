from abc import abstractmethod
from typing import Protocol, runtime_checkable

from src.domain.credit_history import MonthlyExpenditure
from src.domain.month_status import MonthStatus
from src.domain.payment import Category, Payment
from src.interfaces.presenters.email_service import EmailOutputBoundary
from src.repository.credit_repository import Repository

@runtime_checkable
class PaymentInputBoundary(Protocol):
    @abstractmethod
    def add_payment(self, user_id: str, payment: Payment, month: MonthStatus):
        pass

    @abstractmethod
    def fetch_payment(self, user_id: str, month: MonthStatus) -> MonthlyExpenditure:
        pass

    @abstractmethod
    def calculate_over_spending(self, current_monthly_spending: MonthlyExpenditure,
                                previous_monthly_spending: MonthlyExpenditure) -> dict:
        pass

    @abstractmethod
    def compose_email(self, overspent_categories) -> str:
        pass


class PaymentUsecase(PaymentInputBoundary):

    def __init__(self, credit_repository: Repository, email_service: EmailOutputBoundary):
        self.__credit_repository = credit_repository
        self.__total_spent_by_category_current_month: dict[Category, float] = {}
        self.__total_spent_by_category_previous_month: dict[Category, float] = {}
        self.__category_overspent = {}
        self.__email_service = email_service

    def add_payment(self, user_id: str, payment: Payment, month: MonthStatus):
        return self.__credit_repository.add_payment_for_month(user_id=user_id, payment=payment, month=month)

    def fetch_payment(self, user_id: str, month: MonthStatus) -> MonthlyExpenditure:
        return self.__credit_repository.fetch_payments_by_month(user_id=user_id, month=month)

    def calculate_over_spending(self, current_monthly_spending: MonthlyExpenditure,
                                previous_monthly_spending: MonthlyExpenditure) -> dict:

        self.__calculate_total_spent_by_category(current_monthly_spending, self.__total_spent_by_category_current_month)
        self.__calculate_total_spent_by_category(previous_monthly_spending, self.__total_spent_by_category_previous_month)
        self.__calculate_overspending_by_category()

        return self.__category_overspent

    def compose_email(self, overspent_categories) -> str:
        return self.__email_service.compose_email(overspent_categories)

    def __calculate_total_spent_by_category(self, monthly_spending: MonthlyExpenditure,
                                            total_spent_by_category: dict[Category, float]):
        if monthly_spending is None:
            return
        for payment in monthly_spending.payments:
            if payment.category in total_spent_by_category:
                total_spent_by_category[payment.category] += payment.price
            else:
                total_spent_by_category[payment.category] = payment.price

    def __calculate_overspending_by_category(self):
        for category in self.__total_spent_by_category_current_month:
            if self.__is_category_overspent(category):
                self.__category_overspent[category] = self.__total_spent_by_category_current_month[category]

    def __is_category_overspent(self, category: Category) -> bool:
        return self.__total_spent_by_category_current_month[category] / 2 >= self.__total_spent_by_category_previous_month[category]
