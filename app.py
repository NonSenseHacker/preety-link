from flask import Flask, session, request, render_template, redirect, url_for
from flask_mysqldb import MySQL
import json
import random
import string
import datetime
with open('config.json', 'r') as c:
	para = json.load(c)["cfgdata"]

app = Flask(__name__)

all = string.digits + string.ascii_uppercase + string.ascii_lowercase

# database config
app.config['MYSQL_HOST'] = para["host"]
app.config['MYSQL_USER'] = para['db-user']
app.config['MYSQL_PASSWORD'] = para['db-pass']
app.config['MYSQL_DB'] = para['db-name']
app.secret_key = para['con-key']
mydb = MySQL(app)
# cursor = mydb.connection.cursor()


def slug_gen():
	temp = random.sample(all, 10)
	nslug = "".join(temp)
	cursor = mydb.connection.cursor()
	cursor.execute('''SELECT file_url FROM multi_link''')
	file_slug = cursor.fetchall()
	file_slug = list(file_slug)
	fileslug = [item for t in file_slug for item in t]
	if nslug in fileslug:
		slug_gen()
	else:
		return nslug


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
	if "user" in session and session['user'] == para['user-name']:
		return redirect("dashboard")

	if request.method == 'POST':
		username = request.form.get("username")
		passwd = request.form.get("password")
		if username == para['user-name'] and passwd == para['user-pass']:
			# set the session variable
			session['user'] = username
			return redirect("dashboard")
		else:
			return render_template("login.html", title=para['app-name'], des=para['app-des'], page="Login", eror=True)
	else:
		return render_template("login.html", title=para['app-name'], des=para['app-des'], page="Login")


@app.route('/protected', methods=['GET', 'POST'])
def protected():
	if "user" in session and session['user'] == para['user-name']:
		if request.method == "POST":
			url1 = request.form.get("url1")
			url2 = request.form.get("url2")
			url3 = request.form.get("url3")
			url4 = request.form.get("url4")
			url5 = request.form.get("url5")
			ftitle = request.form.get("ftitle")
			fsize = request.form.get("fsize")
			fsunit = request.form.get("funit")
			cursor = mydb.connection.cursor()
			try:
				fname=ftitle.split(".")[0]
				fext=ftitle.split(".")[1]
			except:
				fname=ftitle
				fext=None
			slug=slug_gen()
			if slug== None:
				slug=slug_gen()
			dte=datetime.datetime.now()
			date=(f"{dte.year}-{dte.month}-{dte.day}")
			cursor.execute("""INSERT INTO multi_link (id, file_url, Date, file_name, file_ext, file_size, size_ext, Server_1, Server_2, Server_3, Server_4, Server_5) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", ("",slug, date, fname, fext, fsize, fsunit, url1, url2, url3, url4, url5,))
			mydb.connection.commit()
			view_url= json.dumps({"url":slug})
			session['view_url']=view_url
			return redirect(url_for('.view_link', view_url=view_url))

		else:
			return redirect("/dashboard")
	else:
		return redirect('login')
@app.route("/view-link")
def view_link():
	if "user" in session and session['user'] == para['user-name']:
		view_url = request.args['view_url']
		view_url = session['view_url'] 
		return render_template("view-link.html", view_url=json.loads(view_url), site_url=para["site_url"], title=para['app-name'], page=para['app-des'])
	else:
		return redirect('login')
	#  return render_template("login.html", title=para['app-name'], des=para['app-des'], page="Login", methods=['POST','GET'])


@app.route('/dashboard')
def dashboard():
	if "user" in session and session['user'] == para['user-name']:
		cursor = mydb.connection.cursor()
		cursor.execute(
			'''SELECT * FROM multi_link ORDER BY multi_link.id ASC''')
		all_data = cursor.fetchall()
		return render_template("links.html", title=para['app-name'], page="Dashboard", all_data=all_data)
	else:
		return redirect("login")


@app.route("/create-link")
def create_link():
	if "user" in session and session['user'] == para['user-name']:
		return render_template("create-link.html", title=para['app-name'], page="Dashboard")
	else:
		return redirect("login")


@app.route('/view/<string:page_url>')
def view_page(page_url):
	if "user" in session and session['user'] == para['user-name']:
		cursor = mydb.connection.cursor()
		cursor.execute(
			"SELECT * FROM multi_link WHERE file_url LIKE %s ", (page_url,))
		all_urls = cursor.fetchone()

		return render_template('view.html', title=para['app-name'], page="Share Your Link", uploader=para['uploader'], all_urls=all_urls, page_url=page_url)
	else:
		return redirect("login")

@app.route('/edit/<string:page_url>', methods=['GET','POST'])
def edit_page(page_url):
	if "user" in session and session['user'] == para['user-name']:
		if request.method=="POST":
			link1=request.form.get("link1")
			link2=request.form.get("link2")
			link3=request.form.get("link3")
			link4=request.form.get("link4")
			link5=request.form.get("link5")
			ftitle=request.form.get("ftitle")
			fsize=request.form.get("fsize")
			funit=request.form.get("funit")

			fname=ftitle.split(".")[0]
			fext=ftitle.split(".")[1]

			cursor=mydb.connection.cursor()
			cursor.execute("UPDATE multi_link SET file_name = %s, file_ext=%s, size_ext=%s, file_size=%s, Server_1=%s, Server_2=%s, Server_3=%s, Server_4=%s, Server_5=%s WHERE multi_link.file_url = %s",(fname, fext, funit, fsize, link1, link2, link3, link4, link5, page_url,))
			mydb.connection.commit()
			return redirect("/edit/" + page_url)
		else:
			cursor=mydb.connection.cursor()
			cursor.execute("SELECT * FROM multi_link WHERE file_url LIKE %s ", (page_url,))
			all_data = cursor.fetchone()
			return render_template('edit-link.html', title=para['app-name'], page="Share Your Link", page_url=page_url , all_data=all_data)
	else:
		return redirect("login")

@app.route("/links")
def links():
	if "user" in session and session['user'] == para['user-name']:
		cursor = mydb.connection.cursor()
		cursor.execute('''SELECT * FROM multi_link ORDER BY multi_link.id ASC''')
		all_data = cursor.fetchall()
		return render_template("links.html", title=para['app-name'], page="Manage Links", all_data=all_data)
	else:
		return redirect("login")

@app.route('/logout')
def logout():
	if "user" in session and session['user'] == para['user-name']:
		session.clear()
		return redirect(url_for('login'))
	else:
		return redirect("login")
	
@app.route('/del/<string:del_link>')
def delete_link(del_link):
	if "user" in session and session['user'] == para['user-name']:
		try:
			cursor = mydb.connection.cursor()
			cursor.execute("DELETE FROM `multi_link` WHERE `multi_link`.`file_url` = %s", (del_link,))
			mydb.connection.commit()
			cursor.close()
		except:
			return redirect("/dashboard")
		return render_template("delete.html")
	else:
		return redirect("/login")


		
	




if __name__ == ("__main__"):
	app.run(debug=True)
