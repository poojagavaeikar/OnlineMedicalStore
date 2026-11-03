from django.shortcuts import render, redirect
from django.db.models import Q, F, Sum
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from datetime import date, timedelta
from decimal import Decimal
from .models import (Medicine,Category,Manufacturer,Supplier,Purchase,PurchaseItem,Prescription,Order,
    OrderItem,
    Delivery,
    Sale,
    SaleItem,
    Payment,
)
import json



#========================================
#MEDICINE_LIST #
#========================================
def medicine_list(request):
    medicines = Medicine.objects.filter(is_deleted=False)

    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    status_filter = request.GET.get('status', '')
    stock_filter = request.GET.get('stock', '')

    # Search
    if search_query:
        medicines = medicines.filter(
            Q(medicine_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(generic_name__icontains=search_query) |
            Q(brand__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )

    # Category Filter
    if category_filter:
        medicines = medicines.filter(
            category__iexact=category_filter
        )

    # Status Filter
    if status_filter:
        medicines = medicines.filter(
            status__iexact=status_filter
        )

    # =========================================
    # STOCK FILTER
    # =========================================
    
    if stock_filter == 'in_stock':
        medicines = medicines.filter(
            stock__gt=F('low_stock_limit')
        )
    elif stock_filter == 'low_stock':
        medicines = medicines.filter(
            stock__gt=0,
            stock__lte=F('low_stock_limit')
        )

    elif stock_filter == 'out_of_stock':
        medicines = medicines.filter(
            stock=0
        )

    # Category Dropdown
    categories = Medicine.objects.filter(
        is_deleted=False
    ).exclude(
        category=''
    ).exclude(
        category__isnull=True
    ).values_list(
        'category',
        flat=True
    ).distinct()

    # Summary Cards
    total_medicines = Medicine.objects.filter(
        is_deleted=False
    ).count()

    active_medicines = Medicine.objects.filter(
        is_deleted=False,
        stock__gt=0
    ).count()

    low_stock = Medicine.objects.filter(
        is_deleted=False,
        stock__gt=0,
        stock__lte=9
    ).count()

    today = timezone.now().date()
    expiring_date = today + timedelta(days=30)

    expiring_soon = Medicine.objects.filter(
        is_deleted=False,
        expiry_date__gte=today,
        expiry_date__lte=expiring_date
    ).count()

    return render(
        request,
        'store/medicine_master/medicine_list.html',
        {
            'medicines': medicines,
            'categories': categories,
            'total_medicines': total_medicines,
            'active_medicines': active_medicines,
            'low_stock': low_stock,
            'expiring_soon': expiring_soon
        }
    )
    
# =========================================
# CATEGORY MASTER
# =========================================

def category_list(request):
    categories = Category.objects.filter(is_deleted=False)
      
    # Search
    
    search_query = request.GET.get('search', '')

    if search_query:
        categories = categories.filter(
            Q(category_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    
    # Status Filter
    
    status_filter = request.GET.get('status', '')

    if status_filter:
        categories = categories.filter(
            status__iexact=status_filter
        )
    

    total_categories = Category.objects.filter(
        is_deleted=False
    ).count()

    active_categories = Category.objects.filter(
        is_deleted=False,
        status='Active'
    ).count()

    inactive_categories = Category.objects.filter(
        is_deleted=False,
        status='Inactive'
    ).count()

    return render(
        request,
        'store/category_master/category_list.html',
        {
            'categories': categories,
            'total_categories': total_categories,
            'active_categories': active_categories,
            'inactive_categories': inactive_categories
        }
    )
    
# =========================================
# ADD CATEGORY
# =========================================

def add_category(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        description = request.POST.get('description') or ''
        status = request.POST.get('status') or 'Active'

        Category.objects.create(
            name=name,
            description=description,
            status=status
        )

        return redirect('category_list')

    return render(
        request,
        'store/category_master/add_category.html'
    )
    
    
    # =========================================
# VIEW CATEGORY
# =========================================

def view_category(request, id):

    category = Category.objects.get(
        id=id,
        is_deleted=False
    )

    return render(
        request,
        'store/category_master/view_category.html',
        {
            'category': category
        }
    )
    
    
# =========================================
# EDIT CATEGORY
# =========================================

def edit_category(request, id):

    category = Category.objects.get(
        id=id,
        is_deleted=False
    )

    if request.method == 'POST':

        category.name = request.POST.get('name')
        category.description = request.POST.get('description') or ''
        category.status = request.POST.get('status') or 'Active'

        category.save()

        return redirect('category_list')

    return render(
        request,
        'store/category_master/edit_category.html',
        {
            'category': category
        }
    )
    
    
# =========================================
# DELETE CATEGORY
# =========================================


def delete_category(request, id):

    category = Category.objects.get(
        id=id,
        is_deleted=False
    )

    if request.method == 'POST':

        category.is_deleted = True
        category.save()

        return redirect('category_list')

    return render(
        request,
        'store/category_master/delete_category.html',
        {
            'category': category
        }
    )
    
    
# =========================================
# DELETED CATEGORIES
# =========================================

def deleted_categories(request):

    categories = Category.objects.filter(
        is_deleted=True
    )

    return render(
        request,
        'store/category_master/deleted_categories.html',
        {
            'categories': categories
        }
    )


# =========================================
# RESTORE CATEGORY
# =========================================

def restore_category(request, id):

    category = Category.objects.get(
        id=id,
        is_deleted=True
    )

    category.is_deleted = False
    category.save()

    return redirect('deleted_categories')
    
    
 

# =========================================
# MANUFACTURER MASTER
# =========================================

def manufacturer_list(request):

    manufacturers = Manufacturer.objects.filter(
        is_deleted=False
    )

    # =========================================
    # SEARCH
    # =========================================

    search_query = request.GET.get('search', '')

    if search_query:
        manufacturers = manufacturers.filter(
            Q(manufacturer_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    # =========================================
    # STATUS FILTER
    # =========================================

    status_filter = request.GET.get('status', '')

    if status_filter:
        manufacturers = manufacturers.filter(
            status__iexact=status_filter
        )

    # =========================================
    # SUMMARY COUNTS
    # =========================================

    total_manufacturers = Manufacturer.objects.filter(
        is_deleted=False
    ).count()

    active_manufacturers = Manufacturer.objects.filter(
        is_deleted=False,
        status='Active'
    ).count()

    inactive_manufacturers = Manufacturer.objects.filter(
        is_deleted=False,
        status='Inactive'
    ).count()

    return render(
        request,
        'store/manufacturer_master/manufacturer_list.html',
        {
            'manufacturers': manufacturers,
            'total_manufacturers': total_manufacturers,
            'active_manufacturers': active_manufacturers,
            'inactive_manufacturers': inactive_manufacturers
        }
    )
     #  ADD MANUFACTURER #
       
    
def add_manufacturer(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        contact_person = request.POST.get('contact_person') or ''
        phone = request.POST.get('phone') or ''
        email = request.POST.get('email') or ''
        address = request.POST.get('address') or ''
        status = request.POST.get('status') or 'Active'

        Manufacturer.objects.create(
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            status=status
        )

        return redirect('manufacturer_list')

    return render(
        request,
        'store/manufacturer_master/add_manufacturer.html'
    )
    
      
 #  VIEW MANUFACTURER #       
    
def view_manufacturer(request, id):
    

    manufacturer = Manufacturer.objects.get(
        id=id,
        is_deleted=False
    )

    return render(
        request,
        'store/manufacturer_master/view_manufacturer.html',
        {
            'manufacturer': manufacturer
        }
    )
      
# =========================================
# EDIT MANUFACTURER
# =========================================

def edit_manufacturer(request, id):

    manufacturer = Manufacturer.objects.get(
        id=id,
        is_deleted=False
    )

    if request.method == 'POST':

        manufacturer.name = request.POST.get('name')
        manufacturer.contact_person = request.POST.get('contact_person') or ''
        manufacturer.phone = request.POST.get('phone') or ''
        manufacturer.email = request.POST.get('email') or ''
        manufacturer.address = request.POST.get('address') or ''
        manufacturer.status = request.POST.get('status') or 'Active'

        manufacturer.save()

        return redirect('manufacturer_list')

    return render(
        request,
        'store/manufacturer_master/edit_manufacturer.html',
        {
            'manufacturer': manufacturer
        }
    )
    
# =========================================
# DELETE MANUFACTURER
# =========================================

def delete_manufacturer(request, id):

    manufacturer = Manufacturer.objects.get(
        id=id,
        is_deleted=False
    )

    if request.method == 'POST':

        manufacturer.is_deleted = True
        manufacturer.save()

        return redirect('manufacturer_list')

    return render(
        request,
        'store/manufacturer_master/delete_manufacturer.html',
        {
            'manufacturer': manufacturer
        }
    )
    
    
# =========================================
# DELETED MANUFACTURERS
# =========================================

def deleted_manufacturers(request):

    manufacturers = Manufacturer.objects.filter(
        is_deleted=True
    )

    return render(
        request,
        'store/manufacturer_master/deleted_manufacturers.html',
        {
            'manufacturers': manufacturers
        }
    )
    
    
# =========================================
# RESTORE MANUFACTURER
# =========================================

def restore_manufacturer(request, id):

    manufacturer = Manufacturer.objects.get(
        id=id,
        is_deleted=True
    )

    manufacturer.is_deleted = False
    manufacturer.save()

    return redirect('deleted_manufacturers')



# =========================================
# SUPPLIER MASTER
# =========================================

def supplier_list(request):

    suppliers = Supplier.objects.filter(
        is_deleted=False
    )
    
#======================
#SUPPLIER
# =========================================
    search_query = request.GET.get('search', '')

    if search_query:
        suppliers = suppliers.filter(
            Q(supplier_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(contact_person__icontains=search_query) |
            Q(phone__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(gst_number__icontains=search_query)
        )   
# =========================================
# STATUS FILTER
# =========================================
 
    status_filter = request.GET.get('status', '')

    if status_filter:
        suppliers = suppliers.filter(status__iexact=status_filter)
        
        
        
# =========================================
# SUMMARY COUNTS
# =========================================

    total_suppliers = Supplier.objects.filter(
        is_deleted=False
    ).count()

    active_suppliers = Supplier.objects.filter(
        is_deleted=False,
        status='Active'
    ).count()

    inactive_suppliers = Supplier.objects.filter(
        is_deleted=False,
        status='Inactive'
    ).count()

    return render(
        request,
        'store/supplier_master/supplier_list.html',
        {
            'suppliers': suppliers,
            'total_suppliers': total_suppliers,
            'active_suppliers': active_suppliers,
            'inactive_suppliers': inactive_suppliers
        }
    )

# =========================================
# ADD SUPPLIER
# =========================================

def add_supplier(request):

    if request.method == 'POST':

        Supplier.objects.create(
            name=request.POST.get('name'),
            contact_person=request.POST.get('contact_person'),
            phone=request.POST.get('phone'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            gst_number=request.POST.get('gst_number'),
            status=request.POST.get('status', 'Active')
        )

        return redirect('supplier_list')

    return render(
        request,
        'store/supplier_master/add_supplier.html'
    )


# =========================================
# VIEW SUPPLIER
# =========================================
def view_supplier(request, id):
    supplier = Supplier.objects.get(id=id, is_deleted=False)

    return render(
        request,
        'store/supplier_master/view_supplier.html',
        {
            'supplier': supplier
        }
    )
    
    
# =========================================
# EDIT SUPPLIER
# =========================================
def edit_supplier(request, id):
    supplier = Supplier.objects.get(id=id, is_deleted=False)

    if request.method == 'POST':
        supplier.name = request.POST.get('name')
        supplier.contact_person = request.POST.get('contact_person')
        supplier.phone = request.POST.get('phone')
        supplier.email = request.POST.get('email')
        supplier.address = request.POST.get('address')
        supplier.gst_number = request.POST.get('gst_number')
        supplier.status = request.POST.get('status', 'Active')

        supplier.save()

        return redirect('supplier_list')

    return render(
        request,
        'store/supplier_master/edit_supplier.html',
        {
            'supplier': supplier
        }
    )
    
# =========================================
# DELETE SUPPLIER
# =========================================
def delete_supplier(request, id):
    supplier = Supplier.objects.get(id=id, is_deleted=False)

    if request.method == 'POST':
        supplier.is_deleted = True
        supplier.save()

        return redirect('supplier_list')

    return render(
        request,
        'store/supplier_master/delete_supplier.html',
        {
            'supplier': supplier
        }
    )
    
# =========================================
# DELETED SUPPLIERS
# =========================================
def deleted_suppliers(request):
    suppliers = Supplier.objects.filter(is_deleted=True)

    return render(
        request,
        'store/supplier_master/deleted_suppliers.html',
        {
            'suppliers': suppliers
        }
    )
    
# =========================================
# RESTORE SUPPLIER
# =========================================
def restore_supplier(request, id):
    supplier = Supplier.objects.get(id=id, is_deleted=True)

    supplier.is_deleted = False
    supplier.save()

    return redirect('deleted_suppliers')


# =========================================
# CREATE ONLINE ORDER
# =========================================
def create_order(request):

    # =========================================
    # ACTIVE MEDICINES
    # =========================================
    medicines = Medicine.objects.filter(
        is_deleted=False,
        status='Active',
        stock__gt=0
    ).order_by('name')

    # =========================================
    # CREATE ORDER - POST
    # =========================================
    if request.method == 'POST':

        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email') or ''
        delivery_address = request.POST.get('delivery_address') #delivary address
        delivery_pincode = request.POST.get('delivery_pincode') #pincode
                # =========================================
        # CALCULATE EXPECTED DELIVERY DATE
        # =========================================
        pharmacy_pincode = '462001'

        if delivery_pincode == pharmacy_pincode:
            delivery_days = 1

        elif delivery_pincode.startswith('462'):
            delivery_days = 2

        else:
            delivery_days = 5

        expected_delivery_date = (
            timezone.localdate() + timedelta(days=delivery_days)
        )
        payment_method = request.POST.get('payment_method')    #payment method
        medicine_id = request.POST.get('medicine')
        quantity = int(request.POST.get('quantity') or 1)
        notes = request.POST.get('notes') or ''

        # =========================================
        # GET SELECTED MEDICINE
        # =========================================
        medicine = Medicine.objects.get(
            id=medicine_id,
            is_deleted=False,
            status='Active'
        )

        # =========================================
        # CHECK AVAILABLE STOCK
        # =========================================
        if quantity > medicine.stock:

            return render(
                request,
                'store/online_orders/create_order.html',
                {
                    'medicines': medicines,
                    'error': 'Requested quantity is greater than available stock.'
                }
            )

        # =========================================
        # CHECK SELLING RATE
        # =========================================
        if medicine.selling_rate is None:

            return render(
                request,
                'store/online_orders/create_order.html',
                {
                    'medicines': medicines,
                    'error': 'Selling rate is not available for this medicine.'
                }
            )

        # =========================================
        # CALCULATE TOTAL
        # =========================================
        total_amount = medicine.selling_rate * quantity

        # =========================================
        # CREATE ORDER
        # =========================================
        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            email=email,
            delivery_address=delivery_address,
            delivery_pincode=delivery_pincode,
            expected_delivery_date=expected_delivery_date,
            payment_method=payment_method,
            payment_status='Pending',
            status='Pending',
            total_amount=total_amount,
            notes=notes
        )

        # =========================================
        # CREATE ORDER ITEM
        # =========================================
        OrderItem.objects.create(
            order=order,
            medicine=medicine,
            quantity=quantity,
            selling_rate=medicine.selling_rate
        )

        # =========================================
        # OPEN CREATED ORDER
        # =========================================
        return redirect(
            'view_order',
            id=order.id
        )

    # =========================================
    # OPEN CREATE ORDER PAGE
    # =========================================
    return render(
        request,
        'store/online_orders/create_order.html',
        {
            'medicines': medicines
        }
    )
    # =========================================
# ONLINE ORDER LIST
# =========================================
def order_list(request):

    # =========================================
    # ACTIVE / NON-DELETED ORDERS
    # =========================================
    orders = Order.objects.filter(
        is_deleted=False
    ).order_by(
        'id'
    )

    # =========================================
    # SEARCH
    # =========================================
    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:
        orders = orders.filter(
            Q(order_id__icontains=search)
            |
            Q(customer_name__icontains=search)
            |
            Q(phone__icontains=search)
        )

    # =========================================
    # STATUS FILTER
    # =========================================
    status = request.GET.get(
        'status',
        ''
    ).strip()

    if status:
        orders = orders.filter(
            status=status
        )

    # =========================================
    # ORDER SUMMARY COUNTS
    # =========================================
    total_orders = Order.objects.filter(
        is_deleted=False
    ).count()

    pending_orders = Order.objects.filter(
        is_deleted=False,
        status='Pending'
    ).count()

    confirmed_orders = Order.objects.filter(
        is_deleted=False,
        status='Confirmed'
    ).count()

    delivered_orders = Order.objects.filter(
        is_deleted=False,
        status='Delivered'
    ).count()

    # =========================================
    # SEND DATA TO TEMPLATE
    # =========================================
    return render(
        request,
        'store/online_orders/order_list.html',
        {
            'orders': orders,
            'search': search,
            'selected_status': status,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'confirmed_orders': confirmed_orders,
            'delivered_orders': delivered_orders,
        }
    )


# =========================================
# VIEW ONLINE ORDER
# =========================================
def view_order(request, id):

    # =========================================
    # GET ORDER
    # =========================================
    order = Order.objects.get(
        id=id
    )

    # =========================================
    # SEND DATA TO TEMPLATE
    # =========================================
    return render(
        request,
        'store/online_orders/view_order.html',
        {
            'order': order
        }
    )


# =========================================
# CUSTOMER ORDER TRACKING
# =========================================
def track_order(request, order_id):

    # =========================================
    # GET ORDER BY ORDER ID
    # =========================================
    order = Order.objects.filter(
        order_id=order_id,
        is_deleted=False
    ).first()

    # =========================================
    # ORDER NOT FOUND
    # =========================================
    if not order:
        return render(
            request,
            'store/online_orders/track_order.html',
            {
                'order': None,
                'verified': False,
                'error': 'Order not found.'
            }
        )

    # =========================================
    # VERIFY CUSTOMER PHONE NUMBER
    # =========================================
    if request.method == 'POST':

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        if phone == order.phone:

            return render(
                request,
                'store/online_orders/track_order.html',
                {
                    'order': order,
                    'verified': True
                }
            )

        return render(
            request,
            'store/online_orders/track_order.html',
            {
                'order': order,
                'verified': False,
                'error': 'Phone number does not match this order.'
            }
        )

    # =========================================
    # FIRST OPEN - HIDE ORDER DETAILS
    # =========================================
    return render(
        request,
        'store/online_orders/track_order.html',
        {
            'order': order,
            'verified': False
        }
    )


# =========================================
# CUSTOMER TRACK ORDER SEARCH
# =========================================
def track_order_search(request):

    # =========================================
    # SEARCH FORM SUBMITTED
    # =========================================
    if request.method == 'POST':

        order_id = request.POST.get(
            'order_id',
            ''
        ).strip()

        phone = request.POST.get(
            'phone',
            ''
        ).strip()

        # =========================================
        # FIND ORDER USING ORDER ID + PHONE
        # =========================================
        order = Order.objects.filter(
            order_id=order_id,
            phone=phone,
            is_deleted=False
        ).first()

        # =========================================
        # CORRECT ORDER DETAILS
        # =========================================
        if order:

            return render(
                request,
                'store/online_orders/track_order.html',
                {
                    'order': order,
                    'verified': True
                }
            )

        # =========================================
        # WRONG ORDER ID OR PHONE
        # =========================================
        return render(
            request,
            'store/online_orders/track_order_search.html',
            {
                'error': (
                    'Order ID or registered phone '
                    'number is incorrect.'
                ),
                'order_id': order_id
            }
        )

    # =========================================
    # FIRST TIME PAGE OPEN
    # =========================================
    return render(
        request,
        'store/online_orders/track_order_search.html'
    )


# =========================================
# EDIT ONLINE ORDER
# =========================================
def edit_order(request, id):

    # =========================================
    # GET ORDER
    # =========================================
    order = Order.objects.get(
        id=id,
        is_deleted=False
    )

    # =========================================
    # EDIT ONLY ALLOWED ORDER STATUS
    # =========================================
    if order.status not in [
        'Pending',
        'Confirmed',
        'Packed'
    ]:
        return redirect(
            'view_order',
            id=order.id
        )

    # =========================================
    # ACTIVE MEDICINES
    # =========================================
    medicines = Medicine.objects.filter(
        is_deleted=False,
        status='Active'
    ).order_by(
        'name'
    )

    # =========================================
    # UPDATE ORDER - POST
    # =========================================
    if request.method == 'POST':

        customer_name = request.POST.get(
            'customer_name'
        )

        phone = request.POST.get(
            'phone'
        )

        email = request.POST.get(
            'email'
        ) or ''

        delivery_address = request.POST.get(
            'delivery_address'
        )

        delivery_pincode = (
            request.POST.get('delivery_pincode')
            or order.delivery_pincode
            or ''
        )

        payment_method = request.POST.get(
            'payment_method'
        )

        notes = request.POST.get(
            'notes'
        ) or ''

        # =========================================
        # RECALCULATE EXPECTED DELIVERY DATE
        # =========================================
        pharmacy_pincode = '462001'

        if delivery_pincode == pharmacy_pincode:
            delivery_days = 1

        elif delivery_pincode.startswith('462'):
            delivery_days = 2

        else:
            delivery_days = 5

        expected_delivery_date = (
            timezone.localdate()
            + timedelta(days=delivery_days)
        )

        # =========================================
        # UPDATE CUSTOMER / DELIVERY DETAILS
        # =========================================
        order.customer_name = customer_name
        order.phone = phone
        order.email = email
        order.delivery_address = delivery_address
        order.delivery_pincode = delivery_pincode
        order.expected_delivery_date = (
            expected_delivery_date
        )
        order.payment_method = payment_method
        order.notes = notes

        # =========================================
        # PENDING ORDER - UPDATE MEDICINE
        # =========================================
        if order.status == 'Pending':

            medicine_id = request.POST.get(
                'medicine'
            )

            quantity = int(
                request.POST.get('quantity') or 1
            )

            medicine = Medicine.objects.get(
                id=medicine_id,
                is_deleted=False,
                status='Active'
            )

            # =========================================
            # CHECK AVAILABLE STOCK
            # =========================================
            if quantity > medicine.stock:

                return render(
                    request,
                    'store/online_orders/edit_order.html',
                    {
                        'order': order,
                        'medicines': medicines,
                        'error': (
                            'Requested quantity is greater '
                            'than available stock.'
                        )
                    }
                )

            # =========================================
            # CHECK SELLING RATE
            # =========================================
            if medicine.selling_rate is None:

                return render(
                    request,
                    'store/online_orders/edit_order.html',
                    {
                        'order': order,
                        'medicines': medicines,
                        'error': (
                            'Selling rate is not available '
                            'for this medicine.'
                        )
                    }
                )

            # =========================================
            # UPDATE ORDER ITEM
            # =========================================
            order_item = order.items.first()

            order_item.medicine = medicine
            order_item.quantity = quantity
            order_item.selling_rate = (
                medicine.selling_rate
            )
            order_item.save()

            # =========================================
            # RECALCULATE ORDER TOTAL
            # =========================================
            order.total_amount = (
                medicine.selling_rate
                * quantity
            )

        # =========================================
        # SAVE UPDATED ORDER
        # =========================================
        order.save()

        return redirect(
            'view_order',
            id=order.id
        )

    # =========================================
    # OPEN EDIT ORDER PAGE
    # =========================================
    return render(
        request,
        'store/online_orders/edit_order.html',
        {
            'order': order,
            'medicines': medicines
        }
    )


# =========================================
# CONFIRM ONLINE ORDER
# =========================================
def confirm_order(request, id):

    # =========================================
    # POST REQUEST ONLY
    # =========================================
    if request.method == 'POST':

        # =========================================
        # DATABASE TRANSACTION
        # =========================================
        with transaction.atomic():

            order = Order.objects.select_for_update().get(
                id=id,
                is_deleted=False
            )

            # =========================================
            # CONFIRM ONLY PENDING ORDER
            # =========================================
            if (
                order.status == 'Pending'
                and not order.stock_updated
            ):

                # =========================================
                # CHECK AVAILABLE STOCK
                # =========================================
                for item in order.items.all():

                    medicine = (
                        Medicine.objects
                        .select_for_update()
                        .get(
                            id=item.medicine_id
                        )
                    )

                    if medicine.stock < item.quantity:
                        return redirect(
                            'view_order',
                            id=order.id
                        )

                # =========================================
                # DEDUCT MEDICINE STOCK
                # =========================================
                for item in order.items.all():

                    Medicine.objects.filter(
                        id=item.medicine_id
                    ).update(
                        stock=F('stock') - item.quantity
                    )

                # =========================================
                # UPDATE ORDER + CONFIRMED TIME
                # =========================================
                order.status = 'Confirmed'
                order.stock_updated = True
                order.confirmed_at = timezone.now()

                order.save(
                    update_fields=[
                        'status',
                        'stock_updated',
                        'confirmed_at'
                    ]
                )

        return redirect(
            'view_order',
            id=order.id
        )

    return redirect(
        'order_list'
    )


# =========================================
# PACK ONLINE ORDER
# =========================================
def pack_order(request, id):

    if request.method == 'POST':

        order = Order.objects.get(
            id=id,
            is_deleted=False
        )

        # =========================================
        # CONFIRMED -> PACKED
        # =========================================
        if order.status == 'Confirmed':

            order.status = 'Packed'
            order.packed_at = timezone.now()

            order.save(
                update_fields=[
                    'status',
                    'packed_at'
                ]
            )

        return redirect(
            'view_order',
            id=order.id
        )

    return redirect(
        'order_list'
    )


# =========================================
# SHIP ONLINE ORDER
# =========================================
def ship_order(request, id):

    if request.method == 'POST':

        order = Order.objects.get(
            id=id,
            is_deleted=False
        )

        # =========================================
        # PACKED -> SHIPPED
        # =========================================
        if order.status == 'Packed':

            order.status = 'Shipped'
            order.shipped_at = timezone.now()

            order.save(
                update_fields=[
                    'status',
                    'shipped_at'
                ]
            )

        return redirect(
            'view_order',
            id=order.id
        )

    return redirect(
        'order_list'
    )


# =========================================
# OUT FOR DELIVERY ONLINE ORDER
# =========================================
def out_for_delivery_order(request, id):

    if request.method == 'POST':

        order = Order.objects.get(
            id=id,
            is_deleted=False
        )

        # =========================================
        # SHIPPED -> OUT FOR DELIVERY
        # =========================================
        if order.status == 'Shipped':

            order.status = 'Out for Delivery'
            order.out_for_delivery_at = (
                timezone.now()
            )

            order.save(
                update_fields=[
                    'status',
                    'out_for_delivery_at'
                ]
            )

            # =========================================
            # SYNC DELIVERY RECORD
            # =========================================
            Delivery.objects.filter(
                order=order
            ).update(
                status='Out for Delivery'
            )

        return redirect(
            'view_order',
            id=order.id
        )

    return redirect(
        'order_list'
    )

# =========================================
# OUT FOR DELIVERY ONLINE ORDER
# =========================================
def out_for_delivery_order(request, id):

    # =========================================
    # POST REQUEST ONLY
    # =========================================
    if request.method == 'POST':

        order = Order.objects.get(
            id=id,
            is_deleted=False
        )

        # =========================================
        # SHIPPED -> OUT FOR DELIVERY
        # =========================================
        if order.status == 'Shipped':

            order.status = 'Out for Delivery'
            order.out_for_delivery_at = timezone.now()

            order.save(
                update_fields=[
                    'status',
                    'out_for_delivery_at'
                ]
            )

            # =========================================
            # SYNC DELIVERY RECORD
            # =========================================
            Delivery.objects.filter(
                order=order
            ).update(
                status='Out for Delivery'
            )

        return redirect(
            'view_order',
            id=order.id
        )

    return redirect(
        'order_list'
    )
# =========================================
# DELIVER ONLINE ORDER
# =========================================
def deliver_order(request, id):

    # =========================================
    # POST REQUEST ONLY
    # =========================================
    if request.method == 'POST':

        order = Order.objects.get(
            id=id,
            is_deleted=False
        )

        # =========================================
        # OUT FOR DELIVERY -> DELIVERED
        # =========================================
        if order.status == 'Out for Delivery':

            order.status = 'Delivered'
            order.delivered_at = timezone.now()

            # =========================================
            # COD PAYMENT RECEIVED
            # =========================================
            if order.payment_method == 'COD':

                order.payment_status = 'Paid'

                order.save(
                    update_fields=[
                        'status',
                        'delivered_at',
                        'payment_status'
                    ]
                )

                # =========================================
                # CREATE / UPDATE PAYMENT RECORD
                # =========================================
                payment, created = Payment.objects.get_or_create(
                    source='Online Order',
                    reference_id=order.order_id,
                    defaults={
                        'customer_name': order.customer_name,
                        'amount': order.total_amount,
                        'payment_method': 'COD',
                        'status': 'Paid',
                        'notes': 'COD payment received on delivery',
                    }
                )

                # =========================================
                # UPDATE EXISTING PAYMENT IF FOUND
                # =========================================
                if not created:

                    payment.customer_name = order.customer_name
                    payment.amount = order.total_amount
                    payment.payment_method = 'COD'
                    payment.status = 'Paid'
                    payment.notes = (
                        'COD payment received on delivery'
                    )

                    payment.save(
                        update_fields=[
                            'customer_name',
                            'amount',
                            'payment_method',
                            'status',
                            'notes',
                        ]
                    )

            else:

                order.save(
                    update_fields=[
                        'status',
                        'delivered_at'
                    ]
                )

            # =========================================
            # SYNC DELIVERY RECORD
            # =========================================
            Delivery.objects.filter(
                order=order
            ).update(
                status='Delivered'
            )

        return redirect(
            'view_order',
            id=order.id
        )

    return redirect(
        'order_list'
    )

 # =========================================
# SOFT DELETE ONLINE ORDER
# =========================================
def delete_order(request, id):

    # =========================================
    # POST REQUEST ONLY
    # =========================================
    if request.method == 'POST':

        order = Order.objects.get(
            id=id,
            is_deleted=False
        )

        # =========================================
        # SOFT DELETE ONLY
        # DO NOT CHANGE MEDICINE STOCK
        # =========================================
        order.is_deleted = True
        order.deleted_at = timezone.now()

        order.save(
            update_fields=[
                'is_deleted',
                'deleted_at'
            ]
        )

    return redirect(
        'order_list'
    )
    
# =========================================
# DELETED ONLINE ORDERS HISTORY
# =========================================
def deleted_order_history(request):

    deleted_orders = Order.objects.filter(
        is_deleted=True
    ).order_by('-deleted_at')

    context = {
        'deleted_orders': deleted_orders
    }

    return render(
        request,
       'store/online_orders/deleted_order_history.html',
        context
    )
    
    # =========================================
# RESTORE DELETED ONLINE ORDER
# =========================================
def restore_order(request, id):

    if request.method == 'POST':

        order = Order.objects.get(
            id=id,
            is_deleted=True
        )

        # =========================================
        # RESTORE HISTORY ONLY
        # DO NOT CHANGE MEDICINE STOCK
        # =========================================
        order.is_deleted = False
        order.deleted_at = None

        order.save(
            update_fields=[
                'is_deleted',
                'deleted_at'
            ]
        )

    return redirect(
        'deleted_order_history'
    )
    
    # =========================================
# PERMANENT DELETE ONLINE ORDER
# =========================================
def permanent_delete_order(request, id):

    if request.method == 'POST':

        order = Order.objects.get(
            id=id,
            is_deleted=True
        )

        # =========================================
        # HISTORY CLEANUP ONLY
        # DO NOT CHANGE MEDICINE STOCK
        # PAYMENT HISTORY WILL BE PRESERVED
        # =========================================

        order.delete()

    return redirect(
        'deleted_order_history'
    )

# =========================================
# ADD_MEDICINE
# =========================================

def add_medicine(request):

    if request.method == 'POST':

        medicine_id = request.POST.get('medicine_id') or None
        name = request.POST.get('name')
        generic_name = request.POST.get('generic_name') or ''
        brand = request.POST.get('brand') or ''
        category = request.POST.get('category') or ''
        manufacturer = request.POST.get('manufacturer')

        pack_size = request.POST.get('pack_size') or None
        unit = request.POST.get('unit') or ''

        hsn = request.POST.get('hsn') or ''
        gst = request.POST.get('gst') or None
        barcode = request.POST.get('barcode') or ''

        mrp = request.POST.get('mrp') or None
        purchase_rate = request.POST.get('purchase_rate') or None
        selling_rate = request.POST.get('selling_rate') or None

        prescription_required = (
            request.POST.get('prescription_required') == 'on'
        )

        schedule = request.POST.get('schedule') or ''

        stock = request.POST.get('stock') or 0
        low_stock_limit = request.POST.get('low_stock_limit') or 10

        expiry_date = request.POST.get('expiry_date')

        status = request.POST.get('status') or 'Active'
        description = request.POST.get('description') or ''

        Medicine.objects.create(
            medicine_id=medicine_id,
            name=name,
            generic_name=generic_name,
            brand=brand,
            category=category,
            manufacturer=manufacturer,
            pack_size=pack_size,
            unit=unit,
            hsn=hsn,
            gst=gst,
            mrp=mrp,
            purchase_rate=purchase_rate,
            selling_rate=selling_rate,
            prescription_required=prescription_required,
            schedule=schedule,
            barcode=barcode,
            stock=stock,
            low_stock_limit=low_stock_limit,
            expiry_date=expiry_date,
            status=status,
            description=description
        )

        return redirect('medicine_list')

    return render(
        request,
        'store/medicine_master/add_medicine.html'
    )


    
# =========================================
# INVENTORY
# =========================================
def inventory_list(request):
    medicines = Medicine.objects.filter(is_deleted=False)
    
    

    # =========================================
    # INVENTORY SEARCH
    # =========================================
    search_query = request.GET.get('search', '')

    if search_query:
        medicines = medicines.filter(
            Q(medicine_id__icontains=search_query) |
            Q(name__icontains=search_query) |
            Q(generic_name__icontains=search_query) |
            Q(brand__icontains=search_query)
        )

  
  
    # =========================================
    # INVENTORY CATEGORY FILTER
    # =========================================
    category_filter = request.GET.get('category', '')

    if category_filter:
        medicines = medicines.filter(category=category_filter)

    categories = Medicine.objects.filter(
        is_deleted=False
    ).exclude(
        category__isnull=True
    ).exclude(
        category=''
    ).values_list(
        'category',
        flat=True
    ).distinct() 
    
    
    # =========================================
    # INVENTORY STATUS FILTER
    # =========================================
    status_filter = request.GET.get('status', '')

    if status_filter:
        medicines = medicines.filter(
            status__iexact=status_filter
        )
    
    # =========================================
    # INVENTORY STOCK FILTER
    # =========================================
    stock_filter = request.GET.get('stock', '')

    if stock_filter == 'in':
        medicines = medicines.filter(
            stock__gt=F('low_stock_limit')
        )

    elif stock_filter == 'low':
        medicines = medicines.filter(
            stock__gt=0,
            stock__lte=F('low_stock_limit')
        )

    elif stock_filter == 'out':
        medicines = medicines.filter(
            stock=0
        )

    # =========================================
    # INVENTORY SUMMARY COUNTS
    # =========================================
    total_medicines = medicines.count()
    active_medicines = medicines.filter(status='Active').count()
    low_stock = medicines.filter(
        stock__lte=F('low_stock_limit')
    ).count()
    
    expiring_soon = medicines.filter(
        expiry_date__gte=date.today(),
        expiry_date__lte=date.today() + timedelta(days=30)
    ).count()

    return render(
        request,
        'store/inventory/inventory_list.html',
        {
            'medicines': medicines,
            'categories': categories,
            'total_medicines': total_medicines,
            'active_medicines': active_medicines,
            'low_stock': low_stock,
             'expiring_soon': expiring_soon
        }
    )



# =========================================
# VIEW PURCHASE
# =========================================
def view_purchase(request, id):

    # =========================================
    # GET PURCHASE
    # =========================================
    purchase = Purchase.objects.prefetch_related(
        'items__medicine'
    ).get(id=id)

    # =========================================
    # OPEN PURCHASE DETAILS PAGE
    # =========================================
    return render(
        request,
        'store/purchase/view_purchase.html',
        {
            'purchase': purchase
        }
    )


# =========================================
# PURCHASE LIST
# =========================================
def purchase_list(request):

    # =========================================
    # ALL PURCHASES
    # =========================================
    purchases = Purchase.objects.prefetch_related(
        'items__medicine'
    ).select_related(
        'supplier'
  ).order_by('-id')

    # =========================================
    # SEARCH
    # =========================================
    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    if search_query:
        purchases = purchases.filter(
            Q(purchase_id__icontains=search_query) |
            Q(invoice_number__icontains=search_query) |
            Q(supplier__name__icontains=search_query) |
            Q(items__medicine__name__icontains=search_query)
        ).distinct()

    # =========================================
    # STATUS FILTER
    # =========================================
    status_filter = request.GET.get(
        'status',
        ''
    ).strip()

    if status_filter:
        purchases = purchases.filter(
            status=status_filter
        )

    # =========================================
    # SEND DATA TO TEMPLATE
    # =========================================
    return render(
        request,
        'store/purchase/purchase_list.html',
        {
            'purchases': purchases,
            'search_query': search_query,
            'status_filter': status_filter
        }
    )


# =========================================
# ADD PURCHASE
# =========================================
def add_purchase(request):

    # =========================================
    # ACTIVE SUPPLIERS
    # =========================================
    suppliers = Supplier.objects.filter(
        is_deleted=False,
        status='Active'
    )

    # =========================================
    # ACTIVE MEDICINES
    # =========================================
    medicines = Medicine.objects.filter(
        is_deleted=False,
        status='Active'
    )

    # =========================================
    # FORM SUBMIT
    # =========================================
    if request.method == 'POST':

        # =========================================
        # SUPPLIER
        # =========================================
        supplier_id = request.POST.get('supplier')

        supplier = Supplier.objects.get(
            id=supplier_id
        )

        # =========================================
        # INVOICE NUMBER
        # =========================================
        invoice_number = request.POST.get(
            'invoice_number'
        )

        # =========================================
        # CHECK DUPLICATE INVOICE
        # =========================================
        if Purchase.objects.filter(
            supplier=supplier,
            invoice_number=invoice_number
        ).exists():

            return render(
                request,
                'store/purchase/add_purchase.html',
                {
                    'suppliers': suppliers,
                    'medicines': medicines,
                    'error_message':
                        'This invoice number already exists for the selected supplier.'
                }
            )

        # =========================================
        # GET ALL PURCHASE ITEMS
        # =========================================
        medicine_ids = request.POST.getlist(
            'medicine[]'
        )

        quantities = request.POST.getlist(
            'quantity[]'
        )

        purchase_rates = request.POST.getlist(
            'item_purchase_rate[]'
        )

        batch_numbers = request.POST.getlist(
            'batch_number[]'
        )

        expiry_dates = request.POST.getlist(
            'item_expiry_date[]'
        )

        # =========================================
        # CALCULATE TOTAL AMOUNT
        # =========================================
        total_amount = Decimal('0.00')

        for quantity, purchase_rate in zip(
            quantities,
            purchase_rates
        ):
            quantity_value = int(quantity)
            rate_value = Decimal(purchase_rate)

            total_amount += (
                quantity_value * rate_value
            )

        # =========================================
        # SAVE PURCHASE WITH TRANSACTION
        # =========================================
        with transaction.atomic():

            # =========================================
            # CREATE PURCHASE
            # =========================================
            purchase = Purchase.objects.create(
                supplier=supplier,
                invoice_number=invoice_number,
                purchase_date=request.POST.get(
                    'purchase_date'
                ),
                total_amount=total_amount,
                status='Pending',
                notes=request.POST.get(
                    'notes',
                    ''
                )
            )

            # =========================================
            # CREATE MULTIPLE PURCHASE ITEMS
            # =========================================
            for index, medicine_id in enumerate(
                medicine_ids
            ):

                medicine = Medicine.objects.get(
                    id=medicine_id
                )

                quantity_value = int(
                    quantities[index]
                )

                rate_value = Decimal(
                    purchase_rates[index]
                )

                batch_number = (
                    batch_numbers[index]
                    if index < len(batch_numbers)
                    else ''
                )

                expiry_date = (
                    expiry_dates[index]
                    if index < len(expiry_dates)
                    else ''
                )

                PurchaseItem.objects.create(
                    purchase=purchase,
                    medicine=medicine,
                    quantity=quantity_value,
                    purchase_rate=rate_value,
                    batch_number=batch_number,
                    expiry_date=expiry_date or None
                )

        # =========================================
        # PURCHASE SAVED
        # =========================================
        return redirect('purchase_list')

    # =========================================
    # OPEN ADD PURCHASE PAGE
    # =========================================
    return render(
        request,
        'store/purchase/add_purchase.html',
        {
            'suppliers': suppliers,
            'medicines': medicines
        }
    )     
# =========================================
# COMPLETE PURCHASE
# =========================================
def complete_purchase(request, id):

    # =========================================
    # COMPLETE ONLY ON POST
    # =========================================
    if request.method == 'POST':

        # =========================================
        # SAFE DATABASE TRANSACTION
        # =========================================
        with transaction.atomic():

            # =========================================
            # GET AND LOCK PURCHASE
            # =========================================
            purchase = Purchase.objects.select_for_update().get(
                id=id
            )

            # =========================================
            # PREVENT DOUBLE STOCK UPDATE
            # =========================================
            if (
                purchase.status == 'Pending'
                and not purchase.stock_updated
            ):

                # =========================================
                # UPDATE MEDICINE STOCK
                # =========================================
                for item in purchase.items.all():

                    Medicine.objects.filter(
                        id=item.medicine_id
                    ).update(
                        stock=F('stock') + item.quantity
                    )

                # =========================================
                # UPDATE PURCHASE STATUS
                # =========================================
                purchase.status = 'Completed'
                purchase.stock_updated = True

                purchase.save(
                    update_fields=[
                        'status',
                        'stock_updated'
                    ]
                )

        return redirect('purchase_list')

    return redirect('purchase_list')    

# =========================================
# CANCEL PURCHASE
# =========================================
def cancel_purchase(request, id):

    # =========================================
    # GET PURCHASE
    # =========================================
    purchase = Purchase.objects.get(id=id)

    # =========================================
    # CANCEL ONLY ON POST
    # =========================================
    if request.method == 'POST':
        
        
    

        # =========================================
        # ONLY PENDING PURCHASE CAN BE CANCELLED
        # =========================================
        if purchase.status == 'Pending':

            purchase.status = 'Cancelled'
            purchase.save()

        return redirect('purchase_list')

    return redirect('purchase_list')

# =========================================
# PRESCRIPTION LIST
# =========================================
def prescription_list(request):

    # =========================================
    # ALL PRESCRIPTIONS
    # =========================================
    prescriptions = Prescription.objects.all().order_by(
        '-id'
    )


    # =========================================
    # SEARCH
    # =========================================
    search = request.GET.get(
        'search',
        ''
    ).strip()

    if search:

        prescriptions = prescriptions.filter(

            Q(
                prescription_id__icontains=search
            )
            |
            Q(
                customer_name__icontains=search
            )
            |
            Q(
                phone__icontains=search
            )

        )


    # =========================================
    # STATUS FILTER
    # =========================================
    status = request.GET.get(
        'status',
        ''
    ).strip()

    if status:

        prescriptions = prescriptions.filter(
            status=status
        )



    # =========================================
    # PRESCRIPTION SUMMARY COUNTS
    # =========================================
    total_prescriptions = Prescription.objects.count()

    pending_prescriptions = Prescription.objects.filter(
        status='Pending'
    ).count()

    approved_prescriptions = Prescription.objects.filter(
        status='Approved'
    ).count()

    rejected_prescriptions = Prescription.objects.filter(
        status='Rejected'
    ).count()


       # =========================================
    # SEND DATA TO TEMPLATE
    # =========================================
    return render(
        request,
        'store/prescription/prescription_list.html',
        {
            'prescriptions': prescriptions,
            'search': search,
            'selected_status': status,

            # =========================================
            # SUMMARY COUNTS
            # =========================================
            'total_prescriptions': total_prescriptions,
            'pending_prescriptions': pending_prescriptions,
            'approved_prescriptions': approved_prescriptions,
            'rejected_prescriptions': rejected_prescriptions,
        }
    )



# =========================================
# ADD PRESCRIPTION
# =========================================
def add_prescription(request):

    # =========================================
    # FORM SUBMIT
    # =========================================
    if request.method == 'POST':

        Prescription.objects.create(
            customer_name=request.POST.get(
                'customer_name'
            ),
            phone=request.POST.get(
                'phone'
            ),
            prescription_image=request.FILES.get(
                'prescription_image'
            ),
            status='Pending',
            notes=request.POST.get(
                'notes',
                ''
            )
        )

        return redirect('prescription_list')

    # =========================================
    # OPEN PRESCRIPTION FORM
    # =========================================
    return render(
        request,
        'store/prescription/add_prescription.html'
    )


# =========================================
# VIEW PRESCRIPTION
# =========================================
def view_prescription(request, id):

    # =========================================
    # GET PRESCRIPTION
    # =========================================
    prescription = Prescription.objects.get(
        id=id
    )

    # =========================================
    # OPEN PRESCRIPTION DETAILS
    # =========================================
    return render(
        request,
        'store/prescription/view_prescription.html',
        {
            'prescription': prescription
        }
    )


# =========================================
# APPROVE PRESCRIPTION
# =========================================
def approve_prescription(request, id):

    # =========================================
    # APPROVE ONLY ON POST
    # =========================================
    if request.method == 'POST':

        # =========================================
        # GET PRESCRIPTION
        # =========================================
        prescription = Prescription.objects.get(
            id=id
        )

        # =========================================
        # UPDATE STATUS
        # =========================================
        if prescription.status == 'Pending':

            prescription.status = 'Approved'

            prescription.save(
                update_fields=[
                    'status'
                ]
            )

        # =========================================
        # BACK TO VIEW PAGE
        # =========================================
        return redirect(
            'view_prescription',
            id=prescription.id
        )

    return redirect(
        'prescription_list'
    )
    
    
 
 # =========================================
# REJECT PRESCRIPTION
# =========================================
def reject_prescription(request, id):

    # =========================================
    # REJECT ONLY ON POST
    # =========================================
    if request.method == 'POST':

        # =========================================
        # GET PRESCRIPTION
        # =========================================
        prescription = Prescription.objects.get(
            id=id
        )

        # =========================================
        # UPDATE STATUS
        # =========================================
        if prescription.status == 'Pending':

            prescription.status = 'Rejected'

            prescription.save(
                update_fields=[
                    'status'
                ]
            )

        # =========================================
        # BACK TO VIEW PAGE
        # =========================================
        return redirect(
            'view_prescription',
            id=prescription.id
        )

    return redirect(
        'prescription_list'
    )
    
    
    # =========================================
# MARK COD PAYMENT RECEIVED
# =========================================
def mark_payment_received(request, id):

    # =========================================
    # POST REQUEST ONLY
    # =========================================
    if request.method == 'POST':

        order = Order.objects.get(
            id=id
        )

        # =========================================
        # COD PAYMENT -> PAID
        # =========================================
        if (
            order.payment_method == 'COD'
            and order.status == 'Delivered'
            and order.payment_status == 'Pending'
        ):
            order.payment_status = 'Paid'

            order.save(
    update_fields=[
        'status',
        'delivered_at',
        'payment_status'
    ]
)

        return redirect(
            'view_order',
            id=order.id
        )

    return redirect(
        'order_list'
    )
    
    
    
# =========================================
# CANCEL ONLINE ORDER
# =========================================
def cancel_order(request, id):

    if request.method == 'POST':

        with transaction.atomic():

            order = Order.objects.select_for_update().get(
                id=id
            )

            # =========================================
            # ONLY PENDING / CONFIRMED / PACKED
            # =========================================
            if order.status in [
                'Pending',
                'Confirmed',
                'Packed'
            ]:

                # =========================================
                # RESTORE STOCK IF ALREADY DEDUCTED
                # =========================================
                if order.stock_updated:

                    for item in order.items.all():

                        Medicine.objects.filter(
                            id=item.medicine_id
                        ).update(
                            stock=F('stock') + item.quantity
                        )

                    order.stock_updated = False

                # =========================================
                # CANCEL ORDER
                # =========================================
                order.status = 'Cancelled'

                order.save(
                    update_fields=[
                        'status',
                        'stock_updated'
                    ]
                )

        return redirect(
            'view_order',
            id=order.id
        )

    return redirect(
        'order_list'
    )

#=============================================
# EDIT_MEDICINE
#=============================================
def edit_medicine(request, id):

    medicine = Medicine.objects.get(id=id)

    if request.method == 'POST':

        medicine.medicine_id = request.POST.get('medicine_id') or None
        medicine.name = request.POST.get('name')
        medicine.generic_name = request.POST.get('generic_name') or ''
        medicine.brand = request.POST.get('brand') or ''
        medicine.category = request.POST.get('category') or ''
        medicine.manufacturer = request.POST.get('manufacturer')

        medicine.pack_size = request.POST.get('pack_size') or None
        medicine.unit = request.POST.get('unit') or ''

        medicine.hsn = request.POST.get('hsn') or ''
        medicine.gst = request.POST.get('gst') or None
        medicine.barcode = request.POST.get('barcode') or ''

        medicine.mrp = request.POST.get('mrp') or None
        medicine.purchase_rate = request.POST.get('purchase_rate') or None
        medicine.selling_rate = request.POST.get('selling_rate') or None

        medicine.prescription_required = (
            request.POST.get('prescription_required') == 'on'
        )

        medicine.schedule = request.POST.get('schedule') or ''

        medicine.stock = request.POST.get('stock') or 0
        medicine.low_stock_limit = request.POST.get('low_stock_limit') or 10

        medicine.expiry_date = request.POST.get('expiry_date')

        medicine.status = request.POST.get('status') or 'Active'
        medicine.description = request.POST.get('description') or ''

        medicine.save()

        return redirect('medicine_list')

    return render(
        request,
        'store/medicine_master/edit_medicine.html',
        {
            'medicine': medicine
        }
    )
    

   # =========================================
   # VIEW MEDICINE
   # =========================================

def view_medicine(request, id):

    medicine = Medicine.objects.get(id=id)

    return render(
        request,
        'store/medicine_master/view_medicine.html',
        {
            'medicine': medicine
        }
    )
    
       
#
# =========================================
# DELETE MEDICINE - SOFT DELETE
# =========================================

def delete_medicine(request, id):
    medicine = Medicine.objects.get(id=id)

    if request.method == 'POST':
        medicine.is_deleted = True
        medicine.save()

        request.session['deleted_medicine_id'] = medicine.id
        request.session.modified = True

        return redirect('medicine_list')

    return render(
        request,
        'store/medicine_master/delete_medicine.html',
        {'medicine': medicine}
    )


# =========================================
# RESTORE / UNDO DELETED MEDICINE
# =========================================

def restore_medicine(request, id):
    medicine = Medicine.objects.get(id=id)

    medicine.is_deleted = False
    medicine.save()

    request.session.pop('deleted_medicine_id', None)

    return redirect('medicine_list')


# =========================================
# DELETED MEDICINES / TRASH
# =========================================

def deleted_medicines(request):
    medicines = Medicine.objects.filter(is_deleted=True)

    return render(
        request,
        'store/medicine_master/deleted_medicines.html',
        {'medicines': medicines}
    )
    
    
    
  # =========================================
# DELIVERY MANAGEMENT LIST
# =========================================
def delivery_list(request):

    # =========================================
    # GET ALL DELIVERY RECORDS
    # =========================================
    deliveries = (
        Delivery.objects
        .select_related('order')
        .order_by('-assigned_at')
    )

    # =========================================
    # DELIVERY SUMMARY COUNTS
    # =========================================
    total_deliveries = Delivery.objects.count()

    assigned_count = Delivery.objects.filter(
        status='Assigned'
    ).count()

    out_for_delivery_count = Delivery.objects.filter(
        status='Out for Delivery'
    ).count()

    delivered_count = Delivery.objects.filter(
        status='Delivered'
    ).count()

    # =========================================
    # SEND DATA TO DELIVERY PAGE
    # =========================================
    context = {
        'deliveries': deliveries,
        'total_deliveries': total_deliveries,
        'assigned_count': assigned_count,
        'out_for_delivery_count': out_for_delivery_count,
        'delivered_count': delivered_count,
    }

    return render(
        request,
        'store/delivery/delivery_list.html',
        context
    )
    
    # =========================================
# ASSIGN DELIVERY
# =========================================
def assign_delivery(request, order_id):

    # =========================================
    # GET SHIPPED ORDER
    # =========================================
    try:
        order = Order.objects.get(
            id=order_id,
            status='Shipped'
        )

    except Order.DoesNotExist:
        return redirect('order_list')


    # =========================================
    # PREVENT DUPLICATE DELIVERY
    # =========================================
    if Delivery.objects.filter(
        order=order
    ).exists():

        return redirect('delivery_list')


    # =========================================
    # SAVE DELIVERY ASSIGNMENT
    # =========================================
    if request.method == 'POST':

        delivery_person_name = request.POST.get(
            'delivery_person_name',
            ''
        ).strip()

        delivery_person_phone = request.POST.get(
            'delivery_person_phone',
            ''
        ).strip()

        notes = request.POST.get(
            'notes',
            ''
        ).strip()


        # =========================================
        # REQUIRED FIELD CHECK
        # =========================================
        if (
            delivery_person_name and
            delivery_person_phone
        ):

            Delivery.objects.create(
                order=order,
                delivery_person_name=delivery_person_name,
                delivery_person_phone=delivery_person_phone,
                status='Assigned',
                notes=notes
            )

            return redirect(
                'delivery_list'
            )


    # =========================================
    # SHOW ASSIGN DELIVERY FORM
    # =========================================
    context = {
        'order': order
    }

    return render(
        request,
        'store/delivery/assign_delivery.html',
        context
    )
    
# =========================================
# DELIVERY -> OUT FOR DELIVERY
# =========================================
def delivery_out_for_delivery(request, id):

    # =========================================
    # POST REQUEST ONLY
    # =========================================
    if request.method == 'POST':

        delivery = Delivery.objects.select_related(
            'order'
        ).get(id=id)

        # =========================================
        # ASSIGNED -> OUT FOR DELIVERY
        # =========================================
        if delivery.status == 'Assigned':

            order = delivery.order

            # UPDATE DELIVERY STATUS
            delivery.status = 'Out for Delivery'

            delivery.save(
                update_fields=[
                    'status'
                ]
            )

            # UPDATE ONLINE ORDER STATUS
            order.status = 'Out for Delivery'
            order.out_for_delivery_at = timezone.now()

            order.save(
                update_fields=[
                    'status',
                    'out_for_delivery_at'
                ]
            )

        return redirect(
            'delivery_list'
        )

    return redirect(
        'delivery_list'
    )
    
# =========================================
# DELIVERY -> DELIVERED
# =========================================
def delivery_delivered(request, id):

    # =========================================
    # POST REQUEST ONLY
    # =========================================
    if request.method == 'POST':

        delivery = Delivery.objects.select_related(
            'order'
        ).get(id=id)

        # =========================================
        # OUT FOR DELIVERY -> DELIVERED
        # =========================================
        if delivery.status == 'Out for Delivery':

            order = delivery.order

            # =========================================
            # UPDATE DELIVERY STATUS
            # =========================================
            delivery.status = 'Delivered'

            delivery.save(
                update_fields=[
                    'status'
                ]
            )

            # =========================================
            # UPDATE ONLINE ORDER
            # =========================================
            order.status = 'Delivered'
            order.delivered_at = timezone.now()

            # =========================================
            # COD PAYMENT RECEIVED
            # =========================================
            if order.payment_method == 'COD':

                order.payment_status = 'Paid'

                order.save(
                    update_fields=[
                        'status',
                        'delivered_at',
                        'payment_status'
                    ]
                )

                # =========================================
                # CREATE / UPDATE PAYMENT RECORD
                # =========================================
                payment, created = Payment.objects.get_or_create(
                    source='Online Order',
                    reference_id=order.order_id,
                    defaults={
                        'customer_name': order.customer_name,
                        'amount': order.total_amount,
                        'payment_method': 'COD',
                        'status': 'Paid',
                        'notes': 'COD payment received on delivery',
                    }
                )

                # =========================================
                # IF PAYMENT ALREADY EXISTS
                # UPDATE IT INSTEAD OF DUPLICATING
                # =========================================
                if not created:

                    payment.customer_name = order.customer_name
                    payment.amount = order.total_amount
                    payment.payment_method = 'COD'
                    payment.status = 'Paid'
                    payment.notes = (
                        'COD payment received on delivery'
                    )

                    payment.save(
                        update_fields=[
                            'customer_name',
                            'amount',
                            'payment_method',
                            'status',
                            'notes',
                        ]
                    )

            else:

                order.save(
                    update_fields=[
                        'status',
                        'delivered_at'
                    ]
                )

        return redirect(
            'delivery_list'
        )

    return redirect(
        'delivery_list'
    )
    
    
    # =========================================
# VIEW DELIVERY DETAILS
# =========================================
def view_delivery(request, id):

    # =========================================
    # GET DELIVERY WITH ORDER
    # =========================================
    delivery = Delivery.objects.select_related(
        'order'
    ).get(
        id=id
    )

    # =========================================
    # SEND DATA TO DETAIL PAGE
    # =========================================
    context = {
        'delivery': delivery
    }

    return render(
        request,
        'store/delivery/view_delivery.html',
        context
    )
    
  # =========================================
# PAYMENT MANAGEMENT LIST
# =========================================
def payment_list(request):

    # =========================================
    # GET SEARCH / FILTER VALUES
    # =========================================
    search = request.GET.get(
        'search',
        ''
    ).strip()

    source = request.GET.get(
        'source',
        ''
    ).strip()

    status = request.GET.get(
        'status',
        ''
    ).strip()

    payment_method = request.GET.get(
        'payment_method',
        ''
    ).strip()


    # =========================================
    # GET PAYMENTS
    # =========================================
    payments = Payment.objects.all()


    # =========================================
    # SEARCH
    # =========================================
    if search:

        payments = payments.filter(
            Q(payment_id__icontains=search) |
            Q(reference_id__icontains=search) |
            Q(customer_name__icontains=search)
        )


    # =========================================
    # SOURCE FILTER
    # =========================================
    if source:

        payments = payments.filter(
            source=source
        )


    # =========================================
    # STATUS FILTER
    # =========================================
    if status:

        payments = payments.filter(
            status=status
        )


    # =========================================
    # PAYMENT METHOD FILTER
    # =========================================
    if payment_method:

        payments = payments.filter(
            payment_method=payment_method
        )


    # =========================================
    # LATEST PAYMENT FIRST
    # =========================================
    payments = payments.order_by(
        '-payment_date'
    )


    # =========================================
    # PAYMENT SUMMARY
    # =========================================
    total_payments = Payment.objects.count()

    paid_count = Payment.objects.filter(
        status='Paid'
    ).count()

    pending_count = Payment.objects.filter(
        status='Pending'
    ).count()

    failed_count = Payment.objects.filter(
        status='Failed'
    ).count()

    total_received = Payment.objects.filter(
        status='Paid'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0


    # =========================================
    # TEMPLATE DATA
    # =========================================
    context = {
        'payments': payments,

        'total_payments': total_payments,
        'paid_count': paid_count,
        'pending_count': pending_count,
        'failed_count': failed_count,
        'total_received': total_received,

        'search': search,
        'selected_source': source,
        'selected_status': status,
        'selected_payment_method': payment_method,
    }


    return render(
        request,
        'store/payment/payment_list.html',
        context
    )
    
# =========================================
# VIEW PAYMENT DETAILS
# =========================================
def view_payment(request, id):

    payment = Payment.objects.get(
        id=id
    )

    context = {
        'payment': payment
    }

    return render(
        request,
        'store/payment/view_payment.html',
        context
    )
    
# =========================================
# WALK-IN POS
# =========================================
def walk_in_pos(request):

    # =========================================
    # GET AVAILABLE ACTIVE MEDICINES
    # =========================================
    medicines = Medicine.objects.filter(
        status='Active',
        stock__gt=0
    ).order_by('name')


    # =========================================
    # HANDLE COMPLETE SALE
    # =========================================
    if request.method == 'POST':

        customer_name = request.POST.get(
            'customer_name',
            ''
        ).strip()

        customer_phone = request.POST.get(
            'customer_phone',
            ''
        ).strip()

        payment_method = request.POST.get(
            'payment_method',
            'Cash'
        )

        discount_value = request.POST.get(
            'discount',
            '0'
        )

        sale_items_json = request.POST.get(
            'sale_items',
            ''
        )


        # =========================================
        # VALIDATE PAYMENT METHOD
        # =========================================
        if payment_method not in [
            'Cash',
            'UPI',
            'Card'
        ]:

            context = {
                'medicines': medicines,
                'error': 'Invalid payment method.'
            }

            return render(
                request,
                'store/walk_in_pos/pos.html',
                context
            )


        try:

            # =========================================
            # CONVERT DISCOUNT
            # =========================================
            discount = Decimal(
                discount_value or '0'
            )

            if discount < 0:
                discount = Decimal('0.00')


            # =========================================
            # READ SALE ITEMS
            # =========================================
            sale_items = json.loads(
                sale_items_json
            )

            if not isinstance(
                sale_items,
                list
            ) or not sale_items:

                raise ValueError(
                    'No medicines added to sale.'
                )


            # =========================================
            # DATABASE TRANSACTION
            # =========================================
            with transaction.atomic():

                subtotal = Decimal('0.00')

                prepared_items = []


                # =========================================
                # VALIDATE ALL MEDICINES
                # =========================================
                for item in sale_items:

                    medicine_id = int(
                        item.get('medicine_id')
                    )

                    quantity = int(
                        item.get('quantity')
                    )


                    if quantity <= 0:

                        raise ValueError(
                            'Invalid medicine quantity.'
                        )


                    # =========================================
                    # LOCK + GET CURRENT MEDICINE
                    # =========================================
                    medicine = (
                        Medicine.objects
                        .select_for_update()
                        .get(
                            id=medicine_id,
                            status='Active'
                        )
                    )


                    # =========================================
                    # CHECK CURRENT STOCK
                    # =========================================
                    if medicine.stock < quantity:

                        raise ValueError(
                            f'Insufficient stock for '
                            f'{medicine.name}. '
                            f'Available: {medicine.stock}'
                        )


                    # =========================================
                    # GET CURRENT SELLING RATE
                    # =========================================
                    selling_rate = (
                        medicine.selling_rate
                        or Decimal('0.00')
                    )


                    if selling_rate <= 0:

                        raise ValueError(
                            f'Selling rate is not set '
                            f'for {medicine.name}.'
                        )


                    # =========================================
                    # CALCULATE LINE TOTAL
                    # =========================================
                    line_total = (
                        selling_rate *
                        quantity
                    )

                    subtotal += line_total


                    prepared_items.append({
                        'medicine': medicine,
                        'quantity': quantity,
                        'selling_rate': selling_rate,
                        'line_total': line_total,
                    })


                # =========================================
                # VALIDATE DISCOUNT
                # =========================================
                if discount > subtotal:

                    discount = subtotal


                # =========================================
                # GRAND TOTAL
                # =========================================
                total_amount = (
                    subtotal -
                    discount
                )


                # =========================================
                # CREATE SALE
                # =========================================
                sale = Sale.objects.create(
                    customer_name=(
                        customer_name
                        or 'Walk-in Customer'
                    ),
                    customer_phone=(
                        customer_phone
                        or None
                    ),
                    payment_method=payment_method,
                    subtotal=subtotal,
                    discount=discount,
                    total_amount=total_amount
                )


                # =========================================
                # CREATE ITEMS + DEDUCT STOCK
                # =========================================
                for prepared_item in prepared_items:

                    medicine = prepared_item[
                        'medicine'
                    ]

                    quantity = prepared_item[
                        'quantity'
                    ]


                    SaleItem.objects.create(
                        sale=sale,
                        medicine=medicine,
                        quantity=quantity,
                        selling_rate=prepared_item[
                            'selling_rate'
                        ],
                        line_total=prepared_item[
                            'line_total'
                        ]
                    )


                    medicine.stock -= quantity

                    medicine.save(
                        update_fields=['stock']
                    )


                # =========================================
                # CREATE PAYMENT RECORD
                # WALK-IN POS PAYMENT IS ALREADY RECEIVED
                # =========================================
                Payment.objects.create(
                    source='Walk-in POS',
                    reference_id=sale.sale_id,
                    customer_name=(
                        sale.customer_name
                        or 'Walk-in Customer'
                    ),
                    amount=sale.total_amount,
                    payment_method=sale.payment_method,
                    status='Paid',
                    notes='Walk-in POS payment'
                )


            # =========================================
            # SALE SUCCESS → INVOICE
            # =========================================
            return redirect(
                'sale_invoice',
                sale_id=sale.id
            )

        except (
            ValueError,
            TypeError,
            json.JSONDecodeError,
            Medicine.DoesNotExist
        ) as error:

            context = {
                'medicines': medicines,
                'error': str(error)
            }

            return render(
                request,
                'store/walk_in_pos/pos.html',
                context
            )


    # =========================================
    # NORMAL POS PAGE
    # =========================================
    context = {
        'medicines': medicines
    }

    return render(
        request,
        'store/walk_in_pos/pos.html',
        context
    )
    
# =========================================
# WALK-IN POS SALE INVOICE
# =========================================
def sale_invoice(request, sale_id):

    sale = Sale.objects.prefetch_related(
        'items__medicine'
    ).get(
        id=sale_id
    )

    context = {
        'sale': sale
    }

    return render(
        request,
        'store/walk_in_pos/sale_invoice.html',
        context
    )
    
# =========================================
# SALES & INVOICE HISTORY
# =========================================
def sales_list(request):

    # =========================================
    # GET ACTIVE WALK-IN SALES
    # =========================================
    sales = (
        Sale.objects
        .filter(is_deleted=False)
        .prefetch_related('items__medicine')
        .order_by('-sale_date')
    )

    # =========================================
    # SEND SALES TO HISTORY PAGE
    # =========================================
    context = {
        'sales': sales
    }

    return render(
        request,
        'store/sales_invoice/sales_list.html',
        context
    )


# =========================================
# SOFT DELETE WALK-IN SALE HISTORY
# =========================================
def delete_sale(request, sale_id):

    if request.method == 'POST':

        try:
            sale = Sale.objects.get(
                id=sale_id,
                is_deleted=False
            )

            # Move sale to Deleted History
            sale.is_deleted = True
            sale.deleted_at = timezone.now()

            sale.save(
                update_fields=[
                    'is_deleted',
                    'deleted_at'
                ]
            )

        except Sale.DoesNotExist:
            pass

    return redirect('sales_list')

# =========================================
# DELETED SALES HISTORY
# =========================================
def deleted_sales_list(request):

    # =========================================
    # GET DELETED WALK-IN SALES
    # =========================================
    deleted_sales = (
        Sale.objects
        .filter(is_deleted=True)
        .prefetch_related('items__medicine')
        .order_by('-deleted_at')
    )

    context = {
        'deleted_sales': deleted_sales
    }

    return render(
        request,
        'store/sales_invoice/deleted_sales.html',
        context
    )
    
# =========================================
# RESTORE DELETED WALK-IN SALE
# =========================================
def restore_sale(request, sale_id):

    if request.method == 'POST':

        try:
            sale = Sale.objects.get(
                id=sale_id,
                is_deleted=True
            )

            # Restore only the sale history.
            # Medicine stock must NOT change.
            sale.is_deleted = False
            sale.deleted_at = None

            sale.save(
                update_fields=[
                    'is_deleted',
                    'deleted_at'
                ]
            )

        except Sale.DoesNotExist:
            pass

    return redirect('deleted_sales_list')

# =========================================
# PERMANENTLY DELETE WALK-IN SALE
# =========================================
def permanently_delete_sale(request, sale_id):

    if request.method == 'POST':

        try:
            sale = Sale.objects.get(
                id=sale_id,
                is_deleted=True
            )

            # Permanently remove sale history.
            # Medicine stock must NOT change.
            sale.delete()

        except Sale.DoesNotExist:
            pass

    return redirect('deleted_sales_list')


# =========================================
# AUTO CLEANUP DELETED SALES AFTER 30 DAYS
# =========================================
def cleanup_old_deleted_sales():

    # Date/time before which deleted records
    # are older than 30 days
    thirty_days_ago = (
        timezone.now() -
        timedelta(days=30)
    )

    # Get only sales that are already
    # inside Deleted History for 30+ days
    old_deleted_sales = Sale.objects.filter(
        is_deleted=True,
        deleted_at__lte=thirty_days_ago
    )

    # Permanently delete old history.
    # Medicine stock is NOT changed.
    old_deleted_sales.delete()
    
# =========================================
# REPORTS DASHBOARD
# =========================================
def report_dashboard(request):

    return render(
        request,
        'store/reports/report_dashboard.html'
    )
    
# =========================================
# SALES REPORT
# =========================================
def sales_report(request):

    # =========================================
    # ACTIVE SALES ONLY
    # =========================================
    sales = Sale.objects.filter(
        is_deleted=False
    ).order_by('-sale_date')


    # =========================================
    # GET FILTER VALUES
    # =========================================
    filter_type = request.GET.get(
        'filter',
        ''
    )

    start_date = request.GET.get(
        'start_date',
        ''
    )

    end_date = request.GET.get(
        'end_date',
        ''
    )


    # =========================================
    # TODAY FILTER
    # =========================================
    if filter_type == 'today':

        today = timezone.localdate()

        start_datetime = timezone.make_aware(
            timezone.datetime.combine(
                today,
                timezone.datetime.min.time()
            )
        )

        end_datetime = timezone.make_aware(
            timezone.datetime.combine(
                today,
                timezone.datetime.max.time()
            )
        )

        sales = sales.filter(
            sale_date__gte=start_datetime,
            sale_date__lte=end_datetime
        )


    # =========================================
    # THIS MONTH FILTER
    # =========================================
    elif filter_type == 'month':

        today = timezone.localdate()

        month_start = today.replace(
            day=1
        )

        if today.month == 12:
            next_month = date(
                today.year + 1,
                1,
                1
            )
        else:
            next_month = date(
                today.year,
                today.month + 1,
                1
            )

        start_datetime = timezone.make_aware(
            timezone.datetime.combine(
                month_start,
                timezone.datetime.min.time()
            )
        )

        end_datetime = timezone.make_aware(
            timezone.datetime.combine(
                next_month,
                timezone.datetime.min.time()
            )
        )

        sales = sales.filter(
            sale_date__gte=start_datetime,
            sale_date__lt=end_datetime
        )


    # =========================================
    # CUSTOM DATE RANGE FILTER
    # =========================================
    elif filter_type == 'custom':

        if start_date:

            start_date_obj = date.fromisoformat(
                start_date
            )

            start_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    start_date_obj,
                    timezone.datetime.min.time()
                )
            )

            sales = sales.filter(
                sale_date__gte=start_datetime
            )


        if end_date:

            end_date_obj = date.fromisoformat(
                end_date
            )

            next_day = (
                end_date_obj +
                timedelta(days=1)
            )

            end_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    next_day,
                    timezone.datetime.min.time()
                )
            )

            sales = sales.filter(
                sale_date__lt=end_datetime
            )


    # =========================================
    # REPORT SUMMARY
    # =========================================
    total_sales = sales.count()

    total_revenue = (
        sales.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
    )

    total_discount = (
        sales.aggregate(
            total=Sum('discount')
        )['total'] or 0
    )


    # =========================================
    # CONTEXT
    # =========================================
    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'total_discount': total_discount,
        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
    }


    return render(
        request,
        'store/reports/sales_report.html',
        context
    )
# =========================================
# ONLINE ORDERS REPORT
# =========================================
def online_orders_report(request):

    # =========================================
    # ACTIVE ORDERS ONLY
    # =========================================
    orders = Order.objects.filter(
        is_deleted=False
    ).order_by('-order_date')


    # =========================================
    # GET FILTER VALUES
    # =========================================
    filter_type = request.GET.get(
        'filter',
        ''
    )

    start_date = request.GET.get(
        'start_date',
        ''
    )

    end_date = request.GET.get(
        'end_date',
        ''
    )


    # =========================================
    # TODAY FILTER
    # =========================================
    if filter_type == 'today':

        today = timezone.localdate()

        start_datetime = timezone.make_aware(
            timezone.datetime.combine(
                today,
                timezone.datetime.min.time()
            )
        )

        end_datetime = timezone.make_aware(
            timezone.datetime.combine(
                today,
                timezone.datetime.max.time()
            )
        )

        orders = orders.filter(
            order_date__gte=start_datetime,
            order_date__lte=end_datetime
        )


    # =========================================
    # THIS MONTH FILTER
    # =========================================
    elif filter_type == 'month':

        today = timezone.localdate()

        month_start = today.replace(
            day=1
        )

        if today.month == 12:

            next_month = date(
                today.year + 1,
                1,
                1
            )

        else:

            next_month = date(
                today.year,
                today.month + 1,
                1
            )


        start_datetime = timezone.make_aware(
            timezone.datetime.combine(
                month_start,
                timezone.datetime.min.time()
            )
        )

        end_datetime = timezone.make_aware(
            timezone.datetime.combine(
                next_month,
                timezone.datetime.min.time()
            )
        )

        orders = orders.filter(
            order_date__gte=start_datetime,
            order_date__lt=end_datetime
        )


    # =========================================
    # CUSTOM DATE RANGE FILTER
    # =========================================
    elif filter_type == 'custom':

        if start_date:

            start_date_obj = date.fromisoformat(
                start_date
            )

            start_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    start_date_obj,
                    timezone.datetime.min.time()
                )
            )

            orders = orders.filter(
                order_date__gte=start_datetime
            )


        if end_date:

            end_date_obj = date.fromisoformat(
                end_date
            )

            next_day = (
                end_date_obj +
                timedelta(days=1)
            )

            end_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    next_day,
                    timezone.datetime.min.time()
                )
            )

            orders = orders.filter(
                order_date__lt=end_datetime
            )


    # =========================================
    # REPORT SUMMARY
    # =========================================
    total_orders = orders.count()

    total_order_value = (
        orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
    )

    delivered_orders = orders.filter(
        status='Delivered'
    ).count()

    pending_orders = orders.filter(
        status='Pending'
    ).count()

    cancelled_orders = orders.filter(
        status='Cancelled'
    ).count()


    # =========================================
    # CONTEXT
    # =========================================
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_order_value': total_order_value,
        'delivered_orders': delivered_orders,
        'pending_orders': pending_orders,
        'cancelled_orders': cancelled_orders,

        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
    }


    return render(
        request,
        'store/reports/online_orders_report.html',
        context
    )
    
# =========================================
# PURCHASE REPORT
# =========================================
def purchase_report(request):

    # =========================================
    # ALL PURCHASES
    # =========================================
    purchases = Purchase.objects.all().order_by(
        '-purchase_date',
        '-id'
    )


    # =========================================
    # GET FILTER VALUES
    # =========================================
    filter_type = request.GET.get(
        'filter',
        ''
    )

    start_date = request.GET.get(
        'start_date',
        ''
    )

    end_date = request.GET.get(
        'end_date',
        ''
    )


    # =========================================
    # TODAY FILTER
    # =========================================
    if filter_type == 'today':

        today = timezone.localdate()

        purchases = purchases.filter(
            purchase_date=today
        )


    # =========================================
    # THIS MONTH FILTER
    # =========================================
    elif filter_type == 'month':

        today = timezone.localdate()

        purchases = purchases.filter(
            purchase_date__year=today.year,
            purchase_date__month=today.month
        )


    # =========================================
    # CUSTOM DATE RANGE FILTER
    # =========================================
    elif filter_type == 'custom':

        if start_date:

            start_date_obj = date.fromisoformat(
                start_date
            )

            purchases = purchases.filter(
                purchase_date__gte=start_date_obj
            )


        if end_date:

            end_date_obj = date.fromisoformat(
                end_date
            )

            purchases = purchases.filter(
                purchase_date__lte=end_date_obj
            )


    # =========================================
    # REPORT SUMMARY
    # =========================================
    total_purchases = purchases.count()

    total_purchase_value = (
        purchases.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
    )

    completed_purchases = purchases.filter(
        status='Completed'
    ).count()

    pending_purchases = purchases.filter(
        status='Pending'
    ).count()

    cancelled_purchases = purchases.filter(
        status='Cancelled'
    ).count()


    # =========================================
    # CONTEXT
    # =========================================
    context = {
        'purchases': purchases,
        'total_purchases': total_purchases,
        'total_purchase_value': total_purchase_value,
        'completed_purchases': completed_purchases,
        'pending_purchases': pending_purchases,
        'cancelled_purchases': cancelled_purchases,

        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,
    }


    return render(
        request,
        'store/reports/purchase_report.html',
        context
    )
    
# =========================================
# PAYMENT REPORT
# =========================================
def payment_report(request):

    # =========================================
    # ALL PAYMENTS
    # =========================================
    payments = Payment.objects.all().order_by(
        '-payment_date',
        '-id'
    )


    # =========================================
    # GET FILTER VALUES
    # =========================================
    filter_type = request.GET.get(
        'filter',
        ''
    )

    start_date = request.GET.get(
        'start_date',
        ''
    )

    end_date = request.GET.get(
        'end_date',
        ''
    )

    status_filter = request.GET.get(
        'status',
        ''
    )

    method_filter = request.GET.get(
        'payment_method',
        ''
    )


    # =========================================
    # TODAY FILTER
    # =========================================
    if filter_type == 'today':

        today = timezone.localdate()

        start_datetime = timezone.make_aware(
            timezone.datetime.combine(
                today,
                timezone.datetime.min.time()
            )
        )

        end_datetime = timezone.make_aware(
            timezone.datetime.combine(
                today,
                timezone.datetime.max.time()
            )
        )

        payments = payments.filter(
            payment_date__gte=start_datetime,
            payment_date__lte=end_datetime
        )


    # =========================================
    # THIS MONTH FILTER
    # =========================================
    elif filter_type == 'month':

        today = timezone.localdate()

        month_start = today.replace(
            day=1
        )

        if today.month == 12:

            next_month = date(
                today.year + 1,
                1,
                1
            )

        else:

            next_month = date(
                today.year,
                today.month + 1,
                1
            )

        start_datetime = timezone.make_aware(
            timezone.datetime.combine(
                month_start,
                timezone.datetime.min.time()
            )
        )

        end_datetime = timezone.make_aware(
            timezone.datetime.combine(
                next_month,
                timezone.datetime.min.time()
            )
        )

        payments = payments.filter(
            payment_date__gte=start_datetime,
            payment_date__lt=end_datetime
        )


    # =========================================
    # CUSTOM DATE RANGE FILTER
    # =========================================
    elif filter_type == 'custom':

        if start_date:

            start_date_obj = date.fromisoformat(
                start_date
            )

            start_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    start_date_obj,
                    timezone.datetime.min.time()
                )
            )

            payments = payments.filter(
                payment_date__gte=start_datetime
            )


        if end_date:

            end_date_obj = date.fromisoformat(
                end_date
            )

            next_day = (
                end_date_obj +
                timedelta(days=1)
            )

            end_datetime = timezone.make_aware(
                timezone.datetime.combine(
                    next_day,
                    timezone.datetime.min.time()
                )
            )

            payments = payments.filter(
                payment_date__lt=end_datetime
            )


    # =========================================
    # PAYMENT STATUS FILTER
    # =========================================
    if status_filter:

        payments = payments.filter(
            status=status_filter
        )


    # =========================================
    # PAYMENT METHOD FILTER
    # =========================================
    if method_filter:

        payments = payments.filter(
            payment_method=method_filter
        )


    # =========================================
    # REPORT SUMMARY
    # =========================================
    total_payments = payments.count()

    total_amount = (
        payments.aggregate(
            total=Sum('amount')
        )['total'] or 0
    )

    paid_payments = payments.filter(
        status='Paid'
    ).count()

    pending_payments = payments.filter(
        status='Pending'
    ).count()

    failed_payments = payments.filter(
        status='Failed'
    ).count()

    refunded_payments = payments.filter(
        status='Refunded'
    ).count()


    # =========================================
    # TOTAL RECEIVED
    # Only Paid payments
    # =========================================
    total_received = (
        payments.filter(
            status='Paid'
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0
    )


    # =========================================
    # CONTEXT
    # =========================================
    context = {
        'payments': payments,

        'total_payments': total_payments,
        'total_amount': total_amount,
        'total_received': total_received,

        'paid_payments': paid_payments,
        'pending_payments': pending_payments,
        'failed_payments': failed_payments,
        'refunded_payments': refunded_payments,

        'filter_type': filter_type,
        'start_date': start_date,
        'end_date': end_date,

        'status_filter': status_filter,
        'method_filter': method_filter,
    }


    return render(
        request,
        'store/reports/payment_report.html',
        context
    )


# =========================================
# INVENTORY REPORT
# =========================================
def inventory_report(request):

    # =========================================
    # ACTIVE / NON-DELETED MEDICINE RECORDS
    # =========================================
    medicines = Medicine.objects.filter(
        is_deleted=False
    ).order_by(
        'name'
    )


    # =========================================
    # GET FILTER VALUES
    # =========================================
    stock_filter = request.GET.get(
        'stock',
        ''
    )

    status_filter = request.GET.get(
        'status',
        ''
    )

    search_query = request.GET.get(
        'search',
        ''
    ).strip()


    # =========================================
    # SEARCH FILTER
    # =========================================
    if search_query:

        medicines = medicines.filter(

            Q(
                medicine_id__icontains=search_query
            )

            |

            Q(
                name__icontains=search_query
            )

            |

            Q(
                generic_name__icontains=search_query
            )

            |

            Q(
                brand__icontains=search_query
            )

            |

            Q(
                category__icontains=search_query
            )

            |

            Q(
                manufacturer__icontains=search_query
            )

        )


    # =========================================
    # MEDICINE STATUS FILTER
    # =========================================
    if status_filter:

        medicines = medicines.filter(
            status=status_filter
        )


    # =========================================
    # STOCK FILTER
    # =========================================
    if stock_filter == 'out':

        medicines = medicines.filter(
            stock=0
        )


    elif stock_filter == 'low':

        medicines = medicines.filter(
            stock__gt=0,
            stock__lte=F('low_stock_limit')
        )


    elif stock_filter == 'available':

        medicines = medicines.filter(
            stock__gt=F('low_stock_limit')
        )


    # =========================================
    # REPORT SUMMARY
    # =========================================
    total_medicines = medicines.count()

    total_stock = (
        medicines.aggregate(
            total=Sum('stock')
        )['total'] or 0
    )

    active_medicines = medicines.filter(
        status='Active'
    ).count()

    low_stock_medicines = medicines.filter(
        stock__gt=0,
        stock__lte=F('low_stock_limit')
    ).count()

    out_of_stock_medicines = medicines.filter(
        stock=0
    ).count()


    # =========================================
    # CONTEXT
    # =========================================
    context = {
        'medicines': medicines,

        'total_medicines': total_medicines,
        'total_stock': total_stock,
        'active_medicines': active_medicines,
        'low_stock_medicines': low_stock_medicines,
        'out_of_stock_medicines': out_of_stock_medicines,

        'stock_filter': stock_filter,
        'status_filter': status_filter,
        'search_query': search_query,
    }


    return render(
        request,
        'store/reports/inventory_report.html',
        context
    )

# =========================================
# EXPIRY REPORT
# =========================================
def expiry_report(request):

    # =========================================
    # DATE VALUES
    # =========================================
    today = timezone.localdate()

    expiring_soon_date = (
        today + timedelta(days=30)
    )


    # =========================================
    # ALL NON-DELETED MEDICINES
    # =========================================
    medicines = Medicine.objects.filter(
    is_deleted=False
).order_by(
    'expiry_date',
    'name'
)


    # =========================================
    # GET FILTER VALUES
    # =========================================
    expiry_filter = request.GET.get(
        'expiry',
        ''
    )

    status_filter = request.GET.get(
        'status',
        ''
    )

    search_query = request.GET.get(
        'search',
        ''
    ).strip()


    # =========================================
    # SEARCH FILTER
    # =========================================
    if search_query:

        medicines = medicines.filter(

            Q(
                medicine_id__icontains=search_query
            )

            |

            Q(
                name__icontains=search_query
            )

            |

            Q(
                generic_name__icontains=search_query
            )

            |

            Q(
                brand__icontains=search_query
            )

            |

            Q(
                category__icontains=search_query
            )

            |

            Q(
                manufacturer__icontains=search_query
            )

        )


    # =========================================
    # MEDICINE STATUS FILTER
    # =========================================
    if status_filter:

        medicines = medicines.filter(
            status=status_filter
        )


    # =========================================
    # EXPIRY FILTER
    # =========================================
    if expiry_filter == 'expired':

        medicines = medicines.filter(
            expiry_date__lt=today
        )


    elif expiry_filter == 'soon':

        medicines = medicines.filter(
            expiry_date__gte=today,
            expiry_date__lte=expiring_soon_date
        )


    elif expiry_filter == 'safe':

        medicines = medicines.filter(
            expiry_date__gt=expiring_soon_date
        )


    # =========================================
    # REPORT SUMMARY
    # =========================================
    total_medicines = medicines.count()


    expired_medicines = medicines.filter(
        expiry_date__lt=today
    ).count()


    expiring_soon_medicines = medicines.filter(
        expiry_date__gte=today,
        expiry_date__lte=expiring_soon_date
    ).count()


    safe_medicines = medicines.filter(
        expiry_date__gt=expiring_soon_date
    ).count()


    # =========================================
    # CONTEXT
    # =========================================
    context = {

        'medicines': medicines,

        'total_medicines': total_medicines,

        'expired_medicines': expired_medicines,

        'expiring_soon_medicines':
            expiring_soon_medicines,

        'safe_medicines': safe_medicines,

        'today': today,

        'expiring_soon_date':
            expiring_soon_date,

        'expiry_filter': expiry_filter,

        'status_filter': status_filter,

        'search_query': search_query,
    }


    return render(
        request,
        'store/reports/expiry_report.html',
        context
    )