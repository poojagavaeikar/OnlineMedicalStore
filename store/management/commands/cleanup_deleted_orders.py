# =========================================
# CLEANUP DELETED ONLINE ORDERS AFTER 30 DAYS
# =========================================

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from store.models import Order


class Command(BaseCommand):

    help = (
        'Permanently deletes online orders that have '
        'been in Deleted History for 30 days or more.'
    )

    def handle(self, *args, **options):

        # =========================================
        # CALCULATE 30 DAYS AGO
        # =========================================
        thirty_days_ago = (
            timezone.now() -
            timedelta(days=30)
        )

        # =========================================
        # GET ONLY OLD DELETED ONLINE ORDERS
        # =========================================
        old_deleted_orders = Order.objects.filter(
            is_deleted=True,
            deleted_at__isnull=False,
            deleted_at__lte=thirty_days_ago
        )

        # Count before deleting
        deleted_orders_count = (
            old_deleted_orders.count()
        )

        # =========================================
        # PERMANENT DELETE
        # =========================================
        # This does NOT restore/change medicine stock.
        # Payment history is preserved because Payment
        # is not directly deleted here.
        old_deleted_orders.delete()

        # =========================================
        # SUCCESS MESSAGE
        # =========================================
        if deleted_orders_count > 0:

            self.stdout.write(
                self.style.SUCCESS(
                    f'{deleted_orders_count} old deleted '
                    f'order(s) permanently deleted.'
                )
            )

        else:

            self.stdout.write(
                self.style.SUCCESS(
                    'No deleted online orders older than '
                    '30 days were found.'
                )
            )