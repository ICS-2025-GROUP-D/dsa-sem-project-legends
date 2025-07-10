from datetime import datetime

class FeeStack:
    def __init__(self):
        self.stack = []
    
    def push(self, student_id, amount):
        payment = {
            'student_id': student_id,
            'amount': float(amount),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.stack.append(payment)
        return payment
    
    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None
    
    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None
    
    def is_empty(self):
        return len(self.stack) == 0
    
    def get_balance(self):
        return sum(payment['amount'] for payment in self.stack)
    
    def get_all_payments(self):
        return self.stack[::-1]  # Return reversed for LIFO display

def main():
    fee_stack = FeeStack()
    
    while True:
        print("\n=== Student Fee Manager ===")
        print("1. Add Payment")
        print("2. View Current Balance")
        print("3. View Payment History")
        print("4. Exit")
        choice = input("Please enter your choice (1-4): ").strip()
        
        if choice == '1':
            student_id = input("Enter Student ID (e.g., S001): ").strip()
            if not student_id:
                print("Error: Student ID cannot be empty.")
                continue
            try:
                amount = float(input("Enter Amount Paid (e.g., 100.50): ").strip())
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                fee_stack.push(student_id, amount)
                print("Payment added successfully!")
            except ValueError as e:
                print(f"Error: {e if str(e) else 'Invalid amount format.'}")
        
        elif choice == '2':
            balance = fee_stack.get_balance()
            print(f"Current Balance: ${balance:.2f}")
        
        elif choice == '3':
            payments = fee_stack.get_all_payments()
            if not payments:
                print("No payments recorded.")
            else:
                print("\nPayment History (Newest First):")
                for payment in payments:
                    print(f"Student ID: {payment['student_id']}, Amount: ${payment['amount']:.2f}, "
                          f"Time: {payment['timestamp']}")
        
        elif choice == '4':
            print("Exiting... Thank you!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main()