import unittest
from fee_manager import FeeStack

class TestFeeStack(unittest.TestCase):

    def setUp(self):
        """Create a FeeStack instance for testing."""
        self.fee_stack = FeeStack()

    def test_push_and_get_balance(self):
        """Test pushing payments and getting the balance."""
        self.fee_stack.push('S001', 100.50)
        self.fee_stack.push('S002', 200.75)
        self.assertEqual(self.fee_stack.get_balance(), 301.25)

    def test_pop(self):
        """Test popping payments from the stack."""
        payment = self.fee_stack.push('S001', 100.50)
        self.assertEqual(self.fee_stack.pop(), payment)
        self.assertTrue(self.fee_stack.is_empty())

    def test_peek(self):
        """Test peeking at the last payment without removing it."""
        self.fee_stack.push('S001', 100.50)
        self.fee_stack.push('S002', 200.75)

    def test_is_empty(self):
        """Test the is_empty method."""
        self.assertTrue(self.fee_stack.is_empty())
        self.fee_stack.push('S001', 100.50)
        self.assertFalse(self.fee_stack.is_empty())

    def test_get_all_payments(self):
        """Test retrieving all payments in LIFO order."""
        self.fee_stack.push('S001', 100.50)
        self.fee_stack.push('S002', 200.75)
        payments = self.fee_stack.get_all_payments()
        self.assertEqual(len(payments), 2)
        self.assertEqual(payments[0]['student_id'], 'S002')  # Newest first
        self.assertEqual(payments[1]['student_id'], 'S001')

if __name__ == '__main__':
    unittest.main()
