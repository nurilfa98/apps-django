from django.shortcuts import render, get_object_or_404, redirect
from .models import Module, Permission
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseNotFound, HttpResponse
from django.forms.models import model_to_dict
from engine.utils.services import check_model_changes
from django.contrib import messages
import json, importlib, subprocess, semver, sys


def module_list(request):
    objModule = Module.objects.all()
    return render(request, 'engine/module_list.html', {'objModule': objModule})

def module_router(request, slug):
    try:
        # Cek apakah modul sudah diinstall
        module = Module.objects.get(slug=slug)
        if not module.is_installed:
            return render(request, "engine/module_not_installed.html", {"slug": slug}, status=404)

        # Import module views berdasarkan slug
        moduleViews = importlib.import_module(f"modules.{slug}.views")

        # Panggil fungsi 'list' atau default ke halaman not found jika tidak ada
        if hasattr(moduleViews, f"{slug}_list"):
            view_func = getattr(moduleViews, f"{slug}_list")
            return view_func(request)  # Panggil fungsi view
        else:
            return HttpResponseNotFound("Page not found in module")

    except ModuleNotFoundError:
        return HttpResponseNotFound("Module not found")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

@csrf_exempt
def install_module(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            slug = data.get('slug')

            module = Module.objects.get(slug=slug)
            module.is_installed = True
            module.save()

            moduleDict = model_to_dict(module)
            response = {"message": "Success", "data": moduleDict}

            return JsonResponse(response, status=200)
        except Module.DoesNotExist:
            print("Module not found")
            return JsonResponse({"error": "Module not found"}, status=404)
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def uninstall_module(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            slug = data.get('slug')

            module = Module.objects.get(slug=slug)
            module.is_installed = False
            module.save()

            moduleDict = model_to_dict(module)
            response = {"message": "Success", "data": moduleDict}

            return JsonResponse(response, status=200)
        except Module.DoesNotExist:
            print("Module not found")
            return JsonResponse({"error": "Module not found"}, status=404)
        except Exception as e:
            print("Unexpected error:", str(e))
            return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def upgrade_module(request, slug):
    module = get_object_or_404(Module, slug=slug)

    if not module.is_installed:
        return render(request, "engine/module_not_installed.html", {"slug": slug}, status=404)

    try:
        print(f"--->> Running migrations for module: {slug}")
        if not check_model_changes(slug):
            messages.info(request, "The module is already up to date.")
            return redirect("module_list")

        # Jalankan makemigrations
        python_exec = sys.executable  # Path ke Python yang sedang digunakan
        subprocess.run([python_exec, "manage.py", "makemigrations", slug], check=True)

        # Jalankan migrate
        subprocess.run([python_exec, "manage.py", "migrate", slug], check=True)

        if module.version:
            new_version = semver.VersionInfo.parse(module.version).bump_patch()
        else:
            new_version = "1.0.0"

        # Update versi module
        module.version = str(new_version)
        module.save()

        return redirect("module_list")

    except subprocess.CalledProcessError as e:
        return HttpResponse(f"Failed to upgrade module! Error: {e.stderr}", status=500)

@csrf_exempt
def user_login(request):
    if request.method == "POST":
        print("--->> login sebagai:: ", request.POST.get("role"))
        role = request.POST.get("role")
        request.session["role"] = role
        request.session.set_expiry(300)  # Expired dalam 5 menit
        return redirect("product_list")
    return render(request, 'engine/form_login.html', {})

def user_logout(request):
    del request.session["role"]
    return redirect("product_list")