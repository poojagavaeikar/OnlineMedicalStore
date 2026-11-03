from django.db import models


class Medicine(models.Model):

    # Basic Information
    medicine_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, null=True, blank=True)
    brand = models.CharField(max_length=200, null=True, blank=True)

    # Category & Manufacturer
    category = models.CharField(max_length=100, null=True, blank=True)
    manufacturer = models.CharField(max_length=200)

    # Packing Information
    pack_size = models.PositiveIntegerField(null=True, blank=True)
    unit = models.CharField(max_length=50, null=True, blank=True)

    # Tax & Product Information
    hsn = models.CharField(max_length=20, null=True, blank=True)
    gst = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Pricing
    mrp = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    purchase_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    selling_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # Prescription / Schedule
    prescription_required = models.BooleanField(default=False)
    schedule = models.CharField(max_length=20, blank=True)

    # Barcode
    barcode = models.CharField(max_length=100, blank=True)

    # Stock
    stock = models.PositiveIntegerField(default=0)
    low_stock_limit = models.PositiveIntegerField(default=10)

    # Expiry
    expiry_date = models.DateField()

    # Status
    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
        ],
        default='Active'
    )
 
    is_deleted = models.BooleanField(default=False)


       # Description
    description = models.TextField(blank=True)


    # Auto Generate Medicine ID
    def save(self, *args, **kwargs):
        if not self.medicine_id:
            last_medicine = Medicine.objects.order_by('-id').first()

            if last_medicine:
                next_number = last_medicine.id + 1
            else:
                next_number = 1

            self.medicine_id = f"MED{next_number:03d}"

        super().save(*args, **kwargs)


# =========================================
# CATEGORY MASTER
# =========================================

class Category(models.Model):

    category_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
        ],
        default='Active'
    )

    is_deleted = models.BooleanField(default=False)

    # Auto Generate Category ID
    def save(self, *args, **kwargs):
        if not self.category_id:
            last_category = Category.objects.order_by('-id').first()

            if last_category:
                next_number = last_category.id + 1
            else:
                next_number = 1

            self.category_id = f"CAT{next_number:03d}"

        super().save(*args, **kwargs)
            
            
    def __str__(self):
        return self.name
        
# =========================================
# MANUFACTURER MASTER
# =========================================

class Manufacturer(models.Model):

    manufacturer_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=150)

    contact_person = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
        ],
        default='Active'
    )

    is_deleted = models.BooleanField(default=False)

    # Auto Generate Manufacturer ID
    def save(self, *args, **kwargs):

        if not self.manufacturer_id:

            last_manufacturer = Manufacturer.objects.order_by('-id').first()

            if last_manufacturer:
                next_number = last_manufacturer.id + 1
            else:
                next_number = 1

            self.manufacturer_id = f"MFG{next_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# =========================================
# SUPPLIER MASTER
# =========================================

class Supplier(models.Model):

    supplier_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=150)

    contact_person = models.CharField(
        max_length=100,
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    email = models.EmailField(blank=True)

    address = models.TextField(blank=True)

    gst_number = models.CharField(
        max_length=30,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Active', 'Active'),
            ('Inactive', 'Inactive'),
        ],
        default='Active'
    )

    is_deleted = models.BooleanField(default=False)

    # Auto Generate Supplier ID
    def save(self, *args, **kwargs):

        if not self.supplier_id:

            last_supplier = Supplier.objects.order_by('-id').first()

            if last_supplier:
                next_number = last_supplier.id + 1
            else:
                next_number = 1

            self.supplier_id = f"SUP{next_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
# =========================================
# PURCHASE
# =========================================
class Purchase(models.Model):

    purchase_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT
    )

    invoice_number = models.CharField(
        max_length=100
    )

    purchase_date = models.DateField()

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )

    # =========================================
    # STOCK UPDATE TRACKING
    # =========================================
    stock_updated = models.BooleanField(
        default=False
    )

    notes = models.TextField(
        blank=True
    )
    

    # =========================================
    # AUTO PURCHASE ID
    # =========================================
    def save(self, *args, **kwargs):

        if not self.purchase_id:

            last_purchase = Purchase.objects.order_by('-id').first()

            next_number = (
                last_purchase.id + 1
                if last_purchase
                else 1
            )

            self.purchase_id = f"PUR{next_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.purchase_id
    
# =========================================
# PURCHASE ITEMS
# =========================================
class PurchaseItem(models.Model):

    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='items'
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField()

    purchase_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    batch_number = models.CharField(
        max_length=100,
        blank=True
    )

    expiry_date = models.DateField(
        null=True,
        blank=True
    )
    
    
    # =========================================
# PRESCRIPTION
# =========================================
class Prescription(models.Model):

    # =========================================
    # STATUS CHOICES
    # =========================================
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # =========================================
    # PRESCRIPTION DETAILS
    # =========================================
    prescription_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=15
    )

    prescription_image = models.ImageField(
        upload_to='prescriptions/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    notes = models.TextField(
        blank=True
    )
    
        # =========================================
    # SOFT DELETE
    # =========================================
    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =========================================
    # AUTO PRESCRIPTION ID
    # =========================================
    def save(self, *args, **kwargs):

        if not self.prescription_id:

            last_prescription = Prescription.objects.order_by(
                '-id'
            ).first()

            if last_prescription:
                next_number = last_prescription.id + 1
            else:
                next_number = 1

            self.prescription_id = (
                f'PRE{next_number:03d}'
            )

        super().save(*args, **kwargs)

    # =========================================
    # DISPLAY NAME
    # =========================================
    def __str__(self):
        return (
            f'{self.prescription_id} - '
            f'{self.customer_name}'
        )
    
   
# =========================================
# ONLINE ORDER
# =========================================
class Order(models.Model):

    # =========================================
    # ORDER STATUS CHOICES
    # =========================================
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Packed', 'Packed'),
        ('Shipped', 'Shipped'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    # =========================================
    # PAYMENT METHOD CHOICES
    # =========================================
    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Online', 'Online Payment'),
    ]

    # =========================================
    # PAYMENT STATUS CHOICES
    # =========================================
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]


    # =========================================
    # ORDER DETAILS
    # =========================================
    order_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=150
    )

    phone = models.CharField(
        max_length=15
    )

    email = models.EmailField(
        blank=True
    )

    delivery_address = models.TextField()

    order_date = models.DateTimeField(
        auto_now_add=True
    )
     
    # =========================================
    # DELIVERY PIN CODE
    # =========================================
    delivery_pincode = models.CharField(
        max_length=6,
        blank=True
    )

    # =========================================
    # PAYMENT DETAILS
    # =========================================
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='COD'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )

     
    # =========================================
    # ONLINE PAYMENT GATEWAY DETAILS
    # =========================================
    gateway_order_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    gateway_payment_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    gateway_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    # =========================================
    # ORDER STATUS
    # =========================================
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    
    # =========================================
    # STOCK UPDATE SAFETY
    # =========================================
    stock_updated = models.BooleanField(
        default=False
    )
    
    # =========================================
    # ORDER TRACKING TIMESTAMPS
    # =========================================
    confirmed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    packed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    shipped_at = models.DateTimeField(
        null=True,
        blank=True
    )

    out_for_delivery_at = models.DateTimeField(
        null=True,
        blank=True
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    expected_delivery_date = models.DateField(
        null=True,
        blank=True
    )
    
    # =========================================
    # ORDER AMOUNT
    # =========================================
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(
        blank=True
    )


     
    # =========================================
    # SOFT DELETE
    # =========================================
    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )
 
 
 
    # =========================================
    # AUTO ORDER ID
    # =========================================
    def save(self, *args, **kwargs):

        if not self.order_id:

            last_order = Order.objects.order_by(
                '-id'
            ).first()

            if last_order:
                next_number = last_order.id + 1
            else:
                next_number = 1

            self.order_id = (
                f'ORD{next_number:03d}'
            )

        super().save(*args, **kwargs)


    # =========================================
    # DISPLAY NAME
    # =========================================
    def __str__(self):
        return (
            f'{self.order_id} - '
            f'{self.customer_name}'
        )


# =========================================
# ORDER ITEM
# =========================================
class OrderItem(models.Model):

    # =========================================
    # ORDER
    # =========================================
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )


    # =========================================
    # MEDICINE
    # =========================================
    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT
    )


    # =========================================
    # ITEM DETAILS
    # =========================================
    quantity = models.PositiveIntegerField(
        default=1
    )

    selling_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    # =========================================
    # LINE TOTAL
    # =========================================
    @property
    def line_total(self):
        return (
            self.quantity *
            self.selling_rate
        )


    # =========================================
    # DISPLAY NAME
    # =========================================
    def __str__(self):
        return (
            f'{self.order.order_id} - '
            f'{self.medicine.name}'
        )
        
# =========================================
# DELIVERY MANAGEMENT
# =========================================
class Delivery(models.Model):

    # =========================================
    # DELIVERY STATUS CHOICES
    # =========================================
    STATUS_CHOICES = [
        ('Assigned', 'Assigned'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
    ]

    # =========================================
    # LINK WITH ONLINE ORDER
    # One order = one delivery
    # =========================================
    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery'
    )

    # =========================================
    # DELIVERY ID
    # Example: DEL001
    # =========================================
    delivery_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    # =========================================
    # DELIVERY PERSON DETAILS
    # =========================================
    delivery_person_name = models.CharField(
        max_length=150
    )

    delivery_person_phone = models.CharField(
        max_length=15
    )

    # =========================================
    # DELIVERY STATUS
    # =========================================
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Assigned'
    )

    # =========================================
    # DELIVERY TIMESTAMPS
    # =========================================
    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    # =========================================
    # DELIVERY NOTES
    # =========================================
    notes = models.TextField(
        blank=True
    )

    # =========================================
    # AUTO GENERATE DELIVERY ID
    # Example: DEL001
    # =========================================
    def save(self, *args, **kwargs):

        if not self.delivery_id:

            last_delivery = Delivery.objects.order_by(
                '-id'
            ).first()

            if last_delivery:
                next_number = last_delivery.id + 1
            else:
                next_number = 1

            self.delivery_id = (
                f'DEL{next_number:03d}'
            )

        super().save(*args, **kwargs)

    # =========================================
    # DISPLAY NAME
    # =========================================
    def __str__(self):
        return (
            f'{self.delivery_id} - '
            f'{self.order.order_id}'
        )    
        
        
        
# =========================================
# WALK-IN POS SALE
# =========================================
class Sale(models.Model):

    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),
    ]

    sale_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    customer_name = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    customer_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True
    )

    sale_date = models.DateTimeField(
        auto_now_add=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='Cash'
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    # =========================================
    # SOFT DELETE
    # =========================================
    is_deleted = models.BooleanField(
        default=False
    )

    deleted_at = models.DateTimeField(
        null=True,
        blank=True
    )


    def save(self, *args, **kwargs):

        # =========================================
        # AUTO GENERATE SALE ID
        # Example: SALE001
        # =========================================
        if not self.sale_id:

            last_sale = Sale.objects.order_by(
                '-id'
            ).first()

            if last_sale:
                next_number = last_sale.id + 1
            else:
                next_number = 1

            self.sale_id = f"SALE{next_number:03d}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.sale_id


# =========================================
# WALK-IN POS SALE ITEM
# =========================================
class SaleItem(models.Model):

    sale = models.ForeignKey(
        Sale,
        on_delete=models.CASCADE,
        related_name='items'
    )

    medicine = models.ForeignKey(
        Medicine,
        on_delete=models.PROTECT
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    selling_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    line_total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):
        return f"{self.sale.sale_id} - {self.medicine.name}"
    
    # =========================================
# PAYMENT MANAGEMENT
# =========================================
class Payment(models.Model):

    SOURCE_CHOICES = [
        ('Online Order', 'Online Order'),
        ('Walk-in POS', 'Walk-in POS'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery'),
        ('Cash', 'Cash'),
        ('UPI', 'UPI'),
        ('Card', 'Card'),
        ('Online', 'Online Payment'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded'),
    ]

    payment_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True
    )

    source = models.CharField(
        max_length=30,
        choices=SOURCE_CHOICES
    )

    reference_id = models.CharField(
        max_length=30
    )

    customer_name = models.CharField(
        max_length=150,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    notes = models.TextField(
        blank=True
    )

    # =========================================
    # AUTO GENERATE PAYMENT ID
    # Example: PAY001
    # =========================================
    def save(self, *args, **kwargs):

        if not self.payment_id:

            last_payment = Payment.objects.order_by(
                '-id'
            ).first()

            if last_payment:
                next_number = last_payment.id + 1
            else:
                next_number = 1

            self.payment_id = (
                f'PAY{next_number:03d}'
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f'{self.payment_id} - '
            f'{self.reference_id}'
        )
    