from rest_framework import serializers
from .models import Wallet


class CreateWalletSerializer(serializers.Serializer):
    currency = serializers.CharField(required=True)

    def create(self, validated_data):
        return validated_data

    def validate_currency(self, value):
        if value != 'ETH':
            raise serializers.ValidationError('Currency can be only ETH')
        return value


class WalletModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['id', 'public_key']


class TransactionSerializer(serializers.Serializer):
    from_ = serializers.CharField(required=True, source='from')
    to = serializers.CharField(required=True)
    currency = serializers.CharField(required=True)
    amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=5)

    def validate_currency(self, value):
        if value != 'ETH':
            raise serializers.ValidationError('Currency must be only ETH')
        return value

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError('Amount must be more than 0')
        return value
