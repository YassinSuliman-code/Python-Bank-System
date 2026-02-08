from project import Account
from project import UsernameError
from project import PasswordError
from project import InsufficientFundsError
from project import get_password
from project import get_username
from project import confirm_amount
import pytest

def test_get_password():
    assert get_password("Yaseen_12122006","Sonson32") == "Yaseen_12122006"
    assert get_password("CS50p1999$", "JohnHarvard") == "CS50p1999$"

    with pytest.raises(PasswordError):
        get_password("YASSINahmed12345$", "YassinAhmed")
    with pytest.raises(PasswordError):
        get_password("@DavidMalan1999$", "DavidMalan")

    with pytest.raises(PasswordError):
        get_password("Mario_game##", "MarioEnjoyer12")
    with pytest.raises(PasswordError):
        get_password("Dr.House911$", "CameronLove9")
    with pytest.raises(PasswordError):
        get_password("spiderman18@1", "Miles_Morales")
    with pytest.raises(PasswordError):
        get_password("SERIOUSPUNCH9000!!", "Mr.Saitama")
    with pytest.raises(PasswordError):
        get_password("JujutsuKaisen2026", "Itadori_yuji")


def test_get_username():
    assert get_username("Dr_Ahmed2026") == "Dr_Ahmed2026"
    assert get_username("Lebron.James.Jr1") == "Lebron.James.Jr1"

    with pytest.raises(UsernameError):
        get_username("1234Yassin_Soliman")
    with pytest.raises(UsernameError):
        get_username("Titus_40k_")
    with pytest.raises(UsernameError):
        get_username("MonsterHunter!")
    with pytest.raises(UsernameError):
        get_username("Hunger-Games")

def test_confirm_amount():
    account = Account("test_project1", "Yassin_12345", 1700)

    assert confirm_amount(100, account) == 100
    assert confirm_amount(550, account) == 550

    with pytest.raises(InsufficientFundsError):
        confirm_amount(1800, account)
    with pytest.raises(InsufficientFundsError):
        confirm_amount(1701, account)

    with pytest.raises(ValueError):
        confirm_amount(0, account)
    with pytest.raises(ValueError):
        confirm_amount(-200, account)

    with pytest.raises(ValueError):
        confirm_amount("One Hundred", account)
    with pytest.raises(ValueError):
        confirm_amount("Two Hundred and Fifty", account)

def test_deposit():
    account = Account("Test_project2", "HarvardCS50p!", 5000)

    account.deposit(500)
    assert account.money == 5500
    account.deposit(1000)
    assert account.money == 6500

    with pytest.raises(ValueError):
        account.deposit(-100)
    with pytest.raises(ValueError):
        account.deposit("Two Thousand")
    with pytest.raises(ValueError):
        account.deposit(0)

def test_withdraw():
    account = Account("Test_project3", "Final_test1234", 1000)

    account.withdraw(100)
    assert account.money == 900
    account.withdraw(400)
    assert account.money == 500

    with pytest.raises(ValueError):
        account.withdraw(0)
    with pytest.raises(ValueError):
        account.withdraw(-200)
    with pytest.raises(ValueError):
        account.withdraw("Three Hundred and Thirty")

    with pytest.raises(InsufficientFundsError):
        account.withdraw(2000)
    with pytest.raises(InsufficientFundsError):
        account.withdraw(700)
