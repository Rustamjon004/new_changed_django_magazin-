
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from typing import Optional

from .models import Product

from online_magazin.models import Product, Category, Comment


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

    return render(request, 'detail.html', context)


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
