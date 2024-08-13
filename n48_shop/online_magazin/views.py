
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from typing import Optional

from .models import Product
from . form import OrderForm , CommentForm
from online_magazin.models import Product, Category, Comment
from .form import OrderModelForm,ProductModelForm
from django.contrib import messages
from django.db.models import Q

def product_list(request, category_id: Optional[int] = None):
    categories = Category.objects.all().order_by('id')
    search = request.GET.get('q')
    filter_type = request.GET.get('filter', '')
    if category_id:
        if filter_type == 'expensive':
            products = Product.objects.filter(category=category_id).order_by('-price')
        elif filter_type == 'cheap':
            products = Product.objects.filter(category=category_id).order_by('price')
        elif filter_type == 'rating':
            products = Product.objects.filter(Q(category=category_id) & Q(rating__gte=4)).order_by('-rating')

            products = Product.objects.filter(category=category_id)
        else:
            products = Product.objects.filter(category=category_id)

    else:
             products = Product.objects.all()
        if filter_type == 'expensive':
            products = Product.objects.all().order_by('-price')
        elif filter_type == 'cheap':
            products = Product.objects.all().order_by('price')
        elif filter_type == 'rating':
            products = Product.objects.filter(Q(rating__gte=4)).order_by('-rating')
            print(products)

        else:
            products = Product.objects.all()

        if search:
            products = products.filter(Q(name__icontains=search) | Q(comments__name__icontains=search))

        context = {
        'products': products,
        'categories': categories
          }
        return render (request, 'online_magazin.home.html',context)





from django.shortcuts import render, get_object_or_404
from .models import Product, Comment

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    query = request.GET.get('q')
    if query:
        comments = product.comments.filter(body__icontains=query)
    else:
        comments = product.comments.all()

    return render(request, 'deteil.html', {'product': product, 'comments': comments})

def add_comment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.product = product
            comment.save()
            return redirect('detail', product_id)

    context = {
        'form': form,
        'product': product
    }

    return render(request, 'online_magazin/detail.html', context)


def order_product(request, pk):
    product = Product.objects.filter(id=pk).first()
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            order.save()
            return redirect('detail', product.id)

    context = {
        'product': product,
        'form': form
    }

def add_order(request,product_id):
    product = get_object_or_404(Product, id=product_id)
    form = OrderModelForm()
    if request.method == 'GET':
        form = OrderModelForm(request.GET)
        if form.is_valid():
            order = form.save(commit=False)
            order.product = product
            if product.quantity >= order.quanity:
                product.quantity -= order.quanity
                order.save()
                product.save()
                messages.add_message(
                    request,
                    level=messages.SUCCESS,
                    message='Your order is successfully passed .'
                )

                return redirect('product_detail', product.id)
            else:
                messages.add_message(
                    request,
                    level=messages.ERROR,
                    message='You ordered more items .'
                )

    context = {
        'form': form,
        'product': product
            }
    return render(request, 'online_magazin/detail.html', context)
#Create -----

from django.contrib.auth.decorators import login_required
@login_required

def add_product(request ):
    form = ProductModelForm()
    if request.method == 'POST':
        form = ProductModelForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
    context = {
        'form': form
    }
    return render(request, 'online_magazin/templates/add_product.html', context)

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductModelForm(instance=product)
    if request.method == 'POST':
        form = ProductModelForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product.id)
        return redirect(request, 'online_magazin/edit.product.html', product_id)


#delete-----
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product:
        product.delete()
        return redirect('product_list')

