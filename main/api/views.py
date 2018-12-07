import time
from datetime import datetime, timedelta
from decimal import Decimal
from math import modf
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.record.models import Record
from main.api.serializers import RecordSerializer

def get_datetime_from_timestring(timestring):
	"""
	Takes a timestring and returns a microsecond resolution datetime
	:param: timestring
	:return: datetime
	"""
	try:
		time_float = float(timestring)
		print("time_float")
		print(time_float)
		time_decimal = Decimal(time_float)
		time_decimal = round(time_decimal, 6)
		print("time_decimal")
		print(time_decimal)
		b, a = modf(time_decimal)
		ms = round(b, 6)
		print("ms")
		print(ms)
		dt_obj = datetime.fromtimestamp(time_decimal)
		dt_obj = dt_obj + timedelta(microseconds=ms)
		print("dt_obj")
		print(dt_obj)
	except Exception as e:
		print("Error in function: ")
		print(e)
		raise
	return dt_obj

@api_view(['GET'])
def api_routes(request, format=None):
	"""
	list of api endpoints
	:param request:
	:return: Response
	"""
	id = 0
	try:
		record = Record.objects.first()
		if record:
			id = record._id
	except:
		pass

	data = {
		'List': '<a href=/api/list/>/api/list/</a>',
		'Create': '<a href=/api/create/>/api/create/</a>',
		'Read': '<a href=/api/read/{0}>/api/read/{0}</a>'.format(id),
		'Modify': '<a href=/api/modify/{0}>/api/modify/{0}</a>'.format(id),
		'Remove': '<a href=/api/remove/{0}>/api/remove/{0}</a>'.format(id)
	}
	return Response(data)


@api_view(['GET'])
def record_list(request, format=None):
	"""
	list of all records
	:param request:
	:return: Response
	"""
	records = Record.objects.order_by('-lastModificationDate').all()
	serializer = RecordSerializer(records, many=True)
	return Response(serializer.data)

@api_view(['POST'])
def record_create(request, format=None):
	"""
	create a new record
	:param request: data payload
	:param format:  json, html
	:return: Response
	:note: If the timestamp is an int or float, try to convert to timestamp, using mktime
	"""
	ts = request.data.get("timestamp")
	print("ts")
	print(ts)
	
	if type(ts).__name__ == 'string':
		try:
			"""
			first, see if the string input is in datetime format.  
			If it is, then we don't have to do any conversion.
			"""
			if ":" == ts[-3:-2]:
				ts = ts[:-3]+ts[-2:]   #annoying hack to make timezones format correctly
			dt_obj = datetime.strptime(ts, "%Y-%m-%dT%H:%M:%S.%f%z")
			print("dt_obj")
			print(dt_obj)
		except Exception as e:
			return Response("Sorry, but {0} cannot be formatted into a datetime: {1}".format(ts, e), 
					status=status.HTTP_400_BAD_REQUEST)

	if type(ts).__name__ == 'float':
		"""
		Ok, now it's not a well-formatted date, so let's see if it's a decimal number that
		can be formatted into a date.
		"""
		try:
			request.data.timestamp = get_datetime_from_timestring(ts)
		except Exception as e:
			return Response("Sorry, couldn't convert {0} into datetime: {1}".format(ts, e), 
					status=status.HTTP_400_BAD_REQUEST)

	if type(ts).__name__ == 'int':
		"""
		And hey, if timestamp is an int, and it's bigger than 9999999999 
		and less than 1000000000000, then we must be dealing with the number of milliseconds 
		"""
		try:
			time_float = int(ts)
			if 9999999999 < time_int < 1000000000000:
				time_decimal = Decimal(time_int / 1000)
				time_string = str(time_decimal)
				request.data.timestamp = get_datetime_from_timestring(time_string)
		except Exception as e:
			return Response("Sorry, couldn't convert {0} into datetime: {1}".format(ts, e), 
					status=status.HTTP_400_BAD_REQUEST)

			
	serializer = RecordSerializer(data=request.data)	
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def record_detail(request, pk, format=None):
	"""
	create a new record
	:param request:
	:param pk: primary key
	:param format: json, html
	:return: Response
	"""
	try:
		record = Record.objects.get(pk=pk)
	except Record.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = RecordSerializer(record)
	return Response(serializer.data)

@api_view(['PUT'])
def record_modify(request, pk, format=None):
	"""
	modify a record
	:param request: data payload
	:param pk: primary key
	:param format: json, html
	:return: Response
	"""
	try:
		record = Record.objects.get(pk=pk)
	except Record.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	serializer = RecordSerializer(record, data=request.data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def record_delete(request, pk, format=None):
	"""
	delete a record
	:param request:
	:param pk: primary key
	:param format: json, html
	:return: Response
	"""
	try:
		record = Record.objects.get(pk=pk)
	except Record.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	record.delete()
	return Response(status=status.HTTP_204_NO_CONTENT)
