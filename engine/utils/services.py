from django.db import connection
from django.apps import apps


def check_model_changes(module_name):
    try:
        app_config = apps.get_app_config(module_name)
        models = app_config.get_models()

        with connection.cursor() as cursor:
            for model in models:
                table_name = model._meta.db_table
                # cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
                cursor.execute(f"PRAGMA table_info({table_name})")
                db_fields = {row[1] for row in cursor.fetchall()}

                model_fields = {field.column for field in model._meta.fields}

                print(f"Model: {model.__name__}, DB Fields: {db_fields}, Model Fields: {model_fields}")

                if db_fields != model_fields:
                    return True  # Ada perubahan pada model

        return False  # Tidak ada perubahan

    except Exception as e:
        print(f"Error: {e}")
        return False