from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Sriram000%40@localhost:3306/nearbymart'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Categories(db.Model):
    CategoryID = db.Column(db.Integer, primary_key=True)
    CategoryName = db.Column(db.String(255), nullable=False)

class Electronics(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    BrandName = db.Column(db.String(255))
    ImageURL = db.Column(db.String(255))
    Specifications = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Rating = db.Column(db.DECIMAL(3, 2))
    ManufacturedDate = db.Column(db.DATE)
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    category = db.relationship('Categories', backref=db.backref('electronics', lazy=True))

class Groceries(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    BrandName = db.Column(db.String(255))
    ImageURL = db.Column(db.String(255))
    Specifications = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Rating = db.Column(db.DECIMAL(3, 2))
    ManufacturedDate = db.Column(db.DATE)
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    category = db.relationship('Categories', backref=db.backref('groceries', lazy=True))

class Cloths(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    BrandName = db.Column(db.String(255))
    ImageURL = db.Column(db.String(255))
    Specifications = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Rating = db.Column(db.DECIMAL(3, 2))
    ManufacturedDate = db.Column(db.DATE)
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    category = db.relationship('Categories', backref=db.backref('cloths', lazy=True))

class Footwear(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    BrandName = db.Column(db.String(255))
    ImageURL = db.Column(db.String(255))
    Specifications = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Rating = db.Column(db.DECIMAL(3, 2))
    ManufacturedDate = db.Column(db.DATE)
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    category = db.relationship('Categories', backref=db.backref('footwear', lazy=True))

class HomeAppliance(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    BrandName = db.Column(db.String(255))
    ImageURL = db.Column(db.String(255))
    Specifications = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Rating = db.Column(db.DECIMAL(3, 2))
    ManufacturedDate = db.Column(db.DATE)
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    category = db.relationship('Categories', backref=db.backref('home_appliance', lazy=True))

class Furniture(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    BrandName = db.Column(db.String(255))
    ImageURL = db.Column(db.String(255))
    Specifications = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Rating = db.Column(db.DECIMAL(3, 2))
    ManufacturedDate = db.Column(db.DATE)
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    category = db.relationship('Categories', backref=db.backref('furniture', lazy=True))

class Medicine(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    BrandName = db.Column(db.String(255))
    ImageURL = db.Column(db.String(255))
    Specifications = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Rating = db.Column(db.DECIMAL(3, 2))
    ManufacturedDate = db.Column(db.DATE)
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    category = db.relationship('Categories', backref=db.backref('medicine', lazy=True))

class DairyProducts(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(255), nullable=False)
    BrandName = db.Column(db.String(255))
    ImageURL = db.Column(db.String(255))
    Specifications = db.Column(db.Text)
    Price = db.Column(db.DECIMAL(10, 2), nullable=False)
    Rating = db.Column(db.DECIMAL(3, 2))
    ManufacturedDate = db.Column(db.DATE)
    CategoryID = db.Column(db.Integer, db.ForeignKey('categories.CategoryID'))
    category = db.relationship('Categories', backref=db.backref('dairy_products', lazy=True))


# Define the route for the index page
@app.route('/')
def index():
    return render_template('index.html')

# Define the route for the product_list page
@app.route('/product_list.html')
def product_list():
    return render_template('product_list.html')

@app.route('/favicon.ico')
def favicon():
    return '', 204

from flask import json

@app.route('/search/products')
def search_products():
    keyword = request.args.get('keyword')
    category_filter = request.args.get('category_filter')
    min_price = request.args.get('minPrice')
    max_price = request.args.get('maxPrice')
    min_rating = request.args.get('minRating')
    max_rating = request.args.get('maxRating')

    if not keyword:
        return jsonify({'error': 'Keyword not provided'}), 400

    try:
        # Query each category table separately based on the category filter
        if category_filter:
            # Use the category filter in your queries
            electronics_results = Electronics.query.filter(Electronics.ProductName.ilike(f'%{keyword}%'), Electronics.CategoryID == category_filter).all()
            groceries_results = Groceries.query.filter(Groceries.ProductName.ilike(f'%{keyword}%'), Groceries.CategoryID == category_filter).all()
            cloths_results = Cloths.query.filter(Cloths.ProductName.ilike(f'%{keyword}%'), Cloths.CategoryID == category_filter).all()
            footwear_results = Footwear.query.filter(Footwear.ProductName.ilike(f'%{keyword}%'), Footwear.CategoryID == category_filter).all()
            home_appliance_results = HomeAppliance.query.filter(HomeAppliance.ProductName.ilike(f'%{keyword}%'), HomeAppliance.CategoryID == category_filter).all()
            furniture_results = Furniture.query.filter(Furniture.ProductName.ilike(f'%{keyword}%'), Furniture.CategoryID == category_filter).all()
            medicine_results = Medicine.query.filter(Medicine.ProductName.ilike(f'%{keyword}%'), Medicine.CategoryID == category_filter).all()
            dairy_products_results = DairyProducts.query.filter(DairyProducts.ProductName.ilike(f'%{keyword}%'), DairyProducts.CategoryID == category_filter).all()
            # Add other categories as needed
        else:
            # No category filter, query all categories
            electronics_results = Electronics.query.filter(Electronics.ProductName.ilike(f'%{keyword}%')).all()
            groceries_results = Groceries.query.filter(Groceries.ProductName.ilike(f'%{keyword}%')).all()
            cloths_results = Cloths.query.filter(Cloths.ProductName.ilike(f'%{keyword}%')).all()
            footwear_results = Footwear.query.filter(Footwear.ProductName.ilike(f'%{keyword}%')).all()
            home_appliance_results = HomeAppliance.query.filter(HomeAppliance.ProductName.ilike(f'%{keyword}%')).all()
            furniture_results = Furniture.query.filter(Furniture.ProductName.ilike(f'%{keyword}%')).all()
            medicine_results = Medicine.query.filter(Medicine.ProductName.ilike(f'%{keyword}%')).all()
            dairy_products_results = DairyProducts.query.filter(DairyProducts.ProductName.ilike(f'%{keyword}%')).all()
            # Add other categories as needed

        # Combine the results from all tables
        all_results = (electronics_results + groceries_results + cloths_results + footwear_results + home_appliance_results + furniture_results + medicine_results + dairy_products_results)  # Add other categories as needed

         # Filter results based on price range
        if min_price and max_price:
            all_results = [result for result in all_results if float(result.Price) >= float(min_price) and float(result.Price) <= float(max_price)]
            # Filter results based on rating range
        if min_rating and max_rating:
            all_results = [result for result in all_results if result.Rating is not None and float(result.Rating) >= float(min_rating) and float(result.Rating) <= float(max_rating)]

        # Convert results to a JSON response
        response = [
            {
                'ProductName': result.ProductName,
                'BrandName': result.BrandName,
                'ImageURL': result.ImageURL,
                'Specifications': result.Specifications,
                'Price': float(result.Price),  # Convert to float if needed
                'Rating': float(result.Rating) if result.Rating is not None else None,  # Convert to float if not None
                'ManufacturedDate': str(result.ManufacturedDate) if result.ManufacturedDate is not None else None,  # Convert to string if not None
                'Category': result.category.CategoryName if result.category else None  # Assuming you want the category name
            }
            for result in all_results
        ]
        return json.dumps(response)
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return jsonify({'error': 'Database Error'}), 500


if __name__ == '__main__':
    app.run(debug=True)
