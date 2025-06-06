from flask import Flask
from flask import render_template, request, jsonify, url_for, redirect
import re
from markupsafe import Markup, escape
import uuid

app = Flask(__name__)

data ={
    "1": {
        "id": "1",
        "title": "MagicLinen",
        "image": "https://www.thegoodtrade.com/wp-content/uploads/2023/09/magiclinen-sustainable-linen-dresses-576x720.jpeg",
        "age_group": "25-55",
        "summary": "MagicLinen is a family-run brand specializing in beautifully crafted linen apparel and home textiles. Made in Lithuania, their pieces emphasize natural elegance, comfort, and sustainability. With a focus on timeless designs, breathable fabrics, and eco-friendly production, MagicLinen is perfect for individuals who value quality, craftsmanship, and a relaxed yet refined aesthetic. The brand uses sustainably produced linen, free of harmful chemicals, local and low emissions, prioritizes zero waste, and biodegradable packaging.",
        "founders": "Vita Murauskiene",
        "price_range": "$50 - $250",
        "categories": ["Boho", "Relaxed Natural"],
        "similar_brand_ids": ["2", "3"]
    },
    "2": {
        "id": "2",
        "title": "Selva Negra",
        "image": "https://selvanegra.us/cdn/shop/products/000012570017.jpg?v=1678149662",
        "age_group": "20-40",
        "summary": "Founded by Kristen Gonzalez, Selva Negra is a Latina-owned fashion brand that blends ethical production with bold, contemporary designs. Made in Los Angeles using sustainable fabrics, the brand embraces vibrant colors and statement pieces, ideal for creative professionals, social gatherings, and casual wear with an artistic edge.",
        "founders": "Kristen Gonzalez",
        "price_range": "$80 - $400",
        "categories": ["Boho", "Relaxed Natural","Chic","Bold"],
        "similar_brand_ids": ["1", "4"]
    },
    "3": {
        "id": "3",
        "title": "Pact",
        "image": "https://www.thegoodtrade.com/wp-content/uploads/2023/09/la-relaxed-sustainable-womens-clothes-1-576x864.jpeg",
        "age_group": "18-50",
        "summary": "Founded by Brendan Synnott, Pact is an eco-friendly brand specializing in organic cotton clothing for everyday wear. Their comfortable, minimalist basics are ideal for casual, work-from-home, and travel attire, offering a versatile wardrobe for those prioritizing sustainability without sacrificing affordability.",
        "founders": "Brendan Synnott",
        "price_range": "$20 - $150",
        "categories": ["Everyday Wear","Minimalist","Modern"],
        "similar_brand_ids": ["1", "5"]
    },
    "4": {
        "id": "4",
        "title": "Buck Mason",
        "image": "https://www.thegoodtrade.com/wp-content/uploads/2023/09/buck-mason-mens-sustainable-clothing-576x768.jpeg",
        "age_group": "25-55",
        "summary": "Founded by Erik Allen and Sasha Koehn, Buck Mason is an American-made brand known for its elevated everyday essentials. Focused on quality craftsmanship and timeless design, Buck Mason offers modern takes on classic menswear, including premium T-shirts, denim, and outerwear. With an emphasis on durability and simplicity, the brand appeals to those seeking effortless, well-made wardrobe staples.",
        "founders": "Erik Allen, Sasha Koehn",
        "price_range": "$40 - $500",
        "categories": ["Everyday Wear","Minimalist","Modern"],
        "similar_brand_ids": ["2", "6"]
    },
    "5": {
        "id": "5",
        "title": "ThredUp",
        "image": "https://images.squarespace-cdn.com/content/5511f9bee4b068878ae651fb/1529089572933-XZH6KL6Z55XZ81OWYJBQ/thredup1.jpg?format=1500w&content-type=image%2Fjpeg",
        "age_group": "18-50",
        "summary": "Founded by James Reinhart, ThredUp is one of the largest online thrift stores, offering secondhand fashion at affordable prices. The brand promotes circular fashion and sustainable shopping by giving clothes a second life. Ideal for budget-conscious shoppers, eco-friendly consumers, and those looking for vintage finds.",
        "founders": "James Reinhart",
        "price_range": "$5 - $200",
        "categories": ["Secondhand", "Circular Fashion"],
        "similar_brand_ids": ["6", "7"]
    },
    "6": {
        "id": "6",
        "title": "Reformation",
        "image": "https://cdn.sanity.io/images/hc18dks8/production/19b345a5b0957d1d0d2b4cfb58bc5f290ec73b43-2000x1200.jpg",
        "age_group": "20-40",
        "summary": "Founded by Yael Aflalo, Reformation is known for its trendy yet eco-conscious designs. Using sustainable fabrics and ethical production, the brand creates stylish, feminine pieces perfect for weddings, date nights, and casual chic wear.",
        "founders": "Yael Aflalo",
        "price_range": "$80 - $500",
        "categories": ["Chic", "Eco-Luxe"],
        "similar_brand_ids": ["5", "8"]
    },
    "7": {
        "id": "7",
        "title": "Kotn",
        "image": "https://thesustainablebusinessguide.com/wp-content/uploads/2023/08/Kotn-Ethical-Clothing-1440x962.jpeg",
        "age_group": "25-45",
        "summary": "Founded by Mackenzie Yeates, Kotn creates high-quality essentials using ethically sourced Egyptian cotton. Their minimalist, timeless pieces are ideal for everyday wear, work attire, and relaxed weekends.",
        "founders": "Mackenzie Yeates",
        "price_range": "$40 - $200",
        "categories": ["Minimalist", "Modern","Eco-Luxe"],
        "similar_brand_ids": ["6", "9"]
    },
    "8": {
        "id": "8",
        "title": "Quince",
        "image": "https://www.thegoodtrade.com/wp-content/uploads/2024/04/sustainable-clothing-brand-quince-1-edited-576x768.jpeg",
        "age_group": "18-50",
        "summary": "Quince, founded with the goal of making high-quality, sustainable fashion affordable, offers luxury-grade essentials at fair prices. Their cashmere, silk, and organic cotton pieces are perfect for work, travel, and elevated casual wear.",
        "founders": "Sid Gupta",
        "price_range": "$30 - $300",
        "categories": ["Minimalist","Eco-Luxe","Casual"],
        "similar_brand_ids": ["7", "10"]
    },
    "9": {
        "id": "9",
        "title": "Everlane",
        "image": "https://thegreenhubonline.com/wp-content/uploads/2017/04/everlane.jpg",
        "age_group": "20-50",
        "summary": "Founded by Michael Preysman, Everlane is a brand committed to radical transparency and ethical production. Their minimalist and versatile pieces are ideal for workwear, casual outings, and travel, focusing on timeless wardrobe staples.",
        "founders": "Michael Preysman",
        "price_range": "$30 - $250",
        "categories": ["Minimalist", "Eco-Luxe", "Casual"],
        "similar_brand_ids": ["8", "10"]
    },
    "10": {
        "id": "10",
        "title": "Sézane",
        "image": "https://www.thegoodtrade.com/wp-content/uploads/2024/04/sustainable-clothes-sezane-1-edited-576x768.jpeg",
        "age_group": "25-45",
        "summary": "Founded by Morgane Sézalory, Sézane is a French brand that blends Parisian chic with sustainable fashion. Their vintage-inspired, feminine pieces are perfect for date nights, weekend outings, and effortlessly elegant everyday wear.",
        "founders": "Morgane Sézalory",
        "price_range": "$80 - $400",
        "categories": ["Chic", "Boho", "Relaxed Natural", "Bold"],
        "similar_brand_ids": ["9", "7"]
    }
}


@app.route('/')
def home():
    popular_items = list(data.values())[:3]  
    return render_template("home.html", popular_items=popular_items)


@app.route('/search')
def search():
    query = request.args.get('q', '')
    query = request.args.get("q", "").strip().lower()
    if not query:
        return render_template("search.html", query="", results=[])
    
    results = [
        item for item in data.values()
        if query in item['title'].lower() or
           query in item['founders'].lower() or
           any(query in category.lower() for category in item['categories'])
    ]
    return render_template('search.html', results=results, query=query)


@app.route('/add', methods=['GET', 'POST'])
def add_item():
    errors = {}  # Ensure errors is always defined
    success = False
    new_id = None

    if request.method == 'POST':
        form_data = request.form

        required_fields = ['title', 'age_group', 'summary', 'founders', 'price_range', 'categories', 'image']
        for field in required_fields:
            if not form_data.get(field, '').strip():
                errors[field] = 'This field is required.'

        if not errors:
            new_id = str(uuid.uuid4())
            data[new_id] = {
                'id': new_id,
                'title': form_data['title'],
                'age_group': form_data['age_group'],
                'summary': form_data['summary'],
                'founders': form_data['founders'],
                'price_range': form_data['price_range'],
                'categories': [c.strip() for c in form_data['categories'].split(',')],
                'image': form_data['image']
            }
            success = True

    return render_template('add.html', errors=errors, success=success, new_id=new_id)


@app.route('/view/<id>')
def view(id):
    item = data.get(id)
    if not item:
        return "Item not found", 404
    
    relevant_brands = [
        {"id": similar_id, "title": data.get(str(similar_id), {}).get("title", "Unknown Brand")}
        for similar_id in item.get("similar_brand_ids", [])
    ]

    return render_template('view.html', item=item, relevant_brands=relevant_brands)

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    item = data.get(id)
    if not item:
        return "Item not found", 404

    errors = {}  # Initialize errors dictionary

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        age_group = request.form.get('age_group', '').strip()
        summary = request.form.get('summary', '').strip()
        founders = request.form.get('founders', '').strip()
        price_range = request.form.get('price_range', '').strip()
        categories = request.form.get('categories')
        if categories:
            categories = [category.strip() for category in categories.split(',')]
        image = request.form.get('image', '').strip()


        # Validate the form fields
        if not title:
            errors['title'] = 'Title cannot be empty'
        if not summary:
            errors['summary'] = 'Summary cannot be empty'
        if not image:
            errors['image'] = 'Image URL cannot be empty'
        if not age_group:
            errors['age_group'] = 'Targeted Age Group cannot be empty'
        if not founders:
            errors['founders'] = 'Founders cannot be empty'
        if not price_range:
            errors['price_range'] = 'Price Range cannot be empty'
        if not categories:
            errors['categories'] = 'Categories cannot be empty'

        # If no errors, update the item and redirect
        if not errors:
            item['title'] = title
            item['summary'] = summary
            item['age_group'] = age_group
            item['image'] = image
            item['founders'] = founders
            item['price_range'] = price_range
            item['categories'] = categories

            return redirect(url_for('view', id=id))

        

        return render_template('edit.html', item=item, errors=errors)

    return render_template('edit.html', item=item, errors=errors)


@app.route('/category/<category_name>')
def category(category_name):
    matched_items = []

    for item in data.values():
        # Clean up categories to avoid whitespace issues
        categories = [cat.strip() for cat in item.get('categories', [])]
        if category_name in categories:
            matched_items.append(item)

    return render_template('category.html', category_name=category_name, items=matched_items)


# Function to highlight matches
def highlight(text, query):
    pattern = re.escape(query)  
    highlighted = re.sub(
        pattern,
        lambda match: f'<span class="highlight">{escape(match.group(0))}</span>',
        escape(text),
        flags=re.IGNORECASE  # Case-insensitive matching
    )
    return Markup(highlighted)  # Mark as safe HTML

# Register the filter
app.jinja_env.filters['highlight'] = highlight


if __name__ == '__main__':
    app.run(debug = True, port=5001)