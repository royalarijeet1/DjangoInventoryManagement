from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import  ProductForm,AssemblyForm,ComponentForm
from .models import Product,Order,Warehouse,Assembly,Component
from django.contrib.auth.models import User


# Create your views here.
@login_required
def warehouse(request):
    warehouses=Warehouse.objects.all()

    context = {
        'warehouses':warehouses
    }
    return render(request,'dashboard/department.html',context)


@login_required
def index(request):
    # orders = Order.objects.all()
    products = Product.objects.all()
    # orders_count=orders.count()
    customers_count = User.objects.all().count()
    products_count = products.count()


    if request.method=='POST':
        form = ProductForm(request.POST)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('dashboard-index')

    else:
        form = ProductForm()
    context = {
        # 'orders': orders,
        'form':form,
        'products':products,
        'customers_count': customers_count,
        # 'orders_count': orders_count,
        'products_count': products_count

    }
    return render(request,'dashboard/index.html',context)

@login_required
def customers(request):
    customers = User.objects.all()
    customers_count = customers.count()
    # orders_count = Order.objects.all().count()
    products_count = Product.objects.all().count()

    context = {
        'customers': customers,
        'customers_count': customers_count,
        'products_count': products_count,
        # 'orders_count': orders_count,
    }
    return render(request,'dashboard/customers.html',context)

@login_required
def customer_detail(request, pk):

    customers = User.objects.get(id=pk)
    customers_count = User.objects.all().count()
    # orders_count = Order.objects.all().count()
    products_count = Product.objects.all().count()
    context = {
        'customers': customers,
        'customers_count': customers_count,
        'products_count': products_count,
        # 'orders_count': orders_count,

    }
    return render(request, 'dashboard/customers_detail.html', context)


@login_required
def customer_page(request):
    user = request.user

    # Ensure the user has a profile
    if hasattr(user, 'profile'):
        user_department = user.profile.department  # Get the staff's department

        # Filter products by department
        products = Product.objects.filter(department=user_department)
    else:
        products = Product.objects.none()  # No products if the user has no department

    context = {
        'products': products,
    }
    return render(request, 'dashboard/customer_index.html', context)

@login_required
def add_assembly(request,pk):
    item = Product.objects.get(id=pk)


    if request.method == 'POST':
        form=AssemblyForm(request.POST)
        if form.is_valid():
            assembly = form.save(commit=False)
            assembly.product = item
            assembly.save()
            return redirect('dashboard-product-view-assembly', item.id)
    else:
        form = AssemblyForm()
    context = {
        'form':form,
        'item':item
    }
    return render(request, 'dashboard/add_assembly.html', context)

@login_required
def view_assembly(request,pk):
    item = Product.objects.get(id=pk)
    assemblies=Assembly.objects.filter(product=item)

    context = {
        'item': item,
        'assemblies':assemblies,
        'id': pk,
    }
    return render(request, 'dashboard/view_assembly.html', context)

@login_required
def add_component(request,pk):

    assembly = Assembly.objects.get(id=pk)
    item = assembly.product
    #
    if request.method == 'POST':
         form=ComponentForm(request.POST)
         if form.is_valid():
             component = form.save(commit=False)
             component.assembly = assembly
             component.save()
             return redirect('dashboard-product-assembly-view-component', assembly.id)
    else:
        form = ComponentForm()
    context = {
        'form':form,
        'assembly':assembly,
        'item':item
    }
    return render(request, 'dashboard/add_component.html', context)




@login_required
def view_component(request,pk):

    assembly = Assembly.objects.get(id=pk)
    item = assembly.product
    components = Component.objects.filter(assembly=assembly)
    #

    context = {
        'item':item,
        'assembly':assembly,
        'id':pk,
        'components':components
    }
    return render(request, 'dashboard/view_component.html', context)


@login_required
def order(request):
    customers_count = User.objects.all().count()
    # orders = Order.objects.all()
    # orders_count = orders.count()
    products_count = Product.objects.all().count()
    context = {
        # 'orders': orders,
        'customers_count':customers_count,
        # 'orders_count': orders_count,
        'products_count': products_count
    }
    return render(request,'dashboard/order.html',context)


def product(request):

    customer = User.objects.filter(groups=2)
    customers_count = User.objects.all().count()

    products=Product.objects.all()
    products_count=products.count()
    # orders_count = Order.objects.all().count()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
    else:
        form = ProductForm()
    context={
        'customer':customer,
        'form': form,
        'products':products,
        'customers_count':customers_count,
        # 'orders_count': orders_count,
        'products_count':products_count
    }
    return render(request,'dashboard/product.html',context)


@login_required
def product_delete(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('dashboard-product')
    context = {
        'item': item
    }
    return render(request, 'dashboard/product_delete.html', context)


@login_required
def product_update(request, pk):
    item = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('dashboard-product')
        else:
            print(form.errors)  # Debug validation errors
    else:
        form = ProductForm(instance=item)
    context = {
        'form': form
    }
    return render(request, 'dashboard/product_edit.html', context)



