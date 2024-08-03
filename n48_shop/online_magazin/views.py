
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from typing import Optional

from .models import Product
from . form import OrderForm , CommentForm
from online_magazin.models import Product, Category, Comment
from .form import OrderModelForm,ProductModelForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

def product_list(request, cat_id):
    try:
        category = Category.objects.get(id=cat_id)
    except ObjectDoesNotExist:
        return render(request, 'online_magazin/home.html', {'message': 'Category not found.'})

    if cat_id:
        products = Product.objects.filter(category=cat_id)
    else:
        products = Product.objects.all()
    context = {
       'categories': category,
       'products': products
        }
    return render(request, 'online_magazin/home.html', context)


def product_detail(request, pk):
    comments = Comment.objects.filter(product=pk)
    product = Product.objects.get(id=pk)


    return render(request, 'online_magazin/detail.html', {'product': product})


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
    return render(request, 'online_magazin/add_product.html', context)

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

