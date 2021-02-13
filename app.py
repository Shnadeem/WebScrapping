from flask import Flask, render_template, url_for, redirect, flash, request
import requests
from flask_cors import CORS, cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from utils.forms import SearchForm
from utils.utils import get_product_reviews, get_class_param, flipkart_scrapping_class


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'


# Variables declarations
headings = ('Product','Model','Name','Rating','Comments Heading','Comments')
part_url = "https://www.flipkart.com"
search_url = "https://www.flipkart.com/search?q="


# Routing logic starts from here

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
@cross_origin()
def home():
    form = SearchForm()
#    if form.validate_on_submit():
#        return redirect(url_for('result', search=form.Search_String.data.strip().replace(" ","+")))
    return render_template('home.html', title='Home - Products Review', form=form)


@app.route("/result", methods=['POST'])
@cross_origin()
def result():
    if request.method == 'POST':
        search = request.form['Search_String'].strip().replace(" ","+")
        url = search_url + search
    else:
        return redirect(url_for('home'))
    try:
        uClient = uReq(url)
        webPage = uClient.read()
        uClient.close()
    except:
        flash('Invalid strings has been passed for search, Kindly re-try with another string', 'warning')
        return redirect(url_for('home'))

    webPage_html = bs(webPage, "html.parser")
    products = webPage_html.findAll(get_class_param(flipkart_scrapping_class, 0)[0],
                                    get_class_param(flipkart_scrapping_class, 0)[1])
    if len(products) == 0:
        flash('Passed string does not have any match. Kindly retry with another string', 'danger')
        return redirect(url_for('home'))
    for prod in products:
        prod_urls = part_url + prod.a['href']
        url_response = requests.get(prod_urls)  # using only one url to fetch the reviews
        product_name = prod_urls.split('/')[3]
        prod_html = bs(url_response.text, "html.parser")
        comments_section = prod_html.find_all(get_class_param(flipkart_scrapping_class, 1)[0],
                                              get_class_param(flipkart_scrapping_class, 1)[1])
        reviews=[]
        for comments in comments_section:
            customer_name = get_product_reviews(comments,
                                                get_class_param(flipkart_scrapping_class, 2)[0],
                                                get_class_param(flipkart_scrapping_class, 2)[1])
            rating_given = get_product_reviews(comments,
                                               get_class_param(flipkart_scrapping_class, 3)[0],
                                               get_class_param(flipkart_scrapping_class, 3)[1])
            comments_head = get_product_reviews(comments,
                                                get_class_param(flipkart_scrapping_class, 4)[0],
                                                get_class_param(flipkart_scrapping_class, 4)[1])
            comments = get_product_reviews(comments,
                                           get_class_param(flipkart_scrapping_class, 5)[0],
                                           get_class_param(flipkart_scrapping_class, 5)[1]).replace("READ MORE","")
            comments_descr = (search.replace("+", " "), product_name, customer_name, rating_given, comments_head, comments)
            reviews.append(comments_descr)
        break                                   # This is to stop the scrapping after first product's URL
    return render_template('result.html', title='Results - Products Review', headings=headings, data=reviews)


if __name__ == '__main__':
    app.run(port=5001, debug=True)