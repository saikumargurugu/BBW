import random
from shop.models import Brand, ProductType, SubCategory, Category, Color, Product

def populate_mock_data():
    # Create Brands
    brands = ["Nike", "Adidas", "Puma", "Reebok", "Under Armour"]
    for brand_name in brands:
        Brand.objects.get_or_create(name=brand_name, defaults={"discount": random.uniform(5, 20)})

    # Create Product Types
    product_types = ["Shoes", "Clothing", "Accessories", "Equipment"]
    for product_type_name in product_types:
        ProductType.objects.get_or_create(name=product_type_name, defaults={"discount": random.uniform(5, 15)})

    # Create SubCategories
    subcategories = ["Running Shoes", "Sports Jerseys", "Wristbands", "Badminton Rackets", "Tennis Balls"]
    subcategory_objects = {}
    for subcategory_name in subcategories:
        subcategory, _ = SubCategory.objects.get_or_create(name=subcategory_name, defaults={"discount": random.uniform(5, 10)})
        subcategory_objects[subcategory_name] = subcategory

    # Create Categories
    categories = {
        "Sports Equipment": ["Badminton Rackets", "Tennis Balls"],
        "Apparel": ["Running Shoes", "Sports Jerseys"],
    }
    for category_name, subcategory_names in categories.items():
        category, _ = Category.objects.get_or_create(name=category_name, defaults={"discount": random.uniform(5, 10)})
        for subcategory_name in subcategory_names:
            subcategory = subcategory_objects.get(subcategory_name)
            if subcategory:
                category.subcategories.add(subcategory)

    # Create Colors
    colors = ["Red", "Blue", "Green", "Black", "White"]
    for color_name in colors:
        Color.objects.get_or_create(name=color_name)

    # Create Products
    for _ in range(50):  # Generate 50 products
        name = f"Product {_}"
        brand = random.choice(Brand.objects.all())
        category = random.choice(Category.objects.all())
        product_type = random.choice(ProductType.objects.all())
        qty = random.randint(1, 100)
        product_details = f"This is a detailed description of {name}."
        in_stock = random.choice([True, False])
        discount = random.uniform(5, 20)

        # Use get_or_create to avoid duplicates
        product, created = Product.objects.get_or_create(
            name=name,
            defaults={
                "brand": brand,
                "category": category,
                "product_type": product_type,
                "qty": qty,
                "product_details": product_details,
                "in_stock": in_stock,
                "discount": discount,
            },
        )

        if created:
            # Add random colors to the product only if it was newly created
            product.colors.set(random.sample(list(Color.objects.all()), random.randint(1, 3)))

    print("Mock data populated successfully!")

if __name__ == "__main__":
    populate_mock_data()