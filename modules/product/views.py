from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from engine.models import Permission
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from engine.utils.services import check_model_changes


def product_list(request):
    if request.method == "GET":
        if check_model_changes("product"):
            return render(request, 'product/product_upgrade.html', {})

        role = request.session.get("role")
        if role:
            objPermission = get_object_or_404(Permission, role=role)
            userData = {
                "role": role,
                "is_login": True,
                "permission": model_to_dict(objPermission)
            }
        else:
            objPermission = {"is_create": False, "is_edit": False, "is_delete": False}
            userData = {
                "role": "Public",
                "is_login": False,
                "permission": objPermission
            }

        objProduct = Product.objects.all()
        return render(request, 'product/product_list.html', {'objProduct': objProduct, 'userData': userData})

@csrf_exempt
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})

@csrf_exempt
def product_update(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})

@csrf_exempt
def product_delete(request, id):
    product = Product.objects.get(id=id)
    if request.method == 'DELETE':
        product.delete()
        return JsonResponse({"message": "Product deleted successfully."}, status=200)
    return JsonResponse({"meesage": "Invalid request method."}, status=400)