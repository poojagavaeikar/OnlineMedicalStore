# =========================================
# CLEANUP DELETED SALES AFTER 30 DAYS
# =========================================

from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from store.models import Sale


class Command(BaseCommand):

    help = (
        'Permanently deletes walk-in sales that have '
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
        # GET ONLY OLD DELETED SALES
        # =========================================
        old_deleted_sales = Sale.objects.filter(
            is_deleted=True,
            deleted_at__isnull=False,
            deleted_at__lte=thirty_days_ago
        )

        # Count before deleting
        deleted_sales_count = (
            old_deleted_sales.count()
        )

        # =========================================
        # PERMANENT DELETE
        # =========================================
        old_deleted_sales.delete()

        # =========================================
        # SUCCESS MESSAGE
        # =========================================
        if deleted_sales_count > 0:

            self.stdout.write(
                self.style.SUCCESS(
                    f'{deleted_sales_count} old deleted '
                    f'sale(s) permanently deleted.'
                )
            )

        else:

            self.stdout.write(
                self.style.SUCCESS(
                    'No deleted sales older than '
                    '30 days were found.'
                )
            )