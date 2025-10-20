from django.shortcuts import render

# Create your views here.

def view_index(request):
    return render(request, 'index.html')

def view_create(request):
    return render(request, 'create.html')

def view_edit(request):
    return 'Edit'

def view_delete(request):
    return 'Delete'