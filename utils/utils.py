
# List of classes which will be used to fetch the details from web page
# For any website, just update these values as per their own classes and run the code.
# Here, we are putting it for flipkart
flipkart_scrapping_class = [
    {"div": {"class": "_2kHMtA"}},         # Idx=0, Searched Product's URL
    {'div': {'class': "col _2wzgFH"}},     # Idx=1, Comment section
    {'p':{'class': '_2sc7ZR _2V5EHH'}},    # Idx=2, customer name
    {'div':{'class':"_3LWZlK _1BLPMq"}},   # Idx=3, ratng given
    {'p':{'class': "_2-N8zT"}},            # Idx=4, Comment Heading
    {'div':{'class': ''}}                  # Idx=5, Comments
]

# Independent selection of classes and html tag
def get_class_param(param_inp,idx):
  for k, v in param_inp[idx].items():
    return k,v


# Function to fetch the details for passing tags and class
def get_product_reviews(comment, tag, class_tag):
    try:
        return comment.find_all(tag, class_tag)[0].text
    except:
        return "Not Available"