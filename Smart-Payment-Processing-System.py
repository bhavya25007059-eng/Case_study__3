from abc import ABC, abstractmethod

# --- Abstract Base Class ---
class Payment(ABC):
    def __init__(self, user_name):
        self.user_name = user_name
        self.original_amount = 0
        self.final_amount = 0

    @abstractmethod
    def pay(self, amount):
        pass

    def generate_receipt(self):
        print("\n" + "="*30)
        print("       PAYMENT RECEIPT")
        print("="*30)
        print(f"Customer: {self.user_name}")
        print(f"Original Amount:  ₹{self.original_amount:.2f}")
        print(f"Final Paid:      ₹{self.final_amount:.2f}")
        print("="*30 + "\n")

# --- Concrete Implementations ---

class CreditCardPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        gateway_fee = amount * 0.02
        gst = gateway_fee * 0.18
        self.final_amount = amount + gateway_fee + gst
        print(f">> Processing Credit Card (2% Fee + 18% GST on Fee)...")
        self.generate_receipt()

class UPIPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        cashback = 50 if amount > 1000 else 0
        self.final_amount = amount - cashback
        print(f">> Processing UPI...")
        if cashback > 0:
            print(f"✨ Cashback of ₹{cashback} applied!")
        self.generate_receipt()

class PayPalPayment(Payment):
    def pay(self, amount):
        self.original_amount = amount
        self.final_amount = amount + (amount * 0.03) + 20
        print(f">> Processing PayPal (3% Int'l Fee + ₹20 Conversion)...")
        self.generate_receipt()

class WalletPayment(Payment):
    def __init__(self, user_name, balance):
        super().__init__(user_name)
        self.balance = balance

    def pay(self, amount):
        self.original_amount = amount
        if amount > self.balance:
            print(f"❌ Transaction Failed: Insufficient Balance (Available: ₹{self.balance})")
        else:
            self.balance -= amount
            self.final_amount = amount
            print(f">> Wallet Payment Successful!")
            self.generate_receipt()
            print(f"New Wallet Balance: ₹{self.balance}")

# --- Polymorphism in Action ---
def process_payment(payment_method_object, amount):
    payment_method_object.pay(amount)

# --- Interactive Main Loop ---
def main():
    name = input("Enter your name: ")
    # Initialize a wallet with some default money for the demo
    wallet_obj = WalletPayment(name, 2000) 
    
    while True:
        print(f"--- Smart Payment System ---")
        print("1. Credit Card")
        print("2. UPI")
        print("3. PayPal")
        print("4. Digital Wallet")
        print("5. Exit")
        
        choice = input("Select payment method (1-5): ")
        
        if choice == '5':
            print("Thank you for using the system!")
            break
            
        try:
            amt = float(input("Enter amount to pay: ₹"))
            
            if choice == '1':
                process_payment(CreditCardPayment(name), amt)
            elif choice == '2':
                process_payment(UPIPayment(name), amt)
            elif choice == '3':
                process_payment(PayPalPayment(name), amt)
            elif choice == '4':
                process_payment(wallet_obj, amt)
            else:
                print("Invalid selection. Try again.")
        except ValueError:
            print("Invalid input. Please enter a numeric value for the amount.")

if __name__ == "__main__":
    main()