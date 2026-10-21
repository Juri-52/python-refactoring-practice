# リファクタリングの記録

氏名：柳川珠里

## 1. 元のコードの読み取り

- 直接実行したとき、最初に呼び出される関数： Book
- 利用者と本のデータが、料金計算まで渡される流れ： Loan(利用者,本,延滞日数,学生か？)をget_feeに受け渡す
- Mariaの料金が500円になる計算の順序： 150円/日 * 15日 = 2250円 1000円を超えたので1000円 学生なので50%引きで500円
- 同じBookを参照するLoanが、計算のたびにBookの値を変更してはいけない理由：結果が変わってしまうから

## 2. 変更例1

対象ファイル・メソッド：loan.py/get_fee

変更の目的：メソッドの分割・マジックナンバーの使用

### 変更前

```python
# 自分が変更した箇所の変更前のコードを記載する。
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
```

### 変更後

```python
# 対応する変更後のコードを記載する。
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
```

## 3. 変更例2

対象ファイル・関数：main.py/main

変更の目的：printを関数化

### 変更前

```python
# 自分が変更した箇所の変更前のコードを記載する。
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
```

### 変更後

main.py
```python - main.py
# 対応する変更後のコードを記載する。
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
```
display.py
```python
from main import *

def print_loan(loan: Loan):
    print(f"利用者: {loan.borrower}")
    print(f"本: {loan.book.title}")
    print(f"延滞日数: {loan.overdue_days}日")
    print(f"学生: {'はい' if loan.is_student else 'いいえ'}")
    print(f"延滞料金: {loan.get_fee()}円")
    print("---")
```

## 4. 実行確認

- 変更前のテスト結果：
```
12 passed in 0.02s
```
- 変更後のテスト結果：
```
12 passed in 0.03s
```
- expected_output.txtと、変更後の表示を比較した結果：
```text
利用者: Akira
本: Python入門
延滞日数: 3日
学生: いいえ
延滞料金: 300円
---
利用者: Maria
本: Python入門
延滞日数: 15日
学生: はい
延滞料金: 500円
---
利用者: Ren
本: データ分析
延滞日数: 0日
学生: いいえ
延滞料金: 0円
---
```
```
利用者: Akira
本: Python入門
延滞日数: 3日
学生: いいえ
延滞料金: 300円
---
利用者: Maria
本: Python入門
延滞日数: 15日
学生: はい
延滞料金: 500円
---
利用者: Ren
本: データ分析
延滞日数: 0日
学生: いいえ
延滞料金: 0円
---
```
- 最終的な各ファイルの役割：
```
book.py:貸出資料のデータを作成
loan.py:利用料金を計算
display.py:画面に表示する内容を作成
main:各メソッドに受け渡す利用者・貸出資料・利用状況のデータを作成し、返り値を画面に表示する
```