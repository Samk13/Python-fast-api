from app.calc import add, BankAccount, InsufficientFunds
import pytest


@pytest.mark.parametrize("a,b,expected", [(1, 2, 3), (2, 3, 5), (-3, -4, -7)])
def test_add(a, b, expected):
    assert add(a, b) == expected


@pytest.fixture
def zero_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(100)


def test_bank_account_balance(bank_account):
    assert bank_account.balance == 100


def test_bank_account_default_balance(zero_account):
    assert zero_account.balance == 0


def test_bank_account_withdraw(bank_account):
    bank_account.withdraw(100)
    assert bank_account.balance == 0


def test_bank_account_withdraw_negative(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(111)


def test_bank_trsnsaction_withdraw(bank_account):
    bank_account.withdraw(100)
    assert bank_account.balance == 0
