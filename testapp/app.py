import postgresql
import flask
import json
import initdb

app = flask.Flask(__name__)


def db_conn():
    return postgresql.open('pq://user:passw@db:5432/test_db')


def to_json(data):
    return json.dumps(data) + "\n"


def resp(code, data):
    return flask.Response(
        status=code,
        mimetype="application/json",
        response=to_json(data)
    )


def fields_validate():
    errors = []
    json = flask.request.get_json()
    if json is None:
        errors.append(
            "No JSON sent. Did you forget to set Content-Type header" +
            " to application/json?")
        return (None, errors)

    for field_name in ['colour', 'manufacturer']:
        if type(json.get(field_name)) is not str:
            errors.append(
                "Field '{}' is missing or is not a string".format(
          field_name))

    return (json, errors)


def affected_num_to_code(cnt):
    code = 200
    if cnt == 0:
        code = 404
    return code


@app.route('/')
def root():
    return flask.redirect('/api/cars')

# e.g. failed to parse json
@app.errorhandler(400)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(404)
def page_not_found(e):
    return resp(400, {})


@app.errorhandler(405)
def page_not_found(e):
    return resp(405, {})


@app.route('/api/cars/', methods=['GET'])
def get_cars():
    with db_conn() as db:
        tuples = db.query("SELECT * FROM cars")
        cars = []
        for (car_id, colour, year, manufacturer) in tuples:
            cars.append({"car_id": car_id, "colour": colour, "year": year, "manufacturer": manufacturer})
        return resp(200, {"cars": cars})


@app.route('/api/cars/<int:car_id>/', methods=['GET'])
def get_car(car_id):
    with db_conn() as db:
        sql = "SELECT * FROM cars WHERE car_id = " + str(car_id)
        tuples = db.query(sql)
        cars = []
        for (car_id, colour, year, manufacturer) in tuples:
            cars.append({"car_id": car_id, "colour": colour, "year": year, "manufacturer": manufacturer})
        return resp(200, {"cars": cars})


@app.route('/api/cars/', methods=['POST'])
def post_car():
    (json, errors) = fields_validate()
    if errors: 
        return resp(400, {"errors": errors})

    with db_conn() as db:
        insert = db.prepare(
            "INSERT INTO cars (car_id, colour, year, manufacturer) VALUES ($1, $2, $3, $4) " +
            "RETURNING car_id")
        [(car_id,)] = insert(json['car_id'], json['colour'], json['year'], json['manufacturer'])
        return resp(200, {"car_id": car_id})


@app.route('/api/cars/<int:car_id>/', methods=['DELETE'])
def delete_car(car_id):
    with db_conn() as db:
        delete = db.prepare("DELETE FROM cars WHERE car_id = $1")
        (_, cnt) = delete(car_id)
        return resp(affected_num_to_code(cnt), {})


@app.route('/api/cars/<int:car_id>/', methods=['PATCH'])
def patch_car(car_id):
    (json, errors) = fields_validate()
    if errors:  
        return resp(400, {"errors": errors})

    with db_conn() as db:
        update = db.prepare(
            "UPDATE cars SET colour = $2, year = $3, manufacturer = $4 WHERE car_id = $1")
        (_, cnt) = update(car_id, json['colour'], json['year'], json['manufacturer'])
        return resp(affected_num_to_code(cnt), {})


if __name__ == '__main__':
    app.debug = True  
    app.run()
