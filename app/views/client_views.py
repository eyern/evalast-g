from django.shortcuts import render, redirect, get_object_or_404
from app.models import Book, Category, Cart, CartItem, CustomerProfile, Coupon, Order, OrderItem, Review, Wishlist
from django.db.models import Q, Count, Avg, Max
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

def register_view(request):

    if request.user.is_authenticated:
        messages.warning(request, 'You are already login')
        return redirect('index')
    
    if request.method == 'POST':
        
        email = request.POST.get('email', '').strip()
        name = request.POST.get('name', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not email or not name or not password or not confirm_password:

            messages.error(request, 'Please fill in all required fields')

            return redirect('register')
        
        elif User.objects.filter(email=email).exists():

            messages.error(request, 'Email is already exists.')

            return redirect('register')
    
        elif password != confirm_password:

            messages.error(request, 'Password do not match.')

            return redirect('register')

        else:
            user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
        )

        CustomerProfile.objects.create(
            user=user,
            full_name = name
        )

        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'website/auth/login.html')

def login_view(request):

    if request.method == "POST":

        email = request.POST.get("email", '').strip()
        password = request.POST.get("password", '')

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password.')
            return  redirect('login')

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user :

            login(request, user)

            # Admin / Staff User
            if user.is_staff:

                messages.success(request, "Welcome to Admin Dashboard!")

                return redirect("dashboard")

            # Normal User
            else:

                messages.success(request, f"Welcome back { user.username } !")

                return redirect("index")

        else:

            messages.error(request, "Invalid username or password.")

            return redirect("login")

    return render(
        request,
        "website/auth/login.html"
    )

def client_logout_view(request):

    logout(request)

    messages.success(request, 'You have been logout successfully.')

    return redirect('login')

@login_required
def profile(request):

    if request.user.is_staff:
        messages.warning(
            request,
            'Admin account cannot access customer profile'
        )
        return redirect("dashboard")
    
    profile, created = CustomerProfile.objects.get_or_create(
        user=request.user
    )

    return render(
        request,
        "website/profile.html",
        {
            "profile": profile,
        }
    )

@login_required
def edit_profile(request):

    if request.user.is_staff:
        messages.warning(
            request,
            'Admin account cannot access customer profile'
        )
        return redirect("dashboard")

    profile, created = CustomerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        address = request.POST.get("address", "").strip()
        city = request.POST.get("city", "").strip()
        country = request.POST.get("country", "").strip()

        # Customer Profile
        profile.full_name = name
        profile.phone = phone
        profile.address = address
        profile.city = city
        profile.country = country

        # Profile Image
        if request.FILES.get("profile_image"):
            profile.profile_image = request.FILES["profile_image"]

        profile.save()

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("profile")

    return render(
        request,
        "website/edit_profile.html",
        {
            "profile": profile,
        }
    )

def delete_profile(request):
    if request.user.is_staff:
        messages.warning(request, 'Admin account cannot be deleted here.')
        return redirect('dashboard')

    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('index')
    return render(request, 'website/delete_profile.html')

@login_required
def index(request):

    categories_list = Category.objects.all()

    featured_books = Book.objects.filter(
        show_on_home=True,
        home_section='featured',
        status='active'
    ).annotate(
        average_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )[:6]

    best_sellers = Book.objects.filter(
        show_on_home=True,
        home_section='best_seller',
        status='active'
    ).annotate(
        average_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    )[:6]

    new_arrivals = Book.objects.filter(
        show_on_home=True,
        home_section='new_arrival',
        status='active'
    ).annotate(
        average_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-created_at')[:6]

    wishlist_book_ids = Wishlist.objects.filter(
        user=request.user
    ).values_list('book_id', flat=True)

    if search:

        books = Book.objects.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search)
        )

    else:

        books = Book.objects.none()

    context = {
        'categories': categories_list,
        'featured_books': featured_books,
        'best_sellers': best_sellers,
        'new_arrivals': new_arrivals,
        'wishlist_book_ids': wishlist_book_ids,
        'books': books,
        'search': search,
    }

    return render(request, 'website/index.html', context)

def category_books(request, pk):

    category = Category.objects.get(id=pk)

    books =Book.objects.filter(category=category)

    wishlist_book_ids = Wishlist.objects.filter(
            user=request.user
        ).values_list('book_id', flat=True)

    context = {
        'selected_category': category,
        'books': books,
        'wishlist_book_ids': wishlist_book_ids,
        'categories': Category.objects.all()
    }

    return render(request, 'website/category_books.html', context)

def search(request):

    query = request.GET.get("q", "")

    books = Book.objects.all()

    wishlist_book_ids = Wishlist.objects.filter(
                user=request.user
            ).values_list('book_id', flat=True)

    if query:
        books = books.filter(
            Q(title__icontains=query) |
            Q(author__icontains=query)
        )

    context = {
        "books": books,
        "query": query,
        'wishlist_book_ids': wishlist_book_ids,
    }

    return render(
        request,
        "website/search.html",
        context
    )

@login_required
def shop(request):

    # Books + Average Rating
    books = Book.objects.annotate(
        average_rating=Avg('reviews__rating')
    )

    # Search
    search_query = request.GET.get('q', '').strip()

    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    # Category
    categories = Category.objects.filter(status=True)

    category_id = request.GET.get('category')

    if category_id:
        books = books.filter(category_id=category_id)

    # Price Range
    price_max = 70000

    max_price = request.GET.get('max_price')

    if max_price:
        books = books.filter(price__lte=max_price)

    # Availability
    availability = request.GET.get('availability')

    if availability == 'in_stock':
        books = books.filter(stock__gt=0)

    elif availability == 'pre_order':
        books = books.filter(is_pre_order=True)

    # Rating
    rating = request.GET.get('rating')

    if rating:
        books = books.filter(
            average_rating__gte=rating
        )

    # Wishlist
    wishlist_book_ids = Wishlist.objects.filter(
        user=request.user
    ).values_list('book_id', flat=True)

    # Sorting
    sort = request.GET.get('sort')

    if sort == 'price_low':
        books = books.order_by('price')

    elif sort == 'price_high':
        books = books.order_by('-price')

    elif sort == 'newest':
        books = books.order_by('-created_at')

    elif sort == 'oldest':
        books = books.order_by('created_at')

    else:
        books = books.order_by('-created_at')

    # Pagination
    paginator = Paginator(books, 12)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,
        'page_obj': page_obj,

        'categories': categories,

        'search_query': search_query,
        'selected_category': category_id,
        'selected_sort': sort,

        'max_price': max_price,
        'price_max': price_max,

        'availability': availability,

        'rating': rating,

        'wishlist_book_ids': wishlist_book_ids,
    }

    return render(
        request,
        'website/shop.html',
        context
    )

@login_required
def category(request):
    categories_list = Category.objects.all()
    context = {'categories': categories_list}
    return render(request, 'website/category.html', context)

@login_required
def book_by_category(request, category_id):
    category = Category.objects.filter(
        category_id=category_id,
        status='active'
    )

    wishlist_book_ids = Wishlist.objects.filter(
        user=request.user
        ).values_list('book_id', flat=True)
    
    context = {
        'category':category,
        'wishlist_book_ids': wishlist_book_ids,
    }

    return render(request, 'website/shop.html', context)

@login_required
def featured_books(request):

    books = Book.objects.filter(
        show_on_home=True,
        home_section='featured',
        status='active'
    ).annotate(
        average_rating=Avg('reviews__rating'),
        review_count=Count('reviews')
    ).order_by('-created_at')

    wishlist_book_ids = Wishlist.objects.filter(
        user=request.user
    ).values_list('book_id', flat=True)

    context = {
        'books': books,
        'wishlist_book_ids': wishlist_book_ids,
    }

    return render(
        request,
        'website/featured_books.html',
        context
    )
@login_required
def best_sellers(request):

    books = Book.objects.filter(
        home_section='best_seller',
        status='active'
    ).order_by('-created_at')

    wishlist_book_ids = Wishlist.objects.filter(
        user=request.user
        ).values_list('book_id', flat=True)

    context = {
        'books': books,
        'wishlist_book_ids': wishlist_book_ids,
    }

    return render(
        request,
        'website/best_sellers.html',
        context
    )

@login_required
def new_arrival(request):

    books = Book.objects.filter(
        home_section='new_arrival',
        status='active'
    ).order_by('-created_at')

    wishlist_book_ids = Wishlist.objects.filter(
        user=request.user
        ).values_list('book_id', flat=True)

    context = {
        'books': books,
        'wishlist_book_ids': wishlist_book_ids,
    }

    return render(
        request,
        'website/new_arrival.html',
        context
    )

@login_required

def book_detail(request, pk):

    book = Book.objects.get(id=pk)

    reviews = Review.objects.filter(book=book).order_by('-created_at')

    average_rating = reviews.aggregate(average=Avg('rating'))['average'] or 0

    related_books = Book.objects.filter(category=book.category).exclude(id=book.id)[:4]

    wishlist_book_ids = Wishlist.objects.filter(user=request.user).values_list('book_id', flat=True)

    context = {
        'book': book,
        'reviews': reviews,
        'average_rating': average_rating,
        'related_books': related_books,
        'wishlist_book_ids': wishlist_book_ids,
    }

    return render(
        request,
        'website/book_detail.html',
        context
    )



@login_required
def add_to_cart(request, book_id):

    book = Book.objects.get(id=book_id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={
            "quantity": 1
        }
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect("cart")


@login_required
def cart_view(request):

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.select_related("book")

    subtotal = 0

    for item in cart_items:
        item.total_price = item.book.price * item.quantity
        subtotal += item.total_price

    total = subtotal

    return render(
        request,
        "website/cart.html",
        {
            "cart": cart,
            "cart_items": cart_items,
            "subtotal": subtotal,
            "total": total,
        }
    )

@login_required
def increase_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.quantity += 1
    cart_item.save()

    return redirect('cart')

@login_required
def decrease_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')

@login_required
def remove_item(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    cart_item.delete()
    return redirect('cart')



@login_required
def checkout(request):

    if request.user.is_staff:
        messages.warning(
            request,
            'You cannot checkout permission with admin account '\
            'Please login again with customer account.'
            )
        return redirect("index")

    cart = get_object_or_404(
        Cart,
        user=request.user
    )

    cart_items = cart.items.select_related("book")

    subtotal = sum(
        item.book.price * item.quantity
        for item in cart_items
    )

    discount_amount = 0
    coupon = None
    coupon_code = ""

    
    # POST

    if request.method == "POST":

        coupon_code = request.POST.get(
            "coupon_code",
            ""
        ).strip()

        # Apply Coupon

        if request.POST.get("apply_coupon"):

            if coupon_code:

                try:
                    coupon = Coupon.objects.get(
                        code__iexact=coupon_code,
                        active=True
                    )

                    discount_amount = (
                        subtotal * coupon.discount_percent
                    ) // 100

                except Coupon.DoesNotExist:

                    coupon = None
                    discount_amount

        # Place Order

        elif request.POST.get("place_order"):

            # Get delivery information

            full_name = request.POST.get(
                "full_name"
            )

            phone = request.POST.get(
                "phone"
            )

            address = request.POST.get(
                "address"
            )

            city = request.POST.get(
                "city"
            )

            country = request.POST.get(
                "country"
            )

            payment_method = request.POST.get(
                "payment_method"
            )

            # Re-check coupon
            # because Place Order is a new POST request

            if coupon_code:

                try:

                    coupon = Coupon.objects.get(
                        code__iexact=coupon_code,
                        active=True
                    )

                    discount_amount = (
                        subtotal * coupon.discount_percent
                    ) // 100

                except Coupon.DoesNotExist:

                    coupon = None
                    discount_amount = 0

            # Final total

            total = subtotal - discount_amount

            # Create Order

            order = Order.objects.create(
                customer=request.user,

                full_name=full_name,
                phone=phone,
                address=address,
                city=city,
                country=country,

                payment_method=payment_method,

                coupon=coupon,
                discount_amount=discount_amount,

                total_amount=total,
            )

            # Create Order Items

            for item in cart_items:

                OrderItem.objects.create(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    price=item.book.price,
                )

            # Clear Cart

            cart.items.all().delete()

            # Temporary success response

            return render(
                request,
                "website/order_success.html",
                {
                    "order": order
                }
            )

    # Total

    total = subtotal - discount_amount

    context = {
        "cart_items": cart_items,
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "total": total,
        "coupon": coupon,
        "coupon_code": coupon_code,
    }

    return render(
        request,
        "website/checkout.html",
        context
    )

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        customer=request.user
    ).order_by('-created_at')

    context = {
        'orders': orders,
    }

    return render(
        request,
        'website/my_orders.html',
        context
    )

@login_required
def my_order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    context = {
        'order': order,
    }

    return render(
        request,
        'website/my_order_detail.html',
        context
    )

@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        customer=request.user
    )

    if request.method == "POST":

        if order.status == "pending":
            order.status = "cancelled"
            order.save()

    return redirect(
        'my_order_detail',
        order_id=order.id
    )


@login_required
def submit_review(request, pk):

    if request.user.is_staff:
                messages.warning(
                    request,
                    'Admin cannot write a comment and star rating in this page  '\
                    'because the developer is mean for customers only.'
                )
                return redirect("index")

    book = get_object_or_404(Book, id=pk)

    if request.method == 'POST':

        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        if not rating or not comment:

            messages.error(
                request,
                'Please provide rating and review.'
            )

            return redirect(
                'book_detail',
                pk=book.id
            )

        Review.objects.create(
            customer=request.user,
            book=book,
            rating=rating,
            comment=comment
        )

        messages.success(request, 'Your review has been submitted.')

        return redirect('book_detail', pk=book.id)

    return redirect('book_detail', pk=book.id)

@login_required
def update_review(request, pk):

    review = get_object_or_404(
        Review,
        id=pk,
        customer=request.user
    )

    if request.method == 'POST':

        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '').strip()

        if not rating or not comment:

            messages.error(
                request,
                'Please provide rating and review.'
            )

            return redirect(
                'book_detail',
                pk=review.book.id
            )

        review.rating = rating
        review.comment = comment

        review.save()

        messages.success(
            request,
            'Your review has been updated.'
        )

    return redirect(
        'book_detail',
        pk=review.book.id
    )

@login_required
def delete_review(request, pk):

    review = get_object_or_404(
        Review,
        id=pk,
        customer=request.user
    )

    book_id = review.book.id

    if request.method == 'POST':

        review.delete()

        messages.success(
            request,
            'Your review has been deleted.'
        )

    return redirect(
        'book_detail',
        pk=book_id
    )


@login_required
def add_to_wishlist(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    wishlist, created = Wishlist.objects.get_or_create(
        user=request.user,
        book=book
    )

    return redirect(
        'book_detail',
        pk=book.id
    )

@login_required
def remove_from_wishlist(request, book_id):

    wishlist = get_object_or_404(
        Wishlist,
        user=request.user,
        book_id=book_id
    )

    wishlist.delete()

    return redirect(
        'book_detail',
        pk=book_id
    )

@login_required
def my_wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('book')

    context = {
        'wishlist_items': wishlist_items,
    }

    return render(
        request,
        'website/my_wishlist.html',
        context
    )

def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = sum(
                item.quantity
                for item in cart.items.all()
            )
        except Cart.DoesNotExist:
            count = 0
    else:
        count = 0

    return {
        'cart_count': count
    }

def wishlist_count(request):
    if request.user.is_authenticated:
        count = Wishlist.objects.filter(
            user=request.user
        ).count()
    else:
        count = 0

    return {
        'wishlist_count': count
    }

def about(request):

    return render(
        request,
        'website/about.html'
    )