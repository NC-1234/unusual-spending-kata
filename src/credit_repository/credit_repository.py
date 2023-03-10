from abc import abstractmethod
from typing import Protocol, NewType, runtime_checkable

from src.domain.credit_history import MonthlyExpenditure
from src.domain.month_status import MonthStatus
from src.domain.payment import Payment

UserId = NewType('UserId', str)

@runtime_checkable
class Repository(Protocol):
    @abstractmethod
    def fetch_payments_by_month(self, user_id: UserId, month: MonthStatus) -> MonthlyExpenditure | None:
        pass

    @abstractmethod
    def add_payment_for_month(self, user_id: UserId, payment: Payment, month: MonthStatus):
        pass


class CreditRepository:
    __credit_data: dict[UserId, list[MonthlyExpenditure]] = {}

    def fetch_payments_by_month(self, user_id: UserId, month: MonthStatus) -> MonthlyExpenditure | None:
        if user_id not in self.__credit_data:
            return None

        user_credit_history = self.__credit_data[user_id]
        for monthly_payment in user_credit_history:
            if monthly_payment.month_status == month:
                return monthly_payment

    def add_payment_for_month(self, user_id: UserId, payment: Payment, month: MonthStatus):
        if user_id in self.__credit_data.keys():
            self.__add_payment_to_existing_month(user_id, payment, month)
        else:
            self.__create_new_monthly_expenditure(user_id, payment, month)

    def __add_payment_to_existing_month(self, user_id: UserId, payment: Payment, month: MonthStatus):
        for monthly_expenditure in self.__credit_data[user_id]:
            if monthly_expenditure.month_status == month:
                monthly_expenditure.payments.append(payment)
                break
        else:
            self.__credit_data[user_id].append(MonthlyExpenditure(month, [payment]))

    @classmethod
    def __create_new_monthly_expenditure(self, user_id: UserId, payment: Payment, month: MonthStatus):
        self.__credit_data[user_id] = [MonthlyExpenditure(month, [payment])]
