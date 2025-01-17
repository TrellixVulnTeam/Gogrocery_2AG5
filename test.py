#all important imports

from flask import Flask,request, json, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask import request, redirect, url_for, render_template
from sqlalchemy import desc, and_, or_, func
#func for aggregation in sql

from sqlalchemy.exc import IntegrityError
from settings import db,app
from datetime import date
import datetime


#all settings details in setings.py file

#to get the errors printed on to screen
app.debug = True

#test class for testing
#did this when the project was just starting
class Test(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(255), unique=False)
	age = db.Column(db.Integer)
	email = db.Column(db.String(20),unique = True)
	
	
	def __init__(self,userrname,age,email):
		
		self.username = name
		self.age = age
		self.email = email
	
	def __repr_(self):
		return '<user %r>' % self.username

#db.create_all()

'''
INSERT INTO test (id,username,age,email) VALUES (10, 'Teddy', 23, 'Teddy@bear.com');
'''

@app.route('/')
def index():
	# This is just for testing
	# if 'username' in session:
		# username = session['username']
		# return 'Logged in as ' + username +"<br /><b><a href='/logout'>click here to log out</a></b>"
	# return "You are not logged in <br><a href='/login'><b>click here to log in</b></a>"
	return render_template('login.html')


#backend call after inputting username and password	
@app.route('/login',  methods=['POST'])
def login():
	
	username = request.form['username']
	password = request.form['password']
	
	#check if there is another user who is already logged in...logout that user
	if 'user' in session:
		session.pop('user', None)
	
	from database import Admin
	obj = Admin.query.filter(and_(Admin.username == username, Admin.password == password)).first()
	
	#if that user isn't there in the database or if the password is incorrect then return to llogin page again
	if obj != None:
		session['user'] = username
		return redirect(url_for('dashboard'))
	else:
		claim = "Wrong Username or Password!!"
		return redirect(url_for('index'))
	

@app.route('/logout')
def logout():
	# remove the username from the session if it is there
	session.pop('user', None)
	return redirect(url_for('index'))			
			
@app.route('/signUp')
def signUp():
    return render_template('ajax_test.html')

	
@app.route('/add_user', methods=['POST'])
def add_user():
	#only admin can add new users
	if 'user' in session:
		if session['user'] == 'Admin' :
			
			from database import Admin
			
			username = request.form['username']
			password = request.form['password']
			user = Admin(username, password)
			db.session.add(user)
			db.session.commit()
			return "New User named" + username + "and with password " + password + "successfully created!"
		else :
			return "You are not an Admin and so you can't Add a new User! Sorry!"
	else:
		return redirect(url_for('index'))
	
#test route ..dont bother much
@app.route('/select')
def select_test():
    return render_template('select.html')	

#header file which renders navigation bar for all pages in the web app	
@app.route('/header')
def header():
	#for giving login and update password options
	if 'user' in session:
		username = session['user']
	else:
		username = "NO user logged In. Please Login!"
	return render_template('header.html', username = username)	

#footer file which renders footer bar for all pages in the web app		
@app.route('/footer')
def footer():
    return render_template('footer.html')
	
	
@app.route('/signUpUser', methods=['POST'])
def signUpUser():
	#To register a user/admin 
	# Can be added only by the admin ad no other person has this privilege
	user =  request.form['username'];
	password = request.form['password'];
	
	all = Test.query.all()#returns  a list of objects
	
	
    #return json.dumps({'status':'OK','user':user,'pass':password});
	#list_of_data = ['abc','def','xyz']
	list_of_data = [[k.email, k.username] for k in all] 
	
	#return jsonify(list_of_data = list_of_data)
	#ajax return 
	return json.dumps(list_of_data)

@app.route('/bill_fill')
def bill_form():
	from database import Bills
	#to display the bill number which will be used 
	last_bill = Bills.query.order_by(desc(Bills.bill_no)).limit(1).first()
	#add +1 to the last id ...
	invoice_no = int(last_bill.bill_no) + 1
	
	return render_template('bill_form.html', invoice_no = invoice_no)

#backend part for updating the transactions associated with a bill and adding new bill in table	
@app.route('/bill_fill_backend', methods = ['POST'])
def bill_form_backend():
	from database import Bills, Product, Stock, Customer, Transactions
	
	
	#get all details
	products = request.form.getlist('product[]')  #since there can be any number of products in a bill, there is an array passed, so products will have array	
	qty = request.form.getlist('qty[]') #similarly, qty is array
	cost = request.form.getlist('cost[]')
	cgst = request.form.getlist('cgst[]')
	sgst = request.form.getlist('sgst[]')
	total = request.form.getlist('total[]')
	gst = request.form['gst']
	
	
	length = len(products) #get the no of products in the bill
	
	bill_amt = sum(map(float, total)) # get the bill amount 
	
	c = Customer.query.filter_by(cid = 'NONE').first() #since no customer ID is required when there is bill generated by the shopkeeper
	c_name = c.c_name #by default the customer name is NONE
	
	
	
	bill = Bills(3, length, bill_amt, gst,-1, c_name ,c , 'NONE', 'NONE', 'NONE') #create Bill object and add bill to database
	
	
	#for each item -> have a transaction inserted in the transactions table
	for i in range(length):
		prod = Product.query.filter_by(p_name = products[i]).first()
		t = Transactions(bill, prod, cost[i],sgst[i],cgst[i], qty[i], total[i]);
		s = Stock.query.filter_by(pid = prod.pid).first()
		s.stocks_left = s.stocks_left - int(qty[i])
		db.session.add(t)
		db.session.commit()
	
	#add and commit to database
	db.session.add(bill)
	db.session.commit()
	
	# print(products, qty, cgst, sgst, total)
	return render_template('success_bill_fill.html')
	

@app.route('/stock_add', methods = ['POST'])
def stock_add():
	from database import Product, Supplier, Stock
	
	
	p_category = request.form['category']
	p_sub_category = request.form['sub_category']
	pname = request.form['Product']
	qty = request.form['stock']
	
	prod = Product.query.filter_by(p_name = pname).first()#get Products by product name
	s = Stock.query.filter_by(pid = prod.pid).first() #get the stock object using product_id
	s.stocks_left = s.stocks_left + int(qty) #update the stock
	
	db.session.commit() #commit
		
	return render_template('success_update_stock.html')
	

@app.route('/get_list_of_products', methods=['GET'])
def list_of_products():
	#<form action = {{ url_for('list_of_products') }} method = 'POST' >
	#returns the list of products as a list of string! ex:occurence = ttani
	#occurrence = request.form['occurrence'] #for get method
	occurrence = request.args.get('occurrence')
	#occurence = request.args.get('nn')
	from database import Product
	all_products = Product.query.all()
	#list_of_products = [[k.p_name, k.pid, k.p_price, k.p_category, k.p_sub_category] for k in all_products]
	#filtered_list = list(filter(lambda k: occurrence in k[0] ,list_of_products))
	
	filtered_list = {k.p_name: [k.pid, k.p_price, k.gst, k.p_category, k.p_sub_category] for k in all_products if occurrence in k.p_name}
	
	# //output -> ["krittania", "brittania"]
	#print(filtered_list)
	
	return json.dumps(filtered_list)	

@app.route('/all_products')
def all_products():
	
	from database import Product
	all_products = Product.query.all()
	return render_template('products_test.html', products = all_products)

#@app.route('/all_suppliers', methods=['POST'])	
@app.route('/all_suppliers')
def all_suppliers():
	from database import Supplier
	
	all_suppliers = Supplier.query.all()
	
	#return as dictionary with key as name of supplier; helps in UI
	filtered_list = {k.s_name : [k.sid, k.s_contact_name, k.s_number] for k in all_suppliers}
	return json.dumps(filtered_list) #ajax call return

@app.route('/filter_products')
def filter_products():
	return render_template('product_filter.html')

@app.route('/dashboard')
def dashboard():
	# first page which the user lands up afte logging  in to the web app
	return render_template('dashboard.html')

@app.route('/all_products_filter', methods=['POST'])
def all_products_filter():
	stocks_gt = request.form['stock_gt']
	stocks_lt = request.form['stock_lt']
	category  = request.form['category']
	
	
	from database import Product, Stock
	
	all_products = Product.query.all() #first have a general query
	
	if(category == 'ANY'):
		q = Product.query  #store the intermediate result and on this do the queries 
	else :
		q = Product.query.filter_by(p_category = category) #filter based on category
	if( stocks_gt != '-1'):
		q = q.join(Stock).filter(Stock.stocks_left >= stocks_gt) #based on stock greater than some valuee
	else:
		q = q.join(Stock) #else join and just keep for the use of stock lesser than
	if( stocks_lt != '-1'):
		q = q.filter(Stock.stocks_left <= stocks_lt)
		
	q = q.with_entities(Product, Stock).all() #we want only product and stock
	
	#return products as key value pairs
	products = {k[0].pid:[k[0].p_name, k[0].p_category, k[0].p_sub_category, k[0].p_price, k[0].gst, k[1].stocks_left] for k in q}
	
	#return render_template('filter_test.html', products = q)	
	return json.dumps(products) #ajax call return

@app.route('/update_stock')
def update_stock():
	return render_template('update_stock.html')

@app.route('/add_supplier_page')
def add_supplier_page():
	return render_template('add_supplier_page.html')
	
@app.route('/add_supplier', methods=['POST'])
def add_supplier():
	from database import Supplier, Supplier_product
	#try:
	
		
	s_name = request.form['name']
	s_contact_name = request.form['contact']
	s_number = request.form['mobile_no']
	s_address = request.form['address']
	
	
	#get the id for next supplier...shuld be 's11' if previous one is 's10'
	sids = Supplier.query.all()
	sid_list = [k.sid for k in sids] #get all the id's 
	sid_list = [int(k[1:]) for k in sid_list] #remove first letter 's' from them
	sid_list.sort( reverse = True) #sort the remaning in descing order
	prefix = 's'
	postfix = sid_list[0] + 1 # add +1 to the highest 
	sid = prefix + str(postfix) #add 's' to that number .this is the id
		
	#Create a Supplier object to insert into the Supplier table
	supplier = Supplier(sid, s_name, s_contact_name, s_number, s_address)
	
	db.session.add(supplier)
	db.session.commit()
		
	return 'Supplier record added successfully'
	
	'''
	except IntegrityError:
		db.session.rollback()
		return "Account already exists.."
	except:
		db.session.rollback()
		return "Cannot register user..."
	'''

@app.route('/add_product_page')
def add_product_page():
	return render_template('add_product_page.html')
	
@app.route('/add_product', methods=['POST'])
def add_product():
	now=datetime.datetime.now()
	stk_date=now.strftime("%Y-%m-%d")
	from database import Product, Supplier, Supplier_product, Stock
	#try:
	
	p_category = request.form['category']
	p_sub_category = request.form['sub_category']
	p_name = request.form['name']
	p_price = request.form['price']
	gst = request.form['gst']
	product_base_margin = request.form['base_margin']
	p_sale_price = request.form['sale_price']
	sid = request.form['supplier']
	
	
	#similar technique used for generting supplier ID
	pids = Product.query.all()
	pid_list = [k.pid for k in pids]
	pid_list = [int(k[1:]) for k in pid_list]
	pid_list.sort( reverse = True)
	prefix = 'p'
	postfix = pid_list[0] + 1
	pid = prefix + str(postfix)
		
		
	#Create a product object to insert into the Product table
	#	def __init__(self, pid, p_category, p_sub_category, p_name, p_price, gst, product_base_margin, product_sale_price, supplier):
	
	#get supplier obj from database 
	supp = Supplier.query.filter_by(sid = sid).first()
	product = Product(pid, p_category, p_sub_category, p_name, p_price,gst,product_base_margin, p_sale_price, supp)
	supplier_product = Supplier_product( product, supp) #constructor for supplier_product needs product object and supplier object

	db.session.add(product)
	db.session.add(supplier_product)
	#def __init__(self, date, product,  stocks_left, supplier):
	prod = Product.query.filter_by(pid = pid).first()

	stock=Stock(prod,0,supp)
	db.session.add(stock)
	db.session.commit()
		
	return render_template('success_add_product.html')


@app.route('/returnpagetest')
def returnpagetest():
	#return page for testing purpose
	return render_template('returnpagetest.html')

@app.route('/fetch_suppliers')
def fetch_suppliers():
	from database import  Supplier
	lst = Supplier.query.all()
	supp = { k.s_name : k.sid for k in lst} #key value pair for name:id of supplier
	return json.dumps(supp) #ajax
	
@app.route('/fetch_categories')
def fetch_categories():
	from database import Product, Stock
	lst = Product.query.distinct(Product.p_category).all()
	category_lst = [k.p_category for k in lst] #list all category names
	return json.dumps(category_lst) 

@app.route('/fetch_sub_categories', methods=['GET'])
def fetch_sub_categories():
	category = request.args.get('val')
	
	from database import Product, Stock
	lst = Product.query.filter_by(p_category = category).distinct(Product.p_sub_category).all()
	category_lst = [k.p_sub_category for k in lst] #list all sub category names
	return json.dumps(category_lst)

@app.route('/fetch_products', methods=['GET'])
def fetch_products():
	category = request.args.get('val1')
	sub_category = request.args.get('val2')
	
	from database import Product, Stock
	lst = Product.query.filter_by(p_category = category).filter_by(p_sub_category = sub_category).all()
	category_lst = [[k.p_name,k.pid] for k in lst]
	return json.dumps(category_lst)

# @app.route('/fetch_supplier', methods=['GET'])
# def fetch_supplier():
# 	category = request.args.get('val1')
# 	sub_category = request.args.get('val2')
# 	product = request.args.get('val3')
# 	from database import Product, Stock, Supplier
# 	lst = Product.query.filter_by(p_category = category).filter_by(p_sub_category = sub_category).filter_by(p_name = sub_category).with_entities(Product.pid).all()
# 	# category_lst = [[k.p_name,k.pid] for k in lst]
# 	search_pid=lst[0][0]
# 	lst = Stock.query.filter_by(pid=search_pid).all()
# 	supp_lst = [k.sid for k in lst]
# 	suppname_lst=[]
# 	for i in supp_lst:
# 		j=Supplier.query.filter_by(sid=i).with_entities(Supplier.s_name).all()[0][0]
# 		suppname_lst.append(j)
# 	#suppname_lst=['a','b']
# 	return json.dumps(suppname_lst)

@app.route('/get_bills')#, methods=['GET'])	
def get_bills():

	# still have to pass the query result list to a html page to display bill details
	# to know the products involved in the bill ....use next funtion
	
 	# start_year = request.form['start_year']
	# start_month=request.form['start_month']
	# start_day = request.form['start_day']
	# end_year = request.form['end_year']
	# end_month = request.form['end_month']
	# end_day = request.form['end_day']
	
	#request.form['year']
	start = date(year=2017,month=11,day=18) 
	end = date(year=2017,month=11,day=18)
	
	#dummy method...not used anywhere 
	from database import Bills
	
	bills = Bills.query.filter(Bills.bill_date <= end).filter(Bills.bill_date >= start).all()
	
	print(bills)
	return "success"

@app.route('/search_by_bill_id')
def search_by_bill_id():
	return render_template('search_by_bill_id.html')


@app.route('/get_details_of_bill', methods=['POST','GET'])		
def get_details_of_bill():	
	
	#Gets details of the bill, i.e its products and cost of each product and quantity
	
	bill_no = request.form['bill_id']
	
	from database import Transactions, Product, Bills
	
	#q = Transactions.query.join(Product).filter(and_(Product.pid = Transactions.pid,Transactions.bill_no == bill_no)).all()
	q= Transactions.query.join(Product).filter(Transactions.bill_no == bill_no).with_entities(Product, Transactions).all()
	#o/p:
	#[(<Product p3>,<Transaction 1>),(<Product p4>,<Transaction 2>)]
	#q[0][0].p_name ------------>'CrackDisk'
	
	
	b = Bills.query.filter_by(bill_no = bill_no).first()
	
	return render_template('bill_details_test.html', details = q, bill = b)

@app.route('/get_sales')#, methods=['GET'])		
def get_sales():

	from database import Transactions, Product, Bills
	
	
		
	#-------------------------------------------------------------------------------------------------------------
	#monthly
	sales = 30
	start_date = datetime.date.today() + datetime.timedelta(-sales)
	end_date = datetime.date.today()
	
	
	q = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= start_date).all()
	list_bill_no = [i.bill_no for i in q]
	
	
	n = Transactions.query.join(Product).filter(Transactions.bill_no.in_(list_bill_no)).with_entities(Transactions.pid,Product.p_name, func.sum(Transactions.quantity)).group_by(Transactions.pid, Product.p_name).all()
	# products = [i[0] for i in n]
	monthly = {i[0]: [i[1], i[2] ] for i in n}
	#op: { 'p3' : ['Vim',15], 'p2' : ['CrackJack',5]}
	pids = list(monthly)
	
	m = Product.query.filter(Product.pid.in_(pids)).with_entities(Product.pid, Product.p_price).all()
	m1 = {i[0]: i[1] for i in m}
	#op: {'p3' : 30, 'p2': 10}
	
	amount_list_per_day = [] #empty list for amount per day
	quantity_list_per_day = [] #empty list for quantity per day
	for i in range(30):
		date = datetime.date.today() + datetime.timedelta(-i)
		half = Bills.query.filter(Bills.bill_date == date) # store mid result...else it wil be too heavy for the backend
		bills = half.all()
		list_bill_no = [i.bill_no for i in bills]
		amt = half.with_entities(func.sum(Bills.bill_amt)).group_by(Bills.bill_date).first() #op:(1125,)
		if amt == None:
			amt = 0
		else:
			amt = amt[0]
		amount_list_per_day.append(amt)
		
		if len(list_bill_no) == 0:
			quantity_list_per_day.append(0)
		else:
			quantity = Transactions.query.filter(Transactions.bill_no.in_(list_bill_no)).with_entities(func.sum(Transactions.quantity)).group_by(Transactions.bill_no).all()
			total_q = 0
			for i in quantity:
				total_q += i[0]
			quantity_list_per_day.append(total_q)
		
	#yearly
	sales = 365
	start_date = datetime.date.today() + datetime.timedelta(-sales)
	end_date = datetime.date.today()
	
	
	q = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= start_date).all()
	list_bill_no = [i.bill_no for i in q] #get bill numbers in a list
	
	
	n = Transactions.query.join(Product).filter(Transactions.bill_no.in_(list_bill_no)).with_entities(Transactions.pid,Product.p_name, func.sum(Transactions.quantity)).group_by(Transactions.pid, Product.p_name).all()
	# products = [i[0] for i in n]
	yearly = {i[0]: [i[1], i[2] ] for i in n}
	
		
	pids = list(yearly) #get the list of keys...similar to dict.keys()
	
	m = Product.query.filter(Product.pid.in_(pids)).with_entities(Product.pid, Product.p_price).all()
	m2 = {i[0]: i[1] for i in m} #can use zip too for this
	#op: {'p3' : 30, 'p2': 10}
	
	amount_list_per_month = []
	quantity_list_per_month = []
	
	for i in range(12):
		j = i*30
		k = (i+1)*30
		end_date = datetime.date.today() + datetime.timedelta(-j)
		start_date = datetime.date.today() + datetime.timedelta(-k)
		half = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= start_date)
		#store mid result...used later for other purpose too		
		bills = half.all()
		list_bill_no = [i.bill_no for i in bills]
		amt = half.with_entities(func.sum(Bills.bill_amt)).group_by(Bills.bill_date).all() #op:(1125,)
		if len(amt) == 0: #if the query returns 0 bills
			amt_t = 0
		else:
			amt_t = 0
			for i in amt:
				amt_t += i[0]
		amount_list_per_month.append(amt_t)
		
		if len(list_bill_no) == 0:#if the query returns 0 bills
			quantity_list_per_month.append(0)
		else:
			quantity = Transactions.query.filter(Transactions.bill_no.in_(list_bill_no)).with_entities(func.sum(Transactions.quantity)).group_by(Transactions.bill_no).all()
			total_q = 0
			for i in quantity:
				total_q += i[0]
			quantity_list_per_month.append(total_q)
	
	
	#weekly
	sales = 7
	start_date = datetime.date.today() + datetime.timedelta(-sales)
	end_date = datetime.date.today()
	
	
	q = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= start_date).all()
	list_bill_no = [i.bill_no for i in q]
	
	
	n = Transactions.query.join(Product).filter(Transactions.bill_no.in_(list_bill_no)).with_entities(Transactions.pid,Product.p_name, func.sum(Transactions.quantity)).group_by(Transactions.pid, Product.p_name).all()
	# products = [i[0] for i in n]
	weekly = {i[0]: [i[1], i[2] ] for i in n}
	
	pids = list(weekly) #returns the keys()..like dict.keys()
	
	m = Product.query.filter(Product.pid.in_(pids)).with_entities(Product.pid, Product.p_price).all()
	m3 = {i[0]: i[1] for i in m}
	#op: {'p3' : 30, 'p2': 10}
	
	amount_list_per_day_weekly = []
	quantity_list_per_day_weekly = []
	for i in range(7):
		date = datetime.date.today() + datetime.timedelta(-i)
		half = Bills.query.filter(Bills.bill_date == date)#.all()
		bills = half.all()
		list_bill_no = [i.bill_no for i in bills]
		amt = half.with_entities(func.sum(Bills.bill_amt)).group_by(Bills.bill_date).first() #op:(1125,)
		if amt == None: #if there are no bills then it returns null...soo at that time amt is 0
			amt = 0
		else:
			amt = amt[0]
		amount_list_per_day_weekly.append(amt)
		
		if len(list_bill_no) == 0:
			quantity_list_per_day_weekly.append(0)
		else:
			quantity = Transactions.query.filter(Transactions.bill_no.in_(list_bill_no)).with_entities(func.sum(Transactions.quantity)).group_by(Transactions.bill_no).all()
			total_q = 0
			for i in quantity:
				total_q += i[0]
			quantity_list_per_day_weekly.append(total_q)
		
	
	
	#---------------------------------------------------------------------
	# pids = list(products)
	
	# m = Product.query.filter(Product.pid.in_(pids)).with_entities(Product.pid, Product.p_price).all()
	# m = {i[0]: i[1] for i in m}
	#op: {'p3' : 30, 'p2': 10}
	
	mid = Transactions.query.join(Product).filter(Transactions.bill_no.in_(list_bill_no))
	
	#to get sub_categories of the products by grouping so that it's passable to page and can be used in Pie chart 
	
	
	sub_categories = mid.with_entities(Product.p_sub_category, func.sum(Transactions.quantity)).group_by(Product.p_sub_category).all()
	categories = mid.with_entities(Product.p_category, func.sum(Transactions.quantity)).group_by(Product.p_category).all()
	
	#mid.with_entities(Product.p_category, func.sum(Transactions.quantity)).group_by(Product.p_category).all()
	return render_template('sales_summary.html',monthly = monthly, yearly = yearly , weekly= weekly, m1 = m1, m2 = m2, m3 = m3, amount_list_per_day = amount_list_per_day, quantity_list_per_day = quantity_list_per_day, quantity_list_per_month = quantity_list_per_month, amount_list_per_month = amount_list_per_month, end_date = end_date, amount_list_per_day_weekly=amount_list_per_day_weekly, quantity_list_per_day_weekly=quantity_list_per_day_weekly)#, start_date = start_date,end_date = end_date, categories = categories, sub_categories = sub_categories)

@app.route('/get_tax_details_to_file')#, methods=['GET'])
def get_tax_details_to_file():	
	from database import Bills, TaxesFiled
	file=False #to disable or enable the button
	overdue=False # to disable or enable the button
	last_filled = TaxesFiled.query.order_by(desc(TaxesFiled.id)).limit(1).first()
	last_filled_date = last_filled.end
	
	next_file_date=last_filled_date+datetime.timedelta(345)

	#Tax collected after the last filled date
	end_date = datetime.date.today() + datetime.timedelta(-1)
	today_date = datetime.date.today()
	
	if(end_date>next_file_date):
		file=True
	if(end_date>next_file_date+datetime.timedelta(20)):
		overdue=True

	#fetch bills between 2 dates
	bills = Bills.query.filter(Bills.bill_date <= today_date).filter(Bills.bill_date > last_filled_date).all()
	
	
	return render_template('details_of_tax.html',file=file,overdue=overdue,next_file_date = next_file_date,last_filled = last_filled, bills = bills, last_filled_date = last_filled_date)
	
@app.route('/update_password')
def update_password():
	return render_template('update_password.html')
	
@app.route('/file_taxes')#, methods=['GET'])
def file_taxes():
	from database import Bills, TaxesFiled
	today_date = datetime.date.today()

	get_last_tax = TaxesFiled.query.order_by(desc(TaxesFiled.id)).limit(1).first()
	get_last_filed_date = get_last_tax.end
	start_date = get_last_filed_date + datetime.timedelta(1)
	end_date = today_date+ datetime.timedelta(-1) #last date is yesterday and not today
	
	q = Bills.query.filter(Bills.bill_date <= end_date).filter(Bills.bill_date >= start_date).all()
	gst_list = [i.gst for i in q]
	total_gst = sum(gst_list)
	
	tax = TaxesFiled(start_date, end_date, total_gst)
	
	db.session.add(tax)
	db.session.commit()
	#add to database


	return render_template('success_tax.html')

@app.route('/add_user_page')
def add_user_page():
	#only admin can add other users
	if 'user' in session and session['user'] == 'Admin':
		return render_template('add_new_user_page.html')
	else: 
		return render_template('add_new_user_fail.html')

@app.route('/add_user_request', methods=['POST'])
def add_user_request():
	#only admin can add a new user
	if 'user' in session and session['user'] == 'Admin':
		from database import Admin
		username = request.form['username']
		password = request.form['password']
		
		new_user = Admin(username, password)#add new user
		db.session.add(new_user)
		db.session.commit()
		
		return "new user "+ username +"added Successfully"
		#success page
	else:
		return render_template('add_new_user_fail.html')

@app.route('/update_password', methods=['POST'])		
def update_passowrd():
	from database import Admin
	
	new_pwd = request.form['password1']
	username = session['user']
	
	ad = Admin.query.filter_by(username = username).first()
	ad.password = new_pwd 
	db.session.commit()
	return redirect(url_for('dashboard'))
		
if __name__ == "__main__":
    app.run()
