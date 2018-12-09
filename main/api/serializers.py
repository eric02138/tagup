from datetime import datetime
from rest_framework import serializers
from main.record.models import Record

class RecordSerializer(serializers.Serializer):
	_id = serializers.IntegerField(read_only=True)
	timestamp = serializers.DateTimeField(required=True)
	value1 = serializers.IntegerField(required=True)
	value2 = serializers.IntegerField(required=True)
	value3 = serializers.IntegerField(required=True)
	#createdDate = serializers.DateTimeField(read_only=True)
	#lastModificationDate = serializers.DateTimeField(read_only=True)

	def create(self, validated_data):
		return Record.objects.create(**validated_data)

	def update(self, instance, validated_data):
		instance.timestamp = validated_data.get('timestamp', instance.timestamp)
		instance.value1 = validated_data.get('value1', instance.value1)
		instance.value2 = validated_data.get('value2', instance.value2)
		instance.value3 = validated_data.get('value3', instance.value3)
		instance.save()
		return instance
	
	def to_representation(self, instance):
		display = self.context.get("display")
		#if request.data and request.data.get("format") == "datestring":
		if display == "datestring":
			print("show as formatted date")
			return {
				'_id': instance._id,
				'timestamp': instance.timestamp,
				'value1': instance.value1,
				'value2': instance.value2,
				'value3': instance.value3
				}
		else:
			timestamp = instance.timestamp.timestamp()
			milliseconds = round(timestamp * 1000)
			return {
				'_id': instance._id,
				'timestamp': milliseconds,
				'value1': instance.value1,
				'value2': instance.value2,
				'value3': instance.value3
				}
