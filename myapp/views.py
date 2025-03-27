from django.shortcuts import render, redirect , get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product2D ,Product3D , Model3D ,Model2D , Order , Feedback
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db.models import Avg
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from .models import Product2D, Product3D, LikedProduct

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials")
    return render(request, 'login.html')


def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully")
            return redirect('login')
    return render(request, 'register.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'home.html')

def models_2d(request):
    if not request.user.is_authenticated:
        return redirect('login')
    models_2d_carvings=Model2D.objects.all()
    return render(request, 'model_2d.html',{'models_2d':models_2d_carvings})

def models_3d(request):
    if not request.user.is_authenticated:
        return redirect('login')
    models_3d_carvings=Model3D.objects.all()
    return render(request, 'model_3d.html',{'models_3d':models_3d_carvings})

def products_2d(request, pk):
    products_2d_carvings = Product2D.objects.filter(model_2d=pk)

    liked_products = LikedProduct.objects.filter(
        user=request.user,
        content_type=ContentType.objects.get_for_model(Product2D)
    ).values_list('object_id', flat=True)  # Fetch liked Product2D IDs

    return render(request, 'products_2d.html', {
        'products_2d_carvings': products_2d_carvings,
        'liked_products': list(liked_products)  # Convert queryset to list
    })

# def products_3d(request, pk):
#     products_3d_carvings = Product3D.objects.filter(model_3d=pk)
#     liked_products = LikedProduct.objects.filter(user=request.user, content_type=ContentType.objects.get_for_model(Product3D)).values_list('object_id', flat=True) if request.user.is_authenticated else []
#     return render(request, 'products_3d.html', {'products_3d_carvings': products_3d_carvings, 'liked_products': liked_products})
def products_3d(request, pk):
    # Fetch 3D products related to the given model_3d ID
    products_3d_carvings = Product3D.objects.filter(model_3d=pk)

    # Get liked products only if the user is authenticated
    liked_products = []
    if request.user.is_authenticated:
        liked_products = LikedProduct.objects.filter(
            user=request.user,
            content_type=ContentType.objects.get_for_model(Product3D)
        ).values_list('object_id', flat=True)

    return render(request, 'products_3d.html', {
        'products_3d_carvings': products_3d_carvings,
        'liked_products': list(liked_products)  # Convert queryset to a list
    })

def like_product(request, product_type, product_id):
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'error', 'message': 'You need to log in to like products'})

    # Determine product model based on type
    model_class = Product2D if product_type == '2d' else Product3D
    content_type = ContentType.objects.get_for_model(model_class)
    product = get_object_or_404(model_class, id=product_id)

    # Check if the product is already liked
    liked_product, created = LikedProduct.objects.get_or_create(
        user=request.user, content_type=content_type, object_id=product.id
    )

    if not created:
        liked_product.delete()
        return JsonResponse({'status': 'removed', 'liked': False})

    return JsonResponse({'status': 'added', 'liked': True})

def liked_products(request):
    if not request.user.is_authenticated:
        return redirect('login')

    liked_products = LikedProduct.objects.filter(user=request.user)
    return render(request, 'cart.html', {'liked_products': liked_products})

def single_product_2d(request,pk):
    single_2d_product=Product2D.objects.get(id=pk)
    return render(request,'product_2d_single.html',{'single_2d_product':single_2d_product})

def single_product_3d(request,pk):
    single_3d_product=Product3D.objects.get(id=pk)
    return render(request,'product_3d_single.html',{'single_3d_product':single_3d_product})

def logout_user(request):
    logout(request)
    return redirect('login')

def order_product(request, product_type, pk):
    # Determine which model to query based on `product_type`
    if product_type == "3d":
        product = get_object_or_404(Product3D, id=pk)
    elif product_type == "2d":
        product = get_object_or_404(Product2D, id=pk)
    else:
        return render(request, 'error.html', {'message': 'Invalid product type'})

    if request.method == 'POST':
        # Get form data
        email = request.POST.get('email')
        mobile_number1 = request.POST.get('mobile_number1')
        mobile_number2 = request.POST.get('mobile_number2', '')  # Optional field
        address = request.POST.get('address')
        quantity = request.POST.get('quantity')

        # Validate required fields
        if not (email and mobile_number1 and address):
            return render(request, 'order_product.html', {
                'product': product,
                'error': 'All required fields must be filled!',
            })
        
        quantity = int(quantity) if quantity else None  # Ensure it's an integer if provided

        # Save the order
        order = Order.objects.create(
            user=request.user,
            product=product,
            email=email,
            mobile_number1=mobile_number1,
            mobile_number2=mobile_number2,
            address=address,
            quantity=quantity,
        )

        # Send email
        try:
            send_mail(
                subject="Order Confirmation",
                message=f"Dear {request.user.username},\n\n"
                        f"Thank you for placing an order with us! Here are your order details:\n\n"
                        f"Product Name: {product.name}\n"
                        f"Quantity: {quantity}\n"
                        f"Delivery Address: {address}\n\n"
                        f"We will process your order shortly and keep you updated on the status.\n\n"
                        f"If you have any questions or need further assistance, please feel free to contact us (9444133162).\n\n"
                        f"Best regards,\n"
                        f"Kamatchicarvings",
                from_email="Kamatchicarvings@gmail.com",  # Replace with your email
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

        return redirect('order_success')

    return render(request, 'order_product.html', {'product': product})

def order_success(request):
    return render(request, 'order_success.html')

    
# def feedback_list(request):
#     sort_option = request.GET.get('sort', '-created_at')  # Default sorting by most recent
#     feedbacks = Feedback.objects.filter(is_approved=True).order_by(sort_option)
#     return render(request, 'feedback.html', {'feedbacks': feedbacks})

# @login_required
# def submit_feedback(request):
#     if request.method == "POST":
#         rating = request.POST.get('rating')
#         message = request.POST.get('message')
#         image = request.FILES.get('image')

#         Feedback.objects.create(user=request.user, rating=rating, message=message, image=image, is_approved=True)
#         messages.success(request, "Thanks for your feedback!")
#         return redirect('feedback_list')

#     return render(request, 'feedback_form.html')
def feedback_list(request):
    sort_by = request.GET.get('sort', '-created_at') 
    feedbacks = Feedback.objects.filter(is_approved=True).order_by(sort_by)
    return render(request, "feedback.html", {"feedbacks": feedbacks , 'sort_by': sort_by })

def submit_feedback(request):
    if request.method == "POST":
        message = request.POST.get("message")
        rating = request.POST.get("rating")
        image = request.FILES.get("image")  # Handle image file
        user = request.user if request.user.is_authenticated else None

        Feedback.objects.create(user=user, message=message, rating=rating, image=image, is_approved=True)

        return JsonResponse({"status": "success", "message": "Thank you for your feedback!"})

    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)
def about(request):
    return render(request,'about.html')