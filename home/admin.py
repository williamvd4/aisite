# Import the necessary modules
from django.contrib import admin
from myapp.models import MyModel  # Replace this with the actual name of your model

# Register the model with the admin site
# The list_display argument allows you to specify which fields to display in the admin change list page
# The list_filter argument allows you to specify which fields to use for filtering the model instances in the admin change list page
# The search_fields argument allows you to specify which fields to use for searching the model instances in the admin change list page
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('field1', 'field2')  # Replace field1 and field2 with the actual names of the fields you want to display
    list_filter = ('field3',)  # Replace field3 with the actual name of the field you want to use for filtering
    search_fields = ('field4',)  # Replace field4 with the actual name of the field you want to use for searching

