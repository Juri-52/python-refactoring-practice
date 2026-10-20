from book import Book
from loan import Loan


# 変更前と変更後で同じルールを確認するためのテストです。
# テストを通すために、正しい期待値を変更しないでください。
def test_no_overdue_fee() -> None:
    loan = Loan("Akira", Book("Python入門", 100), 0)

    assert loan.get_fee() == 0


def test_student_with_no_overdue_fee() -> None:
    loan = Loan("Maria", Book("Python入門", 100), 0, True)

    assert loan.get_fee() == 0


def test_one_day_fee() -> None:
    loan = Loan("Ren", Book("データ分析", 150), 1)

    assert loan.get_fee() == 150


def test_fee_below_limit() -> None:
    loan = Loan("Akira", Book("アルゴリズム", 111), 9)

    assert loan.get_fee() == 999


def test_fee_at_limit() -> None:
    loan = Loan("Akira", Book("Python入門", 100), 10)

    assert loan.get_fee() == 1000


def test_fee_above_limit() -> None:
    loan = Loan("Akira", Book("Python入門", 100), 11)

    assert loan.get_fee() == 1000


def test_student_discount_below_limit() -> None:
    loan = Loan("Maria", Book("Python入門", 100), 3, True)

    assert loan.get_fee() == 150


def test_student_discount_at_limit() -> None:
    loan = Loan("Maria", Book("Python入門", 100), 10, True)

    assert loan.get_fee() == 500


def test_limit_is_applied_before_student_discount() -> None:
    loan = Loan("Maria", Book("Python入門", 100), 15, True)

    assert loan.get_fee() == 500


def test_student_fee_is_rounded_down() -> None:
    loan = Loan("Maria", Book("コンピューター入門", 151), 1, True)

    assert loan.get_fee() == 75


def test_repeated_calculation_keeps_loan_and_book_unchanged() -> None:
    book = Book("Python入門", 100)
    loan = Loan("Maria", book, 15, True)

    first_fee = loan.get_fee()
    second_fee = loan.get_fee()

    assert first_fee == 500
    assert second_fee == 500
    assert loan.borrower == "Maria"
    assert loan.book is book
    assert loan.overdue_days == 15
    assert loan.is_student is True
    assert book.title == "Python入門"
    assert book.daily_late_fee == 100


def test_loans_can_share_a_book_without_affecting_each_other() -> None:
    book = Book("Python入門", 100)
    student_loan = Loan("Maria", book, 15, True)
    regular_loan = Loan("Akira", book, 2)

    assert student_loan.book is regular_loan.book
    assert regular_loan.get_fee() == 200
    assert student_loan.get_fee() == 500
    assert regular_loan.get_fee() == 200
    assert student_loan.get_fee() == 500
    assert book.daily_late_fee == 100
    assert student_loan.overdue_days == 15
    assert regular_loan.overdue_days == 2
    assert student_loan.is_student is True
    assert regular_loan.is_student is False
