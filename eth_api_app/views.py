import os

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import CreateWalletSerializer, WalletModelSerializer, TransactionSerializer
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()
INFURA_KEY = os.environ.get("INFURA_KEY", "INFURA_KEY")
infura_url = f'https://sepolia.infura.io/v3/{INFURA_KEY}'
w3 = Web3(Web3.HTTPProvider(infura_url))


class WalletListCreateAPIView(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'POST':
            serializer_class = CreateWalletSerializer
        else:
            serializer_class = WalletModelSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        # https://web3py.readthedocs.io/en/stable/web3.eth.account.html#creating-a-private-key
        acc = w3.eth.account.create()

        wallet = Wallet.objects.create(
            public_key=acc.address,
            private_key=w3.to_hex(acc._private_key)
        )

        response = super().create(request, *args, **kwargs)
        data = {
            'id': wallet.id,
            'currency': response.data['currency'],
            'public_key': wallet.public_key,
        }
        return Response(data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        data = []
        for wallet_serializer in serializer.data:
            # https://web3py.readthedocs.io/en/stable/examples.html#checking-the-balance-of-an-account
            balance_wei = w3.eth.get_balance(wallet_serializer['public_key'])
            balance_eth = w3.from_wei(balance_wei, 'ether')

            wallet_info = {
                'id': wallet_serializer['id'],
                'currency': 'ETH',
                'public_key': wallet_serializer['public_key'],
                'balance': balance_eth
            }
            data.append(wallet_info)

        return Response(data, status=status.HTTP_200_OK)


class TransactionView(APIView):
    serializer_class = TransactionSerializer

    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            sender_wallet = serializer.validated_data['from']
            receiver_wallet = serializer.validated_data['to']
            amount = serializer.validated_data.get('amount')

            try:
                sender_wallet_instance = Wallet.objects.get(public_key=sender_wallet)
                receiver_wallet_instance = Wallet.objects.get(public_key=receiver_wallet)
            except Wallet.DoesNotExist:
                return Response({'error': 'Invalid sender or receiver wallet'}, status=status.HTTP_400_BAD_REQUEST)

            balance = w3.eth.get_balance(sender_wallet_instance.public_key)
            balance = w3.from_wei(balance, 'ether')

            if balance < amount:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

            # https://web3py.readthedocs.io/en/stable/transactions.html
            private_key = sender_wallet_instance.private_key
            amount_in_wei = w3.to_wei(amount, 'ether')

            nonce = w3.eth.get_transaction_count(sender_wallet_instance.public_key)

            transaction = {
                'to': receiver_wallet_instance.public_key,
                'value': amount_in_wei,
                'gas': 21000,
                'gasPrice': w3.to_wei('50', 'gwei'),
                'nonce': nonce,
            }

            signed_transaction = w3.eth.account.sign_transaction(transaction, private_key)
            tx_hash = w3.eth.send_raw_transaction(signed_transaction.rawTransaction)

            return Response({'hash': tx_hash.hex()}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
