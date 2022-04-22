from django.contrib.auth.models import User
from rest_framework import serializers

from backend.crm.models import Comission, Customer


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            # 'password',
            # 'last_login',
            # 'is_superuser',
            # 'is_staff',
            # 'is_active',
            # 'date_joined',
            # 'groups',
            # 'user_permissions',
        )
        ref_name = 'Custom User Serializer'


class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Customer
        fields = ('id', 'rg', 'cpf', 'cep', 'address', 'active', 'user', 'seller')
        depth = 1  # expande todas as FK

    def to_representation(self, instance):
        '''
        Representação personalizada para RG, CPF e CEP.
        '''
        data = super(CustomerSerializer, self).to_representation(instance)

        data['rg'] = f"{instance.rg[:2]}.{instance.rg[2:5]}.{instance.rg[5:8]}-{instance.rg[8:]}"
        data['cpf'] = f"{instance.cpf[:3]}.{instance.cpf[3:6]}.{instance.cpf[6:9]}-{instance.cpf[9:]}"
        if instance.cep:
            data['cep'] = f"{instance.cep[:5]}-{instance.cep[5:]}"

        return data


class CustomerCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Customer
        fields = ('user', 'rg', 'cpf', 'cep', 'address')


def only_numbers_validator(value):
    if not value.isnumeric():
        raise serializers.ValidationError('Digitar somente números.')


class CustomerUpdateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    cpf = serializers.CharField(validators=[only_numbers_validator])
    cep = serializers.CharField(validators=[only_numbers_validator])

    class Meta:
        model = Customer
        fields = ('user', 'seller', 'rg', 'cpf', 'cep', 'address')

    def update(self, instance, validated_data):
        # Edita user
        if 'user' in validated_data:
            user = validated_data.pop('user')
            # instance.user.username = user.get('username')
            # instance.user.first_name = user.get('first_name')
            # instance.user.last_name = user.get('last_name')
            # instance.user.email = user.get('email')

            for attr, value in user.items():
                setattr(instance.user, attr, value)

            instance.user.save()

        # Edita seller
        if 'seller' in validated_data:
            seller = validated_data.pop('seller')

            for attr, value in seller.items():
                setattr(instance.seller, attr, value)

            instance.seller.save()

        # Edita demais campos
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class ComissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comission
        fields = ('group', 'percentage')
