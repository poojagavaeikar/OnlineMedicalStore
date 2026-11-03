
from django.urls import path
from . import views

urlpatterns = [
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/add/', views.add_medicine, name='add_medicine'),
    path('medicines/edit/<int:id>/', views.edit_medicine, name='edit_medicine'),

    # View Medicine
    path('medicines/view/<int:id>/', views.view_medicine, name='view_medicine'),
    path('medicines/delete/<int:id>/', views.delete_medicine, name='delete_medicine'),
    path('medicines/restore/<int:id>/', views.restore_medicine, name='restore_medicine'),
    path('medicines/deleted/', views.deleted_medicines, name='deleted_medicines'),
   
   
    # =========================================
    # CATEGORY MASTER
    # =========================================
    path('categories/', views.category_list, name='category_list'), 
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/view/<int:id>/', views.view_category, name='view_category'),
    path('categories/edit/<int:id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:id>/', views.delete_category, name='delete_category'),
    path('categories/deleted/', views.deleted_categories, name='deleted_categories'),
    path('categories/restore/<int:id>/', views.restore_category, name='restore_category'),
    
    
# =========================================
# MANUFACTURER MASTER
# =========================================

path(
    'manufacturers/',
    views.manufacturer_list,
    name='manufacturer_list'
),

path(
    'manufacturers/add/',
    views.add_manufacturer,
    name='add_manufacturer'
),

path(
    'manufacturers/view/<int:id>/',
    views.view_manufacturer,
    name='view_manufacturer'
),
    
    path(
    'manufacturers/edit/<int:id>/',
    views.edit_manufacturer,
    name='edit_manufacturer'
),
  path(
    'manufacturers/edit/<int:id>/',
    views.edit_manufacturer,
    name='edit_manufacturer'
),

path(
    'manufacturers/delete/<int:id>/',
    views.delete_manufacturer,
    name='delete_manufacturer'
),  
    
    path(
    'manufacturers/deleted/',
    views.deleted_manufacturers,
    name='deleted_manufacturers'
),
    
    path(
    'manufacturers/restore/<int:id>/',
    views.restore_manufacturer,
    name='restore_manufacturer'
),
  
  
# =========================================
# SUPPLIER MASTER
# =========================================

path(
    'suppliers/',
    views.supplier_list,
    name='supplier_list'
),
    
    path(
    'suppliers/add/',
    views.add_supplier,
    name='add_supplier'
),

# =========================================
# VIEW SUPPLIER
# =========================================
path(
    'suppliers/view/<int:id>/',
    views.view_supplier,
    name='view_supplier'
),

# =========================================
# EDIT SUPPLIER
# =========================================
path(
    'suppliers/edit/<int:id>/',
    views.edit_supplier,
    name='edit_supplier'
),

# =========================================
# DELETE SUPPLIER
# =========================================
path(
    'suppliers/delete/<int:id>/',
    views.delete_supplier,
    name='delete_supplier'
),

# =========================================
# DELETED SUPPLIERS
# =========================================
path(
    'suppliers/deleted/',
    views.deleted_suppliers,
    name='deleted_suppliers'
),

# =========================================
# RESTORE SUPPLIER
# =========================================
path(
    'suppliers/restore/<int:id>/',
    views.restore_supplier,
    name='restore_supplier'
),

# =========================================
# INVENTORY
# =========================================
path(
    'inventory/',
    views.inventory_list,
    name='inventory_list'
),

# =========================================
# PURCHASE
# =========================================
path('purchase/', views.purchase_list, name='purchase_list'),


# VIEW PURCHASE

path(
    'purchase/view/<int:id>/',
    views.view_purchase,
    name='view_purchase'
),
#Add  Purches
path('purchase/add/', views.add_purchase, name='add_purchase'),
path(
    'purchase/complete/<int:id>/',
    views.complete_purchase,
    name='complete_purchase'
),

# =========================================
# CANCEL PURCHASE
# =========================================
path(
    'purchase/cancel/<int:id>/',
    views.cancel_purchase,
    name='cancel_purchase'
),


# =========================================
# PRESCRIPTION
# =========================================
path(
    'prescriptions/',
    views.prescription_list,
    name='prescription_list'
),

# =========================================
# ADD PRESCRIPTION
# =========================================
path(
    'prescriptions/add/',
    views.add_prescription,
    name='add_prescription'
),

# =========================================
# VIEW PRESCRIPTION
# =========================================
path(
    'prescriptions/view/<int:id>/',
    views.view_prescription,
    name='view_prescription'
),

# =========================================
# APPROVE PRESCRIPTION
# =========================================
path(
    'prescriptions/approve/<int:id>/',
    views.approve_prescription,
    name='approve_prescription'
),

# =========================================
# REJECT PRESCRIPTION
# =========================================
path(
    'prescriptions/reject/<int:id>/',
    views.reject_prescription,
    name='reject_prescription'
),

# =========================================
# CREATE ONLINE ORDER
# =========================================
path(
    'orders/create/',
    views.create_order,
    name='create_order'
),

# =========================================
# ONLINE ORDERS
# =========================================
path(
    'orders/',
    views.order_list,
    name='order_list'
),
# =========================================
# VIEW ONLINE ORDER
# =========================================
path(
    'orders/view/<int:id>/',
    views.view_order,
    name='view_order'
),

# =========================================
# EDIT ONLINE ORDER
# =========================================
path(
    'orders/edit/<int:id>/',
    views.edit_order,
    name='edit_order'
),

# =========================================
# CONFIRM ONLINE ORDER
# =========================================
path(
    'orders/confirm/<int:id>/',
    views.confirm_order,
    name='confirm_order'
),

# =========================================
# PACK ONLINE ORDER
# =========================================
path(
    'orders/pack/<int:id>/',
    views.pack_order,
    name='pack_order'
),

# =========================================
# MARK COD PAYMENT RECEIVED
# =========================================
path(
    'orders/payment-received/<int:id>/',
    views.mark_payment_received,
    name='mark_payment_received'
),

# =========================================
# SHIP ONLINE ORDER
# =========================================
path(
    'orders/ship/<int:id>/',
    views.ship_order,
    name='ship_order'
),

# =========================================
# OUT FOR DELIVERY ONLINE ORDER
# =========================================
path(
    'orders/out-for-delivery/<int:id>/',
    views.out_for_delivery_order,
    name='out_for_delivery_order'
),

# =========================================
# DELIVER ONLINE ORDER
# =========================================
path(
    'orders/deliver/<int:id>/',
    views.deliver_order,
    name='deliver_order'
),

# =========================================
# CANCEL ONLINE ORDER
# =========================================
path(
    'orders/cancel/<int:id>/',
    views.cancel_order,
    name='cancel_order'
),

# =========================================
# CUSTOMER TRACK ORDER SEARCH
# =========================================
path(
    'orders/track/',
    views.track_order_search,
    name='track_order_search'
),

# =========================================
# CUSTOMER ORDER TRACKING
# =========================================
path(
    'orders/track/<str:order_id>/',
    views.track_order,
    name='track_order'
),


# =========================================
# DELIVERY MANAGEMENT
# =========================================
path(
    'deliveries/',
    views.delivery_list,
    name='delivery_list'
),


# =========================================
# ASSIGN DELIVERY
# =========================================
path(
    'deliveries/assign/<int:order_id>/',
    views.assign_delivery,
    name='assign_delivery'
),

# =========================================
# DELIVERY -> OUT FOR DELIVERY
# =========================================
path(
    'deliveries/out-for-delivery/<int:id>/',
    views.delivery_out_for_delivery,
    name='delivery_out_for_delivery'
),

# =========================================
# DELIVERY -> DELIVERED
# =========================================
path(
    'deliveries/delivered/<int:id>/',
    views.delivery_delivered,
    name='delivery_delivered'
),


# =========================================
# VIEW DELIVERY DETAILS
# =========================================
path(
    'deliveries/view/<int:id>/',
    views.view_delivery,
    name='view_delivery'
),


# =========================================
# PAYMENT MANAGEMENT
# =========================================
path(
    'payments/',
    views.payment_list,
    name='payment_list'
),

path(
    'payments/view/<int:id>/',
    views.view_payment,
    name='view_payment'
),

path(
    'orders/delete/<int:id>/',
    views.delete_order,
    name='delete_order'
),

path(
    'orders/deleted-history/',
    views.deleted_order_history,
    name='deleted_order_history'
),

path(
    'orders/restore/<int:id>/',
    views.restore_order,
    name='restore_order'
),


path(
    'orders/permanent-delete/<int:id>/',
    views.permanent_delete_order,
    name='permanent_delete_order'
),

# =========================================
# REPORTS
# =========================================
path(
    'reports/',
    views.report_dashboard,
    name='report_dashboard'
),

path(
    'reports/sales/',
    views.sales_report,
    name='sales_report'
),

path(
    'reports/online-orders/',
    views.online_orders_report,
    name='online_orders_report'
),

path(
    'reports/purchases/',
    views.purchase_report,
    name='purchase_report'
),

path(
    'reports/payments/',
    views.payment_report,
    name='payment_report'
),

path(
    'reports/inventory/',
    views.inventory_report,
    name='inventory_report'
),

path(
    'reports/expiry/',
    views.expiry_report,
    name='expiry_report'
),



# =========================================
# WALK-IN POS
# =========================================
path(
    'pos/',
    views.walk_in_pos,
    name='walk_in_pos'
),

# =========================================
# WALK-IN POS SALE INVOICE
# =========================================
path(
    'pos/invoice/<int:sale_id>/',
    views.sale_invoice,
    name='sale_invoice'
),

# =========================================
# SALES & INVOICE HISTORY
# =========================================
path(
    'sales/',
    views.sales_list,
    name='sales_list'
),

# =========================================
# DELETE WALK-IN SALE HISTORY
# =========================================
path(
    'sales/delete/<int:sale_id>/',
    views.delete_sale,
    name='delete_sale'
),

# =========================================
# DELETED SALES HISTORY
# =========================================
path(
    'sales/deleted/',
    views.deleted_sales_list,
    name='deleted_sales_list'
),


# =========================================
# RESTORE DELETED WALK-IN SALE
# =========================================
path(
    'sales/restore/<int:sale_id>/',
    views.restore_sale,
    name='restore_sale'
),


# =========================================
# PERMANENTLY DELETE WALK-IN SALE
# =========================================
path(
    'sales/permanent-delete/<int:sale_id>/',
    views.permanently_delete_sale,
    name='permanently_delete_sale'
),
]