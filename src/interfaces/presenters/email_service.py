from abc import abstractmethod

from src.domain.payment import Category


class EmailOutputBoundary:
    @abstractmethod
    def compose_email(self, overspent_categories: dict[Category, float]) -> str:
        pass

class EmailPresenter(EmailOutputBoundary):
    def compose_email(self, overspent_categories: dict[Category, float]) -> str:
        email_body = "\n".join([
            "Hello card user!",
            "",
            "We have detected unusually high spending on your card in these categories:",
            "",
            *[f"* You spent ${price:.2f} on {category.value}" for category, price in overspent_categories.items()],
            "",
            "Love,",
            "",
            "The Credit Card Company"
        ])
        return email_body