import os

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from eth_api_app.models import Wallet
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
INFURA_KEY = os.environ.get("INFURA_KEY", "INFURA_KEY")
infura_url = f'https://mainnet.infura.io/v3/{INFURA_KEY}'


class WalletListCreateAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('WalletListCreateAPIView')
        self.w3 = Web3(Web3.HTTPProvider(infura_url))

    def test_create_wallet(self):
        initial_wallet_count = Wallet.objects.count()
        data = {
            "currency": "ETH"
        }

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Wallet.objects.count(), initial_wallet_count + 1)
        self.assertEqual(response.data.keys(), {'id', 'currency', 'public_key'})
        self.assertEqual(response.data['currency'], 'ETH')

        incorrect_data = {
            "currency": "BTC"
        }
        response = self.client.post(self.url, incorrect_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_wallets(self):
        acc = self.w3.eth.account.create()
        Wallet.objects.create(
            public_key=acc.address,
            private_key=self.w3.to_hex(acc._private_key)
        )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for wallet_data in response.data:
            self.assertEqual(wallet_data.keys(), {'id', 'currency', 'public_key', 'balance'})


class TransactionViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('TransactionView')
        self.w3 = Web3(Web3.HTTPProvider(infura_url))

    def test_post_transaction(self):
        pk = os.environ.get('PRIVATE_KEY')
        sender_wallet = self.w3.eth.account.from_key(pk)
        sender = Wallet.objects.create(
            public_key=sender_wallet.address,
            private_key=pk
        )
        self.assertEqual(sender.private_key, pk)

        receiver_wallet = self.w3.eth.account.create()
        receiver = Wallet.objects.create(
            public_key=receiver_wallet.address,
            private_key=self.w3.to_hex(receiver_wallet._private_key)
        )

        data = {
            'from_': sender.public_key,
            'to': receiver.public_key,
            'currency': 'ETH',
            'amount': 0.0001
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
