from dataclasses import dataclass

from book import Book


# 動作する変更前のコードです。料金のルールを保ちながら整理してください。
@dataclass
class Loan:
    borrower: str
    book: Book
    overdue_days: int
    is_student: bool = False

    def get_fee(self) -> int:
        x = 0
        if self.overdue_days > 0:
            if self.is_student:
                x = self.book.daily_late_fee * self.overdue_days
                if x > 1000:
                    x = 1000
                x = x * (100 - 50) // 100
            else:
                x = self.book.daily_late_fee * self.overdue_days
                if x > 1000:
                    x = 1000
        else:
            x = 0
        return x
