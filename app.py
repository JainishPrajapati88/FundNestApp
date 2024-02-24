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
    

if __name__ =="__main__":
    app.run(debug=True)