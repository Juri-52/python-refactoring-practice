from book import Book
from loan import Loan
from display import *

def main() -> None:
    book1 = Book("Python入門", 100)
    book2 = Book("データ分析", 150)

    loan1 = Loan("Akira", book1, 3)
    loan2 = Loan("Maria", book1, 15, True)
    loan3 = Loan("Ren", book2, 0)

    print_loan(loan1)
    print_loan(loan2)
    print_loan(loan3)

if __name__ == "__main__":
    main()
