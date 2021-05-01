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
app.config['MYSQL_DATABASE_DB'] = 'oscarsData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Oscar Winners Male'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM male')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, Names=result)


@app.route('/view/<int:index>', methods=['GET'])
def record_view(index):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM male WHERE `index`=%s', index)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', award=result[0])


@app.route('/edit/<int:index>', methods=['GET'])
def form_edit_get(index):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM male WHERE `index`=%s', index)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', award=result[0])


@app.route('/edit/<int:index>', methods=['POST'])
def form_update_post(index):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('index'), request.form.get('year'), request.form.get('age'),
                 request.form.get('name'), request.form.get('movie'), index)
    sql_update_query = """UPDATE male t SET t.index = %s, t.year = %s, t.age = %s, t.name = %s, 
    t.movie = %s WHERE t.index = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/Names/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Oscar Awardee Form')


@app.route('/Names/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('index'), request.form.get('year'), request.form.get('age'),
                 request.form.get('name'), request.form.get('movie'))
    sql_insert_query = """INSERT INTO male (index,year,age,name,movie) VALUES (%s, %s,%s, %s,%s)"""
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/delete/<int:index>', methods=['POST'])
def form_delete_post(index):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM male WHERE `index` = %s """
    cursor.execute(sql_delete_query, index)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/Names', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM male')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/Names/<int:index>', methods=['GET'])
def api_retrieve(index) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM male WHERE `index`=%s', index)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/Names/<int:index>', methods=['PUT'])
def api_edit(index) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['index'], content['year'], content['age'],
                 content['name'], content['movie'], index)
    sql_update_query = """UPDATE male t SET t.index = %s, t.year = %s, t.age = %s, t.name = 
            %s, t.movie = %s WHERE t.index = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/Names/<int:index>', methods=['POST'])
def api_add(index) -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['index'], content['year'], content['age'],
                 content['name'], content['movie'], index)
    sql_insert_query = """INSERT INTO male (`index`,year,age,name,movie) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/Names/<int:index>', methods=['DELETE'])
def api_delete(index) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM male WHERE `index` = %s """
    cursor.execute(sql_delete_query, index)
    mysql.get_db().commit()
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
