from django.shortcuts import render

# Create your views here.

def view_index(request):
    return render(request, 'index.html')

def view_create(request):
    return render(request, 'budget/create.html')

def view_edit(request, id):
    return render(request, 'budget/edit.html', {'id': id})

def view_delete(request, id):
    return render(request, 'budget/delete.html', {'id': id})