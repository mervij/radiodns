# Copyright 2021 Radio Moreeni
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rest_framework import serializers

from .models import Service, Bearer


def match_bearer(bearer_data):
    # Match existing bearer based on primary key or details
    try:
        bearer = Bearer.objects.get(pk=bearer_data['id'])
    except (Bearer.DoesNotExist, KeyError):
        try:
            bearer = Bearer.objects.get(platform=bearer_data['platform'], ecc=bearer_data['ecc'],
                                        pi=bearer_data['pi'])
        except (Bearer.DoesNotExist, KeyError):
            try:
                bearer = Bearer.objects.get(platform=bearer_data['platform'], url=bearer_data['url'])
            except (Bearer.DoesNotExist, KeyError):
                bearer = None
    return bearer


class BearerSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    service = serializers.HyperlinkedRelatedField(required=False, view_name='service-detail',
                                                  queryset=Service.objects.all())

    class Meta:
        model = Bearer
        fields = '__all__'

    def create(self, validated_data):
        """Normalizes bearer data before creating object."""
        if validated_data.get('ecc'):
            validated_data['ecc'] = validated_data['ecc'].lower()
        if validated_data.get('pi'):
            validated_data['pi'] = validated_data['pi'].lower()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """Normalizes bearer data before updating object."""
        if validated_data.get('ecc'):
            validated_data['ecc'] = validated_data['ecc'].lower()
        if validated_data.get('pi'):
            validated_data['pi'] = validated_data['pi'].lower()
        return super().update(instance, validated_data)

    def validate(self, attrs):
        """Validates bearers based on their platform."""
        if attrs.get('platform'):
            if attrs['platform'] == 'fm':
                if (not attrs.get('ecc')) or attrs['ecc'] == '':
                    raise serializers.ValidationError({'ecc': 'ECC is required for FM bearers'})
                if (not attrs.get('pi')) or attrs['pi'] == '':
                    raise serializers.ValidationError({'pi': 'PI is required for FM bearers'})
                if (not attrs.get('frequency')) or attrs['frequency'] == '':
                    raise serializers.ValidationError({'frequency': 'Frequency is required for FM bearers'})
            elif attrs['platform'] == 'ip':
                if (not attrs.get('url')) or attrs['url'] == '':
                    raise serializers.ValidationError({'url': 'URL is required for IP bearers'})
                if (not attrs.get('mimeValue')) or attrs['mimeValue'] == '':
                    raise serializers.ValidationError({'mimeValue': 'mimeValue is required for IP bearers'})
        return attrs


class ServiceSerializer(serializers.HyperlinkedModelSerializer):
    bearers = BearerSerializer(many=True, required=False, allow_null=True)

    def create(self, validated_data):
        """Creates service objects handling nested bearers."""
        bearers_data = []
        try:
            bearers_data = validated_data.pop('bearers')
        except KeyError:
            pass
        service = Service.objects.create(**validated_data)
        for bearer in bearers_data:
            Bearer.objects.create(service=service, **bearer)
        return service

    def update(self, instance, validated_data):
        """Updates service objects handling nested bearers.

        Based on the method of the request, deletes old bearers what weren't included in the request.
        """
        bearers_data = []
        if validated_data.get('bearers'):
            bearers_data = validated_data.pop('bearers')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        # If this wasn't a PATCH request, we plan to remove hanging bearers at the end
        if self.context['request'].method != 'PATCH':
            removable = Bearer.objects.filter(service=instance)

        # Update or create bearers from nested data
        for bearer_data in bearers_data:
            # Try to find an existing bearer
            bearer = match_bearer(bearer_data)

            # If a bearer exists, update fields for that bearer, otherwise create a new one
            if bearer:
                for key, value in bearer_data.items():
                    setattr(bearer, key, value)
                bearer.save()
            else:
                if 'service' in bearer_data:
                    bearer = Bearer.objects.create(**bearer_data)
                else:
                    bearer = Bearer.objects.create(service=instance, **bearer_data)

            # Exclude matched or created bearer from removal
            if self.context['request'].method != 'PATCH':
                removable = removable.exclude(pk=bearer.pk)

        # Assume PUT requests to contain full bearer list and remove any old ones that didn't match
        if self.context['request'].method != 'PATCH':
            removable.delete()
        return instance

    class Meta:
        model = Service
        fields = '__all__'
