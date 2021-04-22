from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'oscar_age_male'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Oscar Winners Male'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, Names=result)


@app.route('/view/<string:Name>', methods=['GET'])
def record_view(Name):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE Name=%s', Name)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', Awardee=result[0])


@app.route('/edit/<string:Name>', methods=['GET'])
def form_edit_get(Name):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE Name=%s', Name)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', Awardee=result[0])


@app.route('/edit/<string:Name>', methods=['POST'])
def form_update_post(Name):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('srno'), request.form.get('Year'), request.form.get('Age'),
                 request.form.get('Name'), request.form.get('Movie'), Name)
    sql_update_query = """UPDATE oscar_age_male t SET t.srno = %s, t.Year = %s, t.Age = %s, t.Name = 
    %s, t.Movie = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/Names/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar Awardee Form')


@app.route('/Names/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('srno'), request.form.get('Year'), request.form.get('Age'),
                 request.form.get('Name'), request.form.get('Movie'),)
    sql_insert_query = """INSERT INTO oscar_age_male (srno,Year,Age,Name,Movie) 
    VALUES (%s, %s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<string:Name>', methods=['POST'])
def form_delete_post(Name):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM oscar_age_male WHERE Name = %s """
    cursor.execute(sql_delete_query, Name)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/Names', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/Names/<string:Name>', methods=['GET'])
def api_retrieve(Name) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM oscar_age_male WHERE Name=%s', Name)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/Names/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/Names/<string:Name>', methods=['PUT'])
def api_edit(name) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/Names/<string:Name>', methods=['DELETE'])
def api_delete(name) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)