from django.shortcuts import render, redirect, get_object_or_404
from app.models import Book, Category, Order, OrderItem, CustomerProfile, Review, Coupon
from django.db.models import Q, Count, Sum
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models.functions import TruncDate, TruncMonth, TruncYear
from datetime import datetime

# Create your views here.
@login_required
def dashboard(request):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect("index")

    # Total Orders
    total_orders = Order.objects.count()

    # Total Sales
    total_sales = Order.objects.filter(
        status='delivered'
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    # Total Customers
    total_customers = User.objects.filter(
        is_staff=False
    ).count()

    # Total Books
    total_books = Book.objects.count()

    # Top Books
    top_books = Book.objects.annotate(
).annotate(
    total_sold=Sum('order_items__quantity')
).order_by('-total_sold')[:5]
    # Recent Orders
    recent_orders = Order.objects.select_related(
        'customer',
        'customer__profile'
    ).order_by(
        '-created_at'
    )[:5]

    context = {

        'total_orders': total_orders,
        'total_sales': total_sales,
        'total_customers': total_customers,
        'total_books': total_books,
        'top_books': top_books,
        'recent_orders': recent_orders,

    }
    
    return render(
        request,
        'admin/dashboard.html',
        context
    )

@login_required
def admin_logout_view(request):

    if not request.user.is_staff:
            messages.warning(
                request,
                'You are not authorized to access admin dashboard'
            )
            return redirect("index")

    logout(request)

    messages.success(request, 'Admin has logout successfully.')

    return redirect('login')

@login_required
def book_lists(request):

    if not request.user.is_staff:
            messages.warning(
                request,
                'You are not authorized to access admin dashboard'
            )
            return redirect("index")

    books = Book.objects.all()
    categories = Category.objects.filter(status=True)

    search = request.GET.get('search', '').strip()
    category_id = request.GET.get('category', '').strip()
    status = request.GET.get('status', '').strip()

    # Search
    if search:
        books = books.filter(
            Q(title__icontains=search) |
            Q(author__icontains=search) |
            Q(isbn__icontains=search)
        )

    # Category
    if category_id:
        books = books.filter(category_id=category_id)

    # Status
    if status:
        books = books.filter(status=status)

    books = books.order_by('-created_at')

    statuses = Book.STATUS_CHOICES

    context = {
        'books': books,
        'categories': categories,
        'search': search,
        'statuses': statuses,
        'selected_category': category_id,
        'selected_status': status,
    }

    return render(
        request,
        'admin/book_lists.html',
        context
    )

@login_required
def add_book(request):

    if not request.user.is_staff:
            messages.warning(
                request,
                'You are not authorized to access admin dashboard'
            )
            return redirect("index")

    if request.method == 'POST':

        title = request.POST.get('title')
        author = request.POST.get('author')
        category_id = request.POST.get('category')
        isbn = request.POST.get('isbn')
        publisher = request.POST.get('publisher')
        published_date = request.POST.get('published_date')
        language = request.POST.get('language')
        book_format = request.POST.get('format')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        status = request.POST.get('status')
        description = request.POST.get('description')
        cover = request.FILES.get('cover')
        show_on_home = request.POST.get('show_on_home') == 'on'
        home_section = request.POST.get('home_section', 'none')

        category = Category.objects.get(id=category_id)

        Book.objects.create(
            title=title,
            cover=cover,
            author=author,
            category=category,
            isbn=isbn or None,
            publisher=publisher,
            published_date=published_date or None,
            language=language,
            format=book_format,
            price=price,
            stock=stock,
            status=status,
            description=description,
            show_on_home=show_on_home,
            home_section=home_section,
        )

        return redirect('book_lists')

    categories = Category.objects.filter(status=True)

    return render(
        request,
        'admin/add_book.html',
        {'categories': categories}
    )

@login_required
def edit_book(request, pk):

    if not request.user.is_staff:
            messages.warning(
                request,
                'You are not authorized to access admin dashboard'
            )
            return redirect("index")

    book = Book.objects.get(id=pk)

    if request.method == 'POST':

        book.title = request.POST.get('title')
        book.author = request.POST.get('author')

        category_id = request.POST.get('category')

        if category_id:
            book.category = get_object_or_404(
                Category,
                pk=category_id
            )

        book.isbn = request.POST.get('isbn') or None
        book.publisher = request.POST.get('publisher')
        book.published_date = request.POST.get('published_date') or None
        book.language = request.POST.get('language')
        book.format = request.POST.get('format')
        book.price = request.POST.get('price')
        book.stock = request.POST.get('stock')
        book.status = request.POST.get('status')
        book.description = request.POST.get('description')

        book.show_on_home = request.POST.get('show_on_home') == 'on'
        book.home_section = request.POST.get(
            'home_section',
            'none'
        )

        if request.FILES.get('cover'):
            book.cover = request.FILES.get('cover')

        book.save()

        return redirect('book_lists')

    categories = Category.objects.filter(status=True)

    return render(
        request,
        'admin/edit_book.html',
        {
            'book': book,
            'categories': categories
        }
    )

@login_required
def delete_book(request, pk):

    if not request.user.is_staff:
            messages.warning(
                request,
                'You are not authorized to access admin dashboard'
            )
            return redirect("index")
    
    book = Book.objects.get(id=pk)

    if request.method == 'POST':
        
        book.delete()
        return redirect('book_lists')

    return render(
        request,
        'admin/delete_book.html',
        {'book': book}
    )
@login_required
def categories(request):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect("index")

    # Search
    search = request.GET.get('search', '').strip()

    categories = Category.objects.annotate(
        total_books=Count('books')
    )

    if search:
        categories = categories.filter(
            name__icontains=search
        )

    context = {
        'categories': categories,
        'search': search,
    }

    return render(
        request,
        'admin/categories.html',
        context
    )

@login_required
def add_category(request):

    if not request.user.is_staff:
            messages.warning(
                request,
                'You are not authorized to access admin dashboard'
            )
            return redirect("index")

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        category = Category.objects.create(
            name=name,
            description=description,
            status = status
            )
        category.save()
        return redirect('categories')
    
    return render(
        request,
        'admin/add_category.html'
    )

@login_required
def edit_category(request, pk):

    if not request.user.is_staff:
            messages.warning(
                request,
                'You are not authorized to access admin dashboard'
            )
            return redirect("index")
    
    category = Category.objects.get(id=pk) 

    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.status = request.POST.get('status')
        category.save()
        return redirect('categories')

    return render(
        request, 
        'admin/add_category.html', 
        {'category':category}
    )

@login_required
def delete_category(request, pk):
    if not request.user.is_staff:
                messages.warning(
                    request,
                    'You are not authorized to access admin dashboard'
                )
                return redirect("index")
    
    category = Category.objects.get(id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')
    
    return render(
        request,
        'admin/delete_category.html',
        {'category':category}
    )

@login_required
def orders(request):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect("index")

    orders = Order.objects.select_related(
        'customer'
    ).order_by('-created_at')

    search = request.GET.get('search', '').strip()
    status = request.GET.get('status', '').strip()

    # Search Order ID / Customer Name / Email
    if search:
        orders = orders.filter(
            Q(id__icontains=search) |
            Q(customer__username__icontains=search) |
            Q(customer__first_name__icontains=search) |
            Q(customer__last_name__icontains=search) |
            Q(customer__email__icontains=search)
        )

    # Filter by Status
    if status:
        orders = orders.filter(
            status=status
        )

    context = {
        'orders': orders,
        'search': search,
        'selected_status': status,
    }

    return render(
        request,
        'admin/orders.html',
        context
    )

@login_required
def order_detail(request, pk):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect("index")

    order = get_object_or_404(
        Order.objects.select_related('customer'),
        id=pk
    )

    order_items = order.items.all()

    context = {
        'order': order,
        'order_items': order_items,
    }

    return render(
        request,
        'admin/order_detail.html',
        context
    )

@login_required
def update_order(request, pk):
    if not request.user.is_staff:
                    messages.warning(
                        request,
                        'You are not authorized to access admin dashboard'
                    )
                    return redirect("index")

    order = get_object_or_404(
        Order,
        id=pk
    )

    if request.method == 'POST':

        order.status = request.POST.get(
            'status'
        )

        order.payment_status = request.POST.get(
            'payment_status'
        )

        order.payment_method = request.POST.get(
            'payment_method'
        )

        order.save()

        return redirect(
            'order_detail',
            order.id
        )

    return render(
        request,
        'admin/update_order.html',
        {
            'order': order
        }
    )

@login_required
def customers(request):

    if not request.user.is_staff:
                messages.warning(
                    request,
                    'You are not authorized to access admin dashboard'
                )
                return redirect("index")

    customers = User.objects.filter(
        is_staff=False
    ).select_related(
        'profile'
    ).annotate(
        total_orders=Count('orders')
    ).order_by(
        '-date_joined'
    )

    search = request.GET.get(
        'search',
        ''
    )

    status = request.GET.get(
        'status',
        ''
    )

    if search:

        customers = customers.filter(
            Q(username__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(profile__phone__icontains=search)
        )

    if status == 'active':
        customers = customers.filter(
            is_active=True
        )
    elif status == 'blocked':
        customers = customers.filter(
            is_active=False
        )

    context = {

        'customers':customers,
        'search':search,
        'selected_status':status

    }

    return render(
        request,
        'admin/customers.html',
        context
    )

@login_required
def customer_detail(request,pk):

    if not request.user.is_staff:
                messages.warning(
                    request,
                    'You are not authorized to access admin dashboard'
                )
                return redirect("index")

    customer = User.objects.get(id=pk, is_staff=False)

    orders = Order.objects.filter(
        customer=customer
        ).order_by(
        '-created_at'
    )

    total_orders = orders.count()

    total_spending = sum(
        order.total_amount
        for order in orders
        if order.payment_status == 'paid'
    )

    last_order = orders.first()

    context = {

        'customer': customer,
        'orders': orders,
        'total_orders': total_orders,
        'total_spending': total_spending,
        'last_order': last_order,
    }

    return render(
        request,
        'admin/customer_detail.html',
        context
    )


def reports(request):
    return render(request, 'admin/reports.html')

def settings(request):
    return render(request, 'admin/settings.html')

def admin_profile(request):
    return render(request, 'admin/admin_profile.html')

@login_required
def edit_customer(request, pk):

    if not request.user.is_staff:
                messages.warning(
                    request,
                    'You are not authorized to access admin dashboard'
                )
                return redirect("index")

    customer = User.objects.get(id=pk, is_staff=False)

    profile, created = CustomerProfile.objects.get_or_create(user=customer)

    if request.method == 'POST':

        # Customer Information

        customer.email = request.POST.get('email')

        status = request.POST.get('status')

        if status == 'active':

            customer.is_active = True

        elif status == 'blocked':

            customer.is_active = False


        customer.save()


        # =========================
        # Customer Profile
        # =========================

        profile.full_name = request.POST.get('full_name')

        profile.phone = request.POST.get('phone')

        profile.address = request.POST.get('address')

        profile.city = request.POST.get('city')

        profile.country = request.POST.get('country')

        # Customer Profile

        if request.FILES.get('profile_image'):

            profile.profile_image = request.FILES.get(
                'profile_image'
            )


        profile.save()


        return redirect(
            'customer_detail',
            customer.id
        )

    context = {

        'customer': customer,
        'profile': profile,

    }

    return render(
        request,
        'admin/edit_customer.html',
        context
    )

@login_required
def delete_customer(request, pk):

    if not request.user.is_staff:
                messages.warning(
                    request,
                    'You are not authorized to access admin dashboard'
                )
                return redirect("index")

    customer = User.objects.get(id=pk, is_staff=False)

    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer account deleted successfully.')
        return redirect('customers')
    return redirect('customer_detail', customer.id)

@login_required
def reviews(request):

    if not request.user.is_staff:
                messages.warning(
                    request,
                    'You are not authorized to access admin dashboard'
                )
                return redirect("index")

    reviews = Review.objects.select_related(
        'customer',
        'book'
    )

    search = request.GET.get(
        'search',
        ''
    )

    status = request.GET.get(
        'status',
        ''
    )


    # Search

    if search:

        reviews = reviews.filter(

            Q(
                customer__profile__full_name__icontains=search
            ) |

            Q(
                book__title__icontains=search
            ) |

            Q(
                comment__icontains=search
            )

        )


    # Status Filter

    if status:

        reviews = reviews.filter(
            status=status
        )


    context = {

        'reviews': reviews,

        'search': search,

        'selected_status': status,

    }


    return render(
        request,
        'admin/reviews.html',
        context
    )

@login_required
def review_detail(request, pk):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect('index')

    review = get_object_or_404(
        Review.objects.select_related(
            'customer',
            'book'
        ),
        id=pk
    )

    context = {
        'review': review,
    }

    return render(
        request,
        'admin/review_detail.html',
        context
    )

@login_required
def update_review_status(request, pk):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect('index')

    review = get_object_or_404(Review,id=pk)

    if request.method == 'POST':

        status = request.POST.get('status')

        if status in ['published', 'pending']:

            review.status = status
            review.save()

        return redirect('review_detail',review.id)

    return redirect('review_detail',review.id)

@login_required
def delete_review(request, pk):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect('index')

    if request.method == 'POST':

        review = get_object_or_404(
            Review,
            pk=pk
        )

        review.delete()

        messages.success(
            request,
            'Review deleted successfully.'
        )

        return redirect('reviews')

    return redirect('reviews')

@login_required
def coupons(request):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect('index')

    coupons = Coupon.objects.all()

    search = request.GET.get(
        'search',
        ''
    )

    status = request.GET.get(
        'status',
        ''
    )

    # Search

    if search:

        coupons = coupons.filter(
            code__icontains=search
        )

    # Status Filter

    if status:

        coupons = coupons.filter(
            status=status
        )

    context = {

        'coupons': coupons,

        'search': search,

        'selected_status': status,

    }

    return render(
        request,
        'admin/coupons.html',
        context
    )
@login_required
def add_coupon(request):
    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect('index')

    if request.method == 'POST':
        code = request.POST.get('code')
        discount = request.POST.get('discount')
        discount_type = request.POST.get('discount_type', 'percentage')
        status = request.POST.get('status', 'active')
        expiry_date = request.POST.get('expiry_date')

        Coupon.objects.create(
            code=code,
            discount=discount if discount else 0,
            discount_type=discount_type,
            status=status,
            expiry_date=expiry_date if expiry_date else None
        )

        messages.success(
            request,
            'Coupon added successfully.'
        )
        return redirect('coupons')

    return render(request, 'admin/add_coupon.html')

def edit_coupon(request, pk):
    coupon = get_object_or_404(Coupon, id=pk)
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorized to access admin dashboard')
        return redirect('index')

    if request.method == 'POST':
        coupon.code = request.POST.get('code')
        coupon.discount = request.POST.get('discount_value')
        coupon.discount_type = request.POST.get('discount_type', 'percentage')
        coupon.status = request.POST.get('status', 'active')
        coupon.expiry_date = request.POST.get('expiry_date') or None
        

        coupon.save()
        messages.success(request, 'Coupon updated successfully.')
        return redirect('coupons')
    
    return render(request, 'admin/edit_coupon.html', {'coupon': coupon})

def delete_coupon(request, pk):
    coupon = get_object_or_404(Coupon, id=pk)
    coupon.delete()
    messages.success(request, 'Coupon deleted successfully.')
    return redirect('coupons')


@login_required
def reports(request):

    if not request.user.is_staff:
        messages.warning(
            request,
            'You are not authorized to access admin dashboard'
        )
        return redirect('index')


    
    # Date Filter

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    report_type = request.GET.get('report_type')


    orders = Order.objects.all()


    if start_date:
        orders = orders.filter(
            created_at__date__gte=start_date
        )


    if end_date:
        orders = orders.filter(
            created_at__date__lte=end_date
        )

    # Statistics

    total_orders = orders.count()


    total_revenue = orders.aggregate(
        total=Sum('total_amount')
    )['total'] or 0


    books_sold = OrderItem.objects.filter(
        order__in=orders
    ).aggregate(
        total=Sum('quantity')
    )['total'] or 0


    if total_orders > 0:
        average_order = total_revenue / total_orders
    else:
        average_order = 0


    # Report Data

    reports = []


    if report_type == 'daily':

        daily_reports = orders.annotate(
            period=TruncDate('created_at')
        ).values(
            'period'
        ).annotate(
            total_orders=Count('id'),
            revenue=Sum('total_amount')
        ).order_by('-period')


        for report in daily_reports:

            report_orders = orders.filter(
                created_at__date=report['period']
            )


            sold = OrderItem.objects.filter(
                order__in=report_orders
            ).aggregate(
                total=Sum('quantity')
            )['total'] or 0


            revenue = report['revenue'] or 0
            order_count = report['total_orders']


            reports.append({
                'period': report['period'],
                'total_orders': order_count,
                'books_sold': sold,
                'revenue': revenue,
                'average_order': (
                    revenue / order_count
                    if order_count > 0
                    else 0
                ),
            })


    elif report_type == 'yearly':

        yearly_reports = orders.annotate(
            period=TruncYear('created_at')
        ).values(
            'period'
        ).annotate(
            total_orders=Count('id'),
            revenue=Sum('total_amount')
        ).order_by('-period')


        for report in yearly_reports:

            report_orders = orders.filter(
                created_at__year=report['period'].year
            )


            sold = OrderItem.objects.filter(
                order__in=report_orders
            ).aggregate(
                total=Sum('quantity')
            )['total'] or 0


            revenue = report['revenue'] or 0
            order_count = report['total_orders']


            reports.append({
                'period': report['period'],
                'total_orders': order_count,
                'books_sold': sold,
                'revenue': revenue,
                'average_order': (
                    revenue / order_count
                    if order_count > 0
                    else 0
                ),
            })


    else:

        monthly_reports = orders.annotate(
            period=TruncMonth('created_at')
        ).values(
            'period'
        ).annotate(
            total_orders=Count('id'),
            revenue=Sum('total_amount')
        ).order_by('-period')


        for report in monthly_reports:

            report_orders = orders.filter(
                created_at__year=report['period'].year,
                created_at__month=report['period'].month
            )


            sold = OrderItem.objects.filter(
                order__in=report_orders
            ).aggregate(
                total=Sum('quantity')
            )['total'] or 0


            revenue = report['revenue'] or 0
            order_count = report['total_orders']


            reports.append({
                'period': report['period'],
                'total_orders': order_count,
                'books_sold': sold,
                'revenue': revenue,
                'average_order': (
                    revenue / order_count
                    if order_count > 0
                    else 0
                ),
            })


    context = {

        'total_revenue': total_revenue,

        'total_orders': total_orders,

        'books_sold': books_sold,

        'average_order': average_order,

        'reports': reports,

    }


    return render(
        request,
        'admin/reports.html',
        context
    )