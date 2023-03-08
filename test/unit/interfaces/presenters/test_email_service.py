from src.domain.payment import Category
from src.interfaces.presenters.email_service import EmailPresenter


def test_compose_email_should_create_an_email_for_user_overspent_categories():

    test_overspent_categories = {Category.GOLF: 999.99}
    expected_email = """Hello card user!

We have detected unusually high spending on your card in these categories:

* You spent $999.99 on golf

Love,

The Credit Card Company"""


    result = EmailPresenter().compose_email(test_overspent_categories)
    assert result == expected_email
