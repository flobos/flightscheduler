from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from flights.models import Schedule
from flights.serializers import ScheduleSerializer, UserSerializers
from rest_framework import viewsets, status
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return HttpResponse("<h1>Hola</h1>")


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers

#APIS

@csrf_exempt
def flight_list(request):
    if request.method == 'GET':
        schedules = Schedule.objects.all()
        schedules_serializer = ScheduleSerializer(schedules,many=True)
        return JsonResponse(schedules_serializer.data, safe=False)

    if request.method == 'POST':
        schedule_data = JSONParser().parse(request)
        schedule_serializer = ScheduleSerializer(data=schedule_data)
        if schedule_serializer.is_valid():
            schedule_serializer.save()
            return JsonResponse(schedule_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(schedule_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        Schedule.objects.all().delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)

@csrf_exempt
def flight_detail(request, pk):
    try:
        schedule = Schedule.objects.get(pk=pk)
    except Schedule.DoesNotExist:
         return JsonResponse(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        schedule_serializer = ScheduleSerializer(schedule)
        return JsonResponse(schedule_serializer.data)

    if request.method == 'PUT':
        schedule_data = JSONParser().parse(request)
        schedule_serializer = ScheduleSerializer(schedule, data=schedule_data)
        if schedule_serializer.is_valid():
            schedule_serializer.save()
            return JsonResponse(schedule_serializer.data)
        return JsonResponse(schedule_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        schedule.delete()
        return JsonResponse(status=status.HTTP_204_NO_CONTENT)












