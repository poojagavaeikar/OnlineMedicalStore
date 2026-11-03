@echo off

cd /d "C:\Users\dell\Desktop\OnlineMedicalStore"

"C:\Users\dell\Desktop\OnlineMedicalStore\venv\Scripts\python.exe" manage.py cleanup_deleted_sales

exit /b