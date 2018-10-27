from datetime import timedelta
from rest_framework import serializers

from .validators import in_future


class SlotsSerializer(serializers.Serializer):
    start = serializers.DateTimeField(validators=(in_future,))
    end = serializers.DateTimeField(validators=(in_future,))

    def validate(self, data):
        if data['start'] > data['end']:
            raise serializers.ValidationError('end should be later than start')
        if data['start'].minute:
            data['start'] = data['start'].replace(minute=0) + timedelta(hours=1)
        if data['start'] + timedelta(hours=1) > data['end']:
            raise serializers.ValidationError('slot is too short')
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        start = validated_data['start']
        while start + timedelta(hours=1) <= validated_data['end']:
            user.slots.create(start=start)
            start += timedelta(hours=1)
        return validated_data
