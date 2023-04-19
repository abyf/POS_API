from django.test import TestCase
import uuid
from .models import CardHolder

class CardholderModelTest(TestCase):
    def test_cardholder_creation(self):
        name="John Doe"
        address="123 Main St"
        phone="555-1234"
        email = "johndoe@example.com"

        cardholder = CardHolder.objects.create(name=name,address=address, phone=phone,email=email)

        self.assertIsNotNone(cardholder.qr_code)
        self.assertIsNotNone(cardholder.alias)
        self.assertEqual(len(cardholder.alias),8)
        self.assertEqual(cardholder.balance,0)
        self.assertEqual(len(cardholder.group),"cardholders")
        self.assertEqual(len(cardholder.is_active),True)
        self.assertEqual(len(cardholder.name),name)
        self.assertEqual(len(cardholder.address),address)
        self.assertEqual(len(cardholder.phone),phone)
        self.assertEqual(len(cardholder.email),email)

    def test_create_cardholder_optional_fields(self):
        cardholder = CardHolder(name="Jane Doe")

        self.assertIsNotNone(cardholder.qr_code)
        self.assertIsNotNone(cardholder.alias)
        self.assertIsNotNone(cardholder.balance)
        self.assertEqual(len(cardholder.name),"Jane Doe")
        self.assertEqual(len(cardholder.address),address)
        self.assertEqual(len(cardholder.phone),phone)
        self.assertEqual(len(cardholder.email),email)

    def test_cardholder_duplicate_qr_code(self):
        cardholder1 = CardHolder(name="John Doe")
        cardholder2 = CardHolder(name="Jane Doe", qr_code=cardholder1.qr_code)
        self.assertNotEqual(cardholder1.qr_code, cardholder2.qr_code)

    def test_cardholder_duplicate_alias(self):
        cardholder1 = CardHolder(name="John Doe")
        cardholder2 = CardHolder(name="Jane Doe", alias=cardholder1.alias)
        self.assertNotEqual(cardholder1.alias, cardholder2.alias)

    def test_create_cardholder_invalid_phone(self):
        with self.assertRaises(ValueError):
            CardHolder(name="John Doe", phone="123-4567")

    def test_create_cardholder_invalid_qr_code(self):
        with self.assertRaises(ValueError):
            CardHolder(name="John Doe", qr_code="not-a-uuid")

    def test_create_cardholder_no_qr_code(self):
        with self.assertRaises(ValueError):
            CardHolder(name="John Doe", qr_code=None)

    def test_create_cardholder_multiple_qr_codes(self):
        cardholder = CardHolder(name="John Doe")
        with self.assertRaises(AttributeError):
            cardholder.qr_codes = str(uuid.uuid4())

    def test_create_cardholder_multiple_aliases(self):
        cardholder = CardHolder(name="John Doe")
        with self.assertRaises(AttributeError):
            cardholder.alias = "new_alias"

    def test_create_cardholder_invalid_balance(self):
        cardholder = CardHolder(name="John Doe")
        with self.assertRaises(AttributeError):
            cardholder.balance = 100

    def test_create_cardholder_invalid_is_active(self):
        cardholder = CardHolder(name="John Doe")
        with self.assertRaises(AttributeError):
            cardholder.is_active = False
