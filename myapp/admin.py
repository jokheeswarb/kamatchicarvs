from django.contrib import admin
from .models import Model3D,Model2D,Product2D, Product3D , Order , Feedback

admin.site.register(Model2D)
admin.site.register(Model3D)
admin.site.register(Product2D)
admin.site.register(Product3D)
class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('id', 'user', 'product', 'email', 'mobile_number1', 'mobile_number2', 'address', 'quantity', 'order_date', 'status')

    # Add filters to the right sidebar (make sure fields are defined in the model)
    list_filter = ('status', 'order_date')

    # Add search functionality
    search_fields = ('user__username', 'product__name', 'email')

    # Add ordering by specific field (sort by order_date)
    ordering = ('-order_date',)

    # Optionally, add fields you want to display as links or editable inline
    list_display_links = ('id', 'product')

    # Add date hierarchy for better navigation (ensure order_date is a DateTimeField)
    date_hierarchy = 'order_date'

    # Optionally add pagination
    list_per_page = 20

# Register the Order model with the customized OrderAdmin
admin.site.register(Order, OrderAdmin)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'rating', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'rating']
    search_fields = ['user__username', 'comment']
    actions = ['approve_feedback', 'delete_feedback']

    def approve_feedback(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected feedback approved.")

    def delete_feedback(self, request, queryset):
        queryset.delete()
        self.message_user(request, "Selected feedback deleted.")