import pytest
from app.testcalculations import *

@pytest.fixture
def zero_bank_account():
  return BankAccount()

@pytest.fixture
def bank_account():
  return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected",[
  (5,5,10),
  (5,3,8),
  (10,20,30)
])
def test_add(num1, num2, expected):
  assert add(num1,num2) == expected

def test_subract():
  assert subtract(10,2) == 8

def test_multipy():
  assert multiply(5,4) == 20

def test_divide():
  assert divide(10,2) == 5

def test_bank_set_initial_amount(bank_account):
  assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
  assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
  bank_account.withdraw(20)
  assert bank_account.balance == 30

def test_bank_deposit(bank_account):
  bank_account.deposit(30)
  assert bank_account.balance == 80

def test_bank_collect_intrest(bank_account):
  bank_account.collect_interest()
  assert round(bank_account.balance,6) == 55

@pytest.mark.parametrize("deposit, withdraw, final",[
  (5,5,50),
  (5,3,52),
  (10,20,40)
])
def test_bank_transaction(bank_account,deposit,withdraw,final):
  bank_account.deposit(deposit)
  bank_account.withdraw(withdraw)
  assert bank_account.balance == final

def test_bank_insufficent_balance(zero_bank_account):
  with pytest.raises(InsufficientFunds):
    zero_bank_account.withdraw(10)

