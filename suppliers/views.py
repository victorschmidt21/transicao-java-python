from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import models
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def view_index(request):
    search = request.GET.get("search", "").strip()
    suppliers = models.Supplier.objects.all()

    if search:
        suppliers = suppliers.filter(
            Q(cnpj__icontains=search) |
            Q(name__icontains=search)
        )

    return render(request, 'suppliers.html', {
        'suppliers': suppliers,
        'search': search,
    })

@login_required
def view_create(request):
    if request.method == "POST":
        models.Supplier.objects.create(
            name=request.POST["name"],
            email=request.POST["email"],
            mobile=request.POST["mobile"],
            phone=request.POST["phone"],
            postal_code=request.POST["postal_code"],
            address=request.POST["address"],
            neighborhood=request.POST["neighborhood"],
            city=request.POST["city"],
            state=request.POST["state"],
            complement=request.POST["complement"],
            cnpj=request.POST["cnpj"],
        )
        return redirect("/suppliers/")

    return render(request, "supplier_form.html", {
        "title": "Cadastrar Fornecedor",
        "states": models.Supplier.BRAZILIAN_STATES,
    })

@login_required
def view_delete(request, id):
    supplier = get_object_or_404(models.Supplier, id=id)
    supplier.delete()
    return redirect("/suppliers/")

@login_required
def view_edit(request, id):
    supplier = get_object_or_404(models.Supplier, id=id)

    if request.method == "POST":
        supplier.name = request.POST["name"]
        supplier.email = request.POST["email"]
        supplier.mobile = request.POST["mobile"]
        supplier.phone = request.POST["phone"]
        supplier.postal_code = request.POST["postal_code"]
        supplier.address = request.POST["address"]
        supplier.neighborhood = request.POST["neighborhood"]
        supplier.city = request.POST["city"]
        supplier.state = request.POST["state"]
        supplier.complement = request.POST["complement"]
        supplier.cnpj = request.POST["cnpj"]

        supplier.save()

        return redirect("/suppliers/")

    return render(request, "supplier_form.html", {
        "title": "Editar Fornecedor",
        "states": models.Supplier.BRAZILIAN_STATES,
        "supplier": supplier,
    })
