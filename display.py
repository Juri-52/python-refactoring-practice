from loan import Loan

def print_loan(loan: Loan):
    print(f"利用者: {loan.borrower}")
    print(f"本: {loan.book.title}")
    print(f"延滞日数: {loan.overdue_days}日")
    print(f"学生: {'はい' if loan.is_student else 'いいえ'}")
    print(f"延滞料金: {loan.get_fee()}円")
    print("---")