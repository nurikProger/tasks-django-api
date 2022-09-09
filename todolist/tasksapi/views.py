from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Tasks
from .serializers import TasksSerializer
from datetime import datetime
from pytz import timezone


class TasksAPIView(APIView):


    # List
    def get(self, request):
        tasks = Tasks.objects.all()
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    # Create
    def post(self, request):
        data =  {
            'start_time' : request.data.get('start_time'),
            'end_time' : request.data.get('end_time'),
            'title' : request.data.get('title'),
            'description' : request.data.get('description'),
            'status' : request.data.get('status')
        }
        serializer = TasksSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TasksDetailAPIView(APIView):


    # Check for the Task
    def get_object(self, task_id):
        try:
            return Tasks.objects.get(id=task_id)
        except Tasks.DoesNotExist:
            return None


    # Retrieve
    def get(self, request, task_id):

        task_exists = self.get_object(task_id)

        if not task_exists:
            return Response(
                {"res":"Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TasksSerializer(task_exists)
        return Response(serializer.data, status=status.HTTP_200_OK)

    
    # Update
    def put(self, request, task_id):

        task_exists = self.get_object(task_id)
        print(task_exists)
        if not task_exists:
            return Response(
                {"res":"Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'start_time' : request.data.get('start_time'),
            'end_time' : request.data.get('end_time'),
            'title' : request.data.get('title'),
            'description' : request.data.get('description'),
            'status' : request.data.get('status')
        }

        serializer = TasksSerializer(instance=task_exists, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Partial Update
    def patch(self, request, task_id):

        task_exists = self.get_object(task_id)

        if not task_exists:
            return Response(
                {"res":"Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            'start_time' : request.data.get('start_time', task_exists.start_time),
            'end_time' : request.data.get('end_time', task_exists.end_time),
            'title' : request.data.get('title', task_exists.title),
            'description' : request.data.get('description', task_exists.description),
            'status' : request.data.get('status', task_exists.status)
        }

        serializer = TasksSerializer(instance=task_exists, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    # Delete
    def delete(self, request, task_id):

        task_exists = self.get_object(task_id)

        if not task_exists:
            return Response(
                {"res":"Object with task id does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        task_exists.delete()
        return Response(
            {"res":"Object deleted!"},
            status=status.HTTP_200_OK
        )


class TasksToDoAPIView(APIView):

    # Get To-Do Tasks
    def get(self, request):
        tasks = Tasks.objects.filter(status="todo")
        serializer = TasksSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class TasksExpiredAPIView(APIView):

    # Get Expired Tasks
    def get(self, request):
        current = timezone("Asia/Tashkent").localize(datetime.now())
        tasks = Tasks.objects.all().values()
        expired = []

        for task in tasks:
            end_time = task['end_time']

            if current > end_time:
                expired.append(task)

        return Response(expired, status=status.HTTP_200_OK)

class TasksInProgressAPIView(APIView):

    # Get In-Progress Tasks
    def get(self, request):
        tasks = Tasks.objects.filter(status="in progress")
        serializer = TasksSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class TasksDoneAPIView(APIView):

    # Get Done Tasks
    def get(self, request):
        tasks = Tasks.objects.filter(status="done")
        serializer = TasksSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)