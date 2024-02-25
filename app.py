from flask import *
from pymongo import *
from pymongo.server_api import ServerApi
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DiplomatesAtDuHacks3.0'
client = MongoClient("mongodb+srv://fundnest:fundnest@cluster0.gnbp0sa.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", server_api=ServerApi('1'))
db = client.fundnest
collection = db.users

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/CreatingAccount",methods=['GET','POST'])
def CreatingAccount():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        UserName = request.form['UserName']
        email = request.form['email']
        password = request.form['password']
        occupation = request.form['occupation']

        if db.users.find_one({'email': email}) or db.users.find_one({'UserName': UserName}):
            return render_template('signup.html', error_message="User already registered with that mail id OR UserID")
        else:
            user_data = {
                'first_name': first_name,
                'last_name': last_name,
                'UserName':UserName,
                'email': email,
                'password': password,
                'occupation': occupation
            }

            db.users.insert_one(user_data)

            if occupation == 'startup_founder':
                return redirect(url_for('startup_info', user_name=UserName))
            elif occupation == 'investor':
                return redirect(url_for('investor_info', user_name=UserName))
            elif occupation=='seller':
                return redirect(url_for('seller_info', user_name=UserName))
            else:
                return redirect(url_for('login'))
    else:
        return redirect(url_for('signup'))

@app.route("/startup_info/<user_name>", methods=['GET', 'POST'])
def startup_info(user_name):
    if request.method == 'POST':
        startup_name = request.form['startup_name']
        year_of_found = request.form['year_of_found']
        last_financial_details = request.form['last_financial_details']
        number_of_patents = request.form['number_of_patents']
        yearly_turnover = request.form['yearly_turnover']

        startup_logo = request.files['startup_logo'].read()

        dp_base64 = base64.b64encode(startup_logo).decode('utf-8')

        db.users.update_one({'UserName':user_name}, {
            '$set': {
                'startup_info': {
                    'startup_name': startup_name,
                    'year_of_found': year_of_found,
                    'last_financial_details': last_financial_details,
                    'number_of_patents': number_of_patents,
                    'yearly_turnover': yearly_turnover,
                    'dp': dp_base64
                }
            }
        })

        return redirect(url_for('login'))

    return render_template('startup_info.html')

@app.route("/seller_info/<user_name>", methods=['GET', 'POST'])
def seller_info(user_name):
    if request.method == 'POST':
        shop_name = request.form['shop_name']
        Type_of_Business = request.form['Type_of_Business']
        seller_logo = request.files['seller_logo'].read()
        dp_base64 = base64.b64encode(seller_logo).decode('utf-8')
        
        db.users.update_one({'UserName': user_name}, {
            '$set': {
                'seller_info': {
                    'shop_name': shop_name ,
                    'Type_of_Business': Type_of_Business,
                    'dp':dp_base64
                }
            }
        })
        return redirect(url_for('login'))
    return render_template('seller_info.html')

@app.route("/investor_info/<user_name>", methods=['GET', 'POST'])
def investor_info(user_name):
    if request.method == 'POST':
        total_investments = request.form['total_investments']
        area_of_interest = request.form['area_of_interest']

        investor_image = request.files['investor_image'].read()
        dp_base64 = base64.b64encode(investor_image).decode('utf-8')

        db.users.update_one({'UserName': user_name}, {
            '$set': {
                'investor_info': {
                    'total_investments': total_investments,
                    'area_of_interest': area_of_interest,
                    'dp':dp_base64
                }
            }
        })

        return redirect(url_for('login'))

    return render_template('investor_info.html')

@app.route('/home')
def home():
    if 'emailID' in session:
        user_data = db.users.find_one({'email': session['emailID']})

        if user_data:
            first_name = user_data.get('first_name', '')
            last_name = user_data.get('last_name', '')
            UserName = user_data.get('UserName','')
            occupation = user_data.get('occupation', '')
            email = user_data.get('email','')

            posts = db.posts.find().sort('_id', -1)

            if occupation == 'seller':
                return render_template('home.html', first_name=first_name, last_name=last_name,UserName = UserName,posts=posts,email = email,is_seller=True)
            else:
                return render_template('home.html', first_name=first_name, last_name=last_name,UserName = UserName ,posts=posts,email = email,is_seller=False)
        else:
            return render_template('home.html', error_message="User data not found")

    else:
        return redirect(url_for('login'))
    
    
@app.route('/Notifications')
def Notifications():
    if 'emailID' not in session:
        return redirect(url_for('login'))
    
    email = session['emailID']
    Notifications = db.ReqForMeet.find({'FounderMail':email}).sort('_id', -1)
    return render_template('notifications.html',Notifications=Notifications)

@app.route('/RequestingForMeeting', methods=['GET', 'POST'])
def RequestingForMeeting():
    if 'emailID' not in session:
        return redirect(url_for('login'))
    
    usrData = db.users.find_one({'email':session['emailID']})
    Mail = usrData.get('email','')
    date = request.form['date']
    time = request.form['time']
    FounderMail = request.form['fMailID']
    ReqForMeet = {
        'FounderMail':FounderMail,
        'Mail':Mail,
        'Date':date,
        'Time':time
    }
    db.ReqForMeet.insert_one(ReqForMeet)
    link=f"https://video-app-u4dq.onrender.com/{FounderMail}"
    from_email="gpainfo617@gmail.com"
    password="hwhdwqqcwnltztpa"
    subject=f"Invitation to Video Chat on [{date}] at [{time}]"
    body=f'''
    <h5>Dear Sir / Madam,</h5>
    <p>
    
    I hope this email finds you well. I am writing to extend an invitation to a video chat scheduled for {date} at {time}. We have an important matter to discuss, and I believe a video chat would be the most effective way to address it.

    To join the video chat, please use the following link: <button><a href="{link}">Link</a></button>. Kindly ensure that you have a stable internet connection and access to a device with a webcam and microphone.

    If the proposed date and time are not convenient for you, please let me know at your earliest convenience, and we can arrange an alternative time that suits us both.

    I look forward to our discussion and appreciate your prompt attention to this matter.

    
    </p>
    <p>
    Best regards,
    FundNest
    
    </p>
    
    '''
    
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = Mail
    
    msg.attach(MIMEText(body, 'html'))


    with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, password)
            server.sendmail(from_email, Mail, msg.as_string())
            server.sendmail(from_email, FounderMail, msg.as_string())
            print("Mail Send Successfully")

    return redirect(url_for('home'))

@app.route('/profile/<user_name>')
def profile(user_name):
    if 'emailID' not in session:
        return redirect(url_for('login'))
    
    user_data = db.users.find_one({'UserName':user_name})

    if not user_data:
        return render_template('profile.html', error_message="User not found")

    first_name = user_data.get('first_name', '')
    last_name = user_data.get('last_name', '')
    email = user_data.get('email', '')
    occupation = user_data.get('occupation', '')
    email = user_data.get('email','')

    if email == session.get('emailID'):
        if occupation=='startup_founder':
            additional_info = user_data.get('startup_info', {})
            return render_template('profile.html', first_name=first_name, last_name=last_name, occupation=occupation,additional_info=additional_info)
        elif occupation=='seller':
            additional_info = user_data.get('seller_info', {})
            return render_template('profile.html', first_name=first_name, last_name=last_name, occupation=occupation,additional_info=additional_info)
        else:
            investor_info=user_data.get('investor_info',{})
            return render_template('profile.html', first_name=first_name, last_name=last_name, occupation=occupation, additional_info=investor_info)
    else:
        if occupation=='startup_founder':
            additional_info = user_data.get('startup_info', {})
            return render_template('profile.html', first_name=first_name, last_name=last_name,email=email,occupation=occupation, additional_info=additional_info, readonly=True)
        elif occupation=='seller':
            additional_info = user_data.get('seller_info', {})
            return render_template('profile.html', first_name=first_name, last_name=last_name, occupation=occupation,additional_info=additional_info, readonly=True)
        else:
            investor_info =user_data.get('investor_info',{})
            return render_template('profile.html', first_name=first_name, last_name=last_name,occupation=occupation,additional_info=investor_info, readonly=True)


@app.route('/updatingProfile', methods=['POST'])
def update_profile():
    if 'emailID' not in session:
        return redirect(url_for('login'))

    email = session['emailID']

    first_name = request.form.get('first_name', '')
    last_name = request.form.get('last_name', '')

    user_data = db.users.find_one({'email': email})

    occupation = user_data.get('occupation', '')

    if occupation == 'startup_founder':
        startup_name = request.form.get('startup_name', '')
        year_of_found = request.form.get('year_of_found', '')
        last_financial_details = request.form.get('last_financial_details', '')
        number_of_patents = request.form.get('number_of_patents', '')
        yearly_turnover = request.form.get('yearly_turnover', '')

        if 'dp' in request.files:
            file = request.files['dp']
            if file.filename != '':
                print("in if part")
                dp = file.read()
                dp_base64 = base64.b64encode(dp).decode('utf-8')
                print(dp_base64)
            else:
                print("in else part - No file selected")
                dp_base64 = user_data.get('startup_info', {}).get('dp', '')
                print(dp_base64)


        db.users.update_one({'email': email}, {
            '$set': {
                'first_name': first_name,
                'last_name': last_name,
                'startup_info': {
                    'startup_name': startup_name,
                    'year_of_found': year_of_found,
                    'last_financial_details': last_financial_details,
                    'number_of_patents': number_of_patents,
                    'yearly_turnover': yearly_turnover,
                    'dp':dp_base64
                }
            }
        })
    elif occupation == 'investor':
        total_investments = request.form.get('total_investments', '')
        area_of_interest = request.form.get('area_of_interest', '')


        if 'dp' in request.files:
            file = request.files['dp']
            if file.filename != '':
                print("in if part")
                dp = file.read()
                dp_base64 = base64.b64encode(dp).decode('utf-8')
                print(dp_base64)
            else:
                print("in else part - No file selected")
                dp_base64 = user_data.get('investor_info', {}).get('dp', '')
                print(dp_base64)

            
        
        db.users.update_one({'email': email}, {
            '$set': {
                'first_name': first_name,
                'last_name': last_name,
                'investor_info': {
                    'total_investments': total_investments,
                    'area_of_interest': area_of_interest,
                    'dp':dp_base64
                }
            }
        })
    else:
        shop_name= request.form.get('shop_name' , '')
        Type_of_Business = request.form.get('Type_of_Business' , '')
        

        if 'dp' in request.files:
            file = request.files['dp']
            if file.filename != '':
                print("in if part")
                dp = file.read()
                dp_base64 = base64.b64encode(dp).decode('utf-8')
                print(dp_base64)
            else:
                print("in else part - No file selected")
                dp_base64 = user_data.get('seller_info', {}).get('dp', '')
                print(dp_base64)
        

        db.users.update_one({'email': email}, {
                '$set': {
                    'first_name': first_name,
                    'last_name': last_name,
                    'seller_info': {
                        'shop_name': shop_name,
                        'Type_of_Business': Type_of_Business,
                        'dp':dp_base64
                    }
                }
            })
    return redirect(url_for('profile', user_name=user_data.get('UserName','')))

@app.route('/AddPost')
def AddPost():
    if 'emailID' not in session:
        return redirect(url_for('login'))
    return render_template('AddPost.html')

@app.route('/AddIngPost', methods=['POST'])
def AddIngPost():
    if 'emailID' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        img = request.files['image'].read()
        dp_base64 = base64.b64encode(img).decode('utf-8')
        
        email_id = session['emailID']
        usr_data = db.users.find_one({'email':email_id})

        
        if db.posts.find_one({}, sort=[('id', -1)]):
            last_post = db.posts.find_one({}, sort=[('id', -1)])
            print(last_post)
            last_post_id = int(last_post['id'])
            new_post_id = last_post_id + 1
        else:
            new_post_id = 1

        usrName = usr_data.get('UserName','')
        db.posts.insert_one({
            'id': new_post_id,
            'UserName':usrName,
            'email': email_id,
            'title': title,
            'description': description,
            'img':dp_base64
        })

        return redirect(url_for('posts'))
    return redirect(url_for('posts'))

@app.route('/YourPosts')
def posts():
    if 'emailID' not in session:
        return redirect(url_for('login'))
    email_id = session['emailID']
    user_posts = db.posts.find({'email': email_id}).sort('_id', -1)
    return render_template('posts.html', user_posts=user_posts)

@app.route('/deletingPost', methods = ['POST','GET'])
def deletingPost():
    if 'emailID' not in session:
        return redirect(url_for('login'))
    
    Post_ID = int(request.form['pID'])
    print("post id",Post_ID)

    db.posts.find_one_and_delete({'id': Post_ID})
    return redirect(url_for('home'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('emailID', None)
    return redirect(url_for('login'))

@app.route('/loggingIn',methods=['POST'])
def loggingIn():
    emailID = request.form['email']
    PassWd = request.form['pass']

    if db.users.find_one({'email': emailID, 'password': PassWd}):
        session['emailID'] = emailID
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))
    
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if 'emailID' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        product_name = request.form['name']
        product_description = request.form['description']
        product_id = request.form['product_id']
        product_price = request.form['price']
        product_seller = session['emailID']
        product_field = request.form['field']
        product_payment_link = request.form['payment_link']
        
        if db.products.find_one({'product_id': product_id}):
            return render_template('add_products.html', error_message="This product id already exists")
        else:
            product_data = {
                'name': product_name,
                'description': product_description,
                'product_id': product_id,
                'price': product_price,
                'seller': product_seller,
                'field': product_field,
                'payment_link':product_payment_link
            }
            db.products.insert_one(product_data)
        
        return redirect('/home')

    return render_template('add_products.html')

@app.route('/update_products', methods=['GET'])
def update_products_page():
    if 'emailID' not in session:
        return redirect(url_for('login'))

    seller_email = session['emailID']

    seller_products = db.products.find({'seller': seller_email})

    return render_template('update_products.html', products=seller_products)

@app.route('/update_product/<product_id>', methods=['GET','POST'])
def update_product(product_id):
    if 'emailID' not in session:
        return redirect(url_for('login'))


    seller_email = session['emailID']
    print(seller_email)

    product = db.products.find_one({'product_id': product_id, 'seller': seller_email}) 
    print(product)
    if not product:
        return render_template('update_products.html', error_message="Product not found or you are not authorized to update it")

    if request.method == 'POST':
        updated_product = {
            'name': request.form['name'],
            'description': request.form['description'],
            'price': request.form['price'],
            'field': request.form['field']
        }
        db.products.update_one({'product_id': product_id, 'seller': seller_email}, {'$set': updated_product})

        return redirect('/home')

    return render_template('update_product_form.html', product=product)


@app.route('/delete_product', methods=['GET'])
def delete_product_page():
    if 'emailID' not in session:
        return redirect(url_for('login'))

    seller_email = session['emailID']

    seller_products = db.products.find({'seller': seller_email})

    return render_template('delete_products.html', products=seller_products)


@app.route('/delete_product/<product_id>', methods=['POST'])
def delete_product(product_id):
    if 'emailID' not in session:
        return redirect(url_for('login'))

    seller_email = session['emailID']

    result = db.products.delete_one({'product_id': product_id, 'seller': seller_email})

    if result.deleted_count == 1:
        return redirect('/home')
    else:
        return render_template('delete_products.html', error_message="Product not found or you are not authorized to delete it")
    
@app.route('/products')
def products():
    if 'emailID' not in session:
        return redirect(url_for('login'))
    field_filter = request.args.get('field', '') 
    if field_filter:
        products = db.products.find({'field': field_filter})
    else:
        products = db.products.find()
    
    return render_template('products.html', products=products)

@app.route('/submit_order', methods=['POST'])
def submit_order():
    if request.method == 'POST':
        print("In Post Method")

        product_id = request.form['product_id']
        seller_mail = db.products.find({'product_id':product_id}).next()['seller']
        quantity = request.form['quantity']
        email=session.get('emailID')
        UserName = db.users.find( {'email': email}).next()['UserName']

        p_Data = db.products.find_one({'product_id':product_id})

        link_for_payment = p_Data['payment_link']

        order_data = {
                "usernm":UserName,
                'user_email':session.get('emailID'),
                'seller_email':seller_mail,
                'product_id': product_id,
                'quantity': quantity
        }
        print(order_data)
        db.orders.insert_one(order_data)

        return redirect(link_for_payment)
    else:
        return render_template('products.html')

@app.route('/orders')
def orders():
    if 'emailID' not in session:
        return redirect(url_for('login'))
    email=session.get('emailID')

    orders = db.orders.find({'seller_email':email})

    return render_template('seller_side_orders.html',orders=orders)
    
@app.route ('/privacy_policy',methods = ['GET'])
def policy():
    return render_template('privacy_policy.html')

@app.route('/info',methods=['POST','GET'])
def info():
    return render_template('contact_us.html')

if __name__ =="__main__":
    app.run(debug=True)