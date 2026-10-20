from book import Book
from loan import Loan


def main() -> None:
    book1 = Book("Python入門", 100)
    book2 = Book("データ分析", 150)

    loan1 = Loan("Akira", book1, 3)
    loan2 = Loan("Maria", book1, 15, True)
    loan3 = Loan("Ren", book2, 0)

    print(f"利用者: {loan1.borrower}")
    print(f"本: {loan1.book.title}")
    print(f"延滞日数: {loan1.overdue_days}日")
    print(f"学生: {'はい' if loan1.is_student else 'いいえ'}")
    print(f"延滞料金: {loan1.get_fee()}円")
    print("---")

    print(f"利用者: {loan2.borrower}")
    print(f"本: {loan2.book.title}")
    print(f"延滞日数: {loan2.overdue_days}日")
    print(f"学生: {'はい' if loan2.is_student else 'いいえ'}")
    print(f"延滞料金: {loan2.get_fee()}円")
    print("---")

    print(f"利用者: {loan3.borrower}")
    print(f"本: {loan3.book.title}")
    print(f"延滞日数: {loan3.overdue_days}日")
    print(f"学生: {'はい' if loan3.is_student else 'いいえ'}")
    print(f"延滞料金: {loan3.get_fee()}円")
    print("---")


if __name__ == "__main__":
    main()
