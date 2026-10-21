from dataclasses import dataclass

from book import Book


# 動作する変更前のコードです。料金のルールを保ちながら整理してください。
MAX_LATE_FEE = 1000
STUDENT_DISCOUNT_PERCENT = 50

@dataclass
class Loan:
    borrower: str
    book: Book
    overdue_days: int
    is_student: bool = False

    def get_capped_fee(self) -> int:
        if self.overdue_days == 0:
            return 0
        else:
            if self.book.daily_late_fee * self.overdue_days < MAX_LATE_FEE:
                return self.book.daily_late_fee * self.overdue_days
            else:
                return MAX_LATE_FEE

    def get_fee(self) -> int:
        if self.is_student:
            return int(self.get_capped_fee() * (1 - STUDENT_DISCOUNT_PERCENT / 100))
        else:
            return self.get_capped_fee()
