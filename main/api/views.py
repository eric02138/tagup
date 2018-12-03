from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from main.record.models import Record
from main.api.serializers import RecordSerializer

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
	"""
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