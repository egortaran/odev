import os

from django.test import TestCase
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
INFURA_KEY = os.environ.get("INFURA_KEY", "INFURA_KEY")
infura_url = f'https://mainnet.infura.io/v3/{INFURA_KEY}'


class Web3ConnectionTestCase(TestCase):
    def setUp(self):
        self.w3 = Web3(Web3.HTTPProvider(infura_url))

    def test_connection_web3(self):
        self.assertTrue(self.w3.is_connected())
