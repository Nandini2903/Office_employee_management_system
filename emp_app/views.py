from django.shortcuts import render, HttpResponse
from .models import Employee, Role, Department
from datetime import datetime
from django.db import IntegrityError
from django.db.models import Q

def index(request):
    return render(request, 'index.html')

def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    print(context)
    return render(request, 'view_all_emp.html', context)

def add_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        salary = request.POST.get('salary')
        bonus = request.POST.get('bonus')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        role = request.POST.get('role')

        if first_name and last_name and salary and bonus and phone and department and role:
            try:
                salary = int(salary)
                bonus = int(bonus)
                phone = int(phone)
                department = int(department)
                role = int(role)
            except ValueError:
                return HttpResponse("Invalid input: Please ensure salary, bonus, phone, department, and role are valid integers.")

            # Check if department and role exist
            if not Department.objects.filter(id=department).exists():
                return HttpResponse("Invalid department.")
            if not Role.objects.filter(id=role).exists():
                return HttpResponse("Invalid role.")

            try:
                new_emp = Employee(
                    first_name=first_name,
                    last_name=last_name,
                    salary=salary,
                    bonus=bonus,
                    phone=phone,
                    department_id=department,
                    role_id=role,
                    hire_date=datetime.now()
                )
                new_emp.save()
                return HttpResponse('Employee Added Successfully')
            except IntegrityError as e:
                return HttpResponse(f"Error: {str(e)}")
        else:
            return HttpResponse("Please fill out all fields.")

    elif request.method == 'GET':
        departments = Department.objects.all()
        roles = Role.objects.all()
        context = {
            'departments': departments,
            'roles': roles
        }
        return render(request, 'add_emp.html', context)
    else:
        return HttpResponse("An Exception Occurred! Employee Has Not Been Added")


def remove_emp(request, emp_id = 0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Succesfully")

        except:
            return HttpResponse("Please enter a valid EMP ID")
    emps = Employee.objects.all()
    context = {
        'emps' : emps

    }
    return render(request, 'remove_emp.html',context)
def filter_emp(request):
    if request.method=='POST':
        name = request.POST.get('name', '')
        department = request.POST.get('department', '')
        role = request.POST.get('role', '')
        emps = Employee.objects.all()
        if name:
            emps= emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if department:
            emps= emps.filter(department__name__icontains = department)
        if role:
            emps=emps.filter(role__name__icontains = role)

        context = {
            'emps' : emps

        }
        return render(request,'view_all_emp.html', context)
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse(' An Exception Occured')