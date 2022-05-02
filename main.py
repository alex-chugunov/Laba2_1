from flask import Flask, render_template, abort
import data_like_js

app = Flask(__name__)
wsgi_app = app.wsgi_app


@app.errorhandler(404)
def render_not_found(_):
    return "Ошибка 404, попробуйте снова или позже", 404


@app.route("/")
def render_main():
    return render_template("index.html")


@app.route("/categories/")
def render_categories():
    return render_template("categories.html")


@app.route("/product/")
def render_products():
    return render_template("product.html")


@app.route("/data/")
def render_data():
    result = f"<h1>Все продукты:</h1>\n\n"
    for i in range(1, len(data_like_js.products) + 1):
        result += f"""<p><a href = "/data/product/{i}/">{data_like_js.products[i]['name']}</a>\n</p>"""
    return result


@app.route("/data/categories/<category>/")
def render_data_categories(category):
    if category in data_like_js.categories:
        result = f"<h1>Категория: {category}\n"

        for product in data_like_js.products:
            if data_like_js.products[product]['category'] == category:
                result += f"""<p><a href = "/data/product/{product}/">{data_like_js.products[product]['name']}</a>\n</p>"""

        return result
    else:
        abort(404)


@app.route("/data/product/<int:id>/")
def render_data_products(id):
    if id in data_like_js.products:
        result = f"""
        <h1>Название: {data_like_js.products[id]['name']}</h1>
        <p>Категория: {data_like_js.products[id]['category']}</p>
        <p>Цена: {data_like_js.products[id]['price']} р.</p>
        """
        return result
    else:
        abort(404)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
