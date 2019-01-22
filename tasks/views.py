from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Tasks
from .serializers import TasksSerializer


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_task(request, pk):
    try:
        task = Tasks.objects.get(pk=pk)
    except Tasks.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single task
    if request.method == 'GET':
        serializer = TasksSerializer(task)
        return Response(serializer.data)
    # delete a single task
    elif request.method == 'DELETE':
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single task
    elif request.method == 'PUT':
        serializer = TasksSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_tasks(request):
    # get all tasks
    if request.method == 'GET':
        tasks = Tasks.objects.all()
        serializer = TasksSerializer(tasks, many=True)
        return Response(serializer.data)
    # insert a new record for a task

    if request.method == 'POST':
        data = {
            'title': request.data.get('title'),
            'is_done': request.data.get('is_done'),
            'description': request.data.get('description'),
            'date': request.data.get('date')
        }

        serializer = TasksSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


