from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.db.models.functions import Lower

from .models import Product, Category, Subcategory
from .forms import ProductForm

# Create your views here.
def all_products(request):
    """ 
    A view to show all products, including sorting and search queries 
    (This view was obtained from ChatGPT to improve the filtering)
    """
    
    products = Product.objects.all()
    
    # Get Params
    query = request.GET.get('q', None)
    sort = request.GET.get('sort', None)
    direction = request.GET.get('direction', None)
    
    category_list = request.GET.get('category', None)
    subcategory_list = request.GET.get('subcategory', None)
    
    current_categories = None
    current_subcategories = None
            
    # Category filter (safe and slug based)
    if category_list:
        category_list = [c.strip().lower() for c in category_list.split(',')]

        products = products.filter(category__slug__in=category_list)
        current_categories = Category.objects.filter(slug__in=category_list)

    # Subcategory filter
    if subcategory_list:
        subcategory_list = [s.strip().lower() for s in subcategory_list.split(',')]

        products = products.filter(subcategory__slug__in=subcategory_list)
        current_subcategories = Subcategory.objects.filter(slug__in=subcategory_list)
        
    # Search
    if query:
        if not query.strip():
            return redirect('products')

        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )
    
    # Sorting code by Google AI and ChatGPT
    if sort:
        sortkey = sort
        
        if sortkey == 'name':
            products = products.annotate(lower_name=Lower('name'))
            sortkey = 'lower_name'

        if sortkey == 'category':
            sortkey = 'category__name'
        
        if sortkey == 'subcategory':
            sortkey = 'subcategory__name'

        if direction in 'desc':
            sortkey = f'-{sortkey}'
            
        products = products.order_by(sortkey)
       
    # Context     
    context = {
        'products': products,
        'search_term': query,
        'current_categories': current_categories,
        'current_subcategories': current_subcategories,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


@login_required
def add_product(request):
    """ Add a product to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, ' Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)


@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')
        
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }
    return render(request, template, context)


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))