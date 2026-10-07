# ==========================================
# Task 5: Abstraction
# ==========================================

from abc import ABC, abstractmethod


class Payment(ABC):

    @abstractmethod
    def process_payment(self, amount):
        pass


class CreditCardPayment(Payment):

    def process_payment(self, amount):
        print("=" * 40)
        print("       CREDIT CARD PAYMENT")
        print("=" * 40)
        print(f"Payment Amount: {amount}")
        print("Status: Payment processed")
        print("=" * 40)


class UPIPayment(Payment):

    def process_payment(self, amount):
        print("=" * 40)
        print("           UPI PAYMENT")
        print("=" * 40)
        print(f"Payment Amount: {amount}")
        print("Status: Payment processed")
        print("=" * 40)


credit = CreditCardPayment()
upi = UPIPayment()

credit.process_payment(5000)
upi.process_payment(2000)