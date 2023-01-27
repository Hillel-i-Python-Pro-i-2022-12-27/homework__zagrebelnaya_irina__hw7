from flask import Flask, Response
from application.services.create_phone_book_table import create_phonebook_table
from application.services.db_connection import DBConnection
from webargs import fields
from webargs.flaskparser import use_args

app = Flask(__name__)


@app.route("/")
def hello_world():  # put application's code here
    return "Hello World!"


@app.route("/phones/get-all/")
def get_phone():
    with DBConnection() as connection:
        phones = connection.execute("""SELECT *  FROM phone_book;""").fetchall()
    return "<br>".join([f'{phone["id"]}: {phone["contact_name"]} - {phone["phone_value"]} ' for phone in phones])


@app.route("/phones/get/<int:id>")
def get_phone_by_id(id: int):
    with DBConnection() as connection:
        phone = connection.execute("SELECT *  FROM phone_book WHERE (id=:id)", {"id": id}).fetchone()
        if phone is not None:
            return f'{phone["id"]}: {phone["contact_name"]} - {phone["phone_value"]}'
        return f"There isn't phone id ={id}"


@app.route("/phones/set")
@use_args({"contact_name": fields.Str(required=True), "phone_value": fields.Str(required=True)}, location="query")
def set_phone(args):
    with DBConnection() as connection:
        with connection:
            connection.execute(
                "INSERT INTO phone_book (contact_name, phone_value)  VALUES (:contact_name, :phone_value);",
                {"contact_name": args["contact_name"], "phone_value": args["phone_value"]},
            )
    return "Phone number created!"


@app.route("/phones/delete/<int:id>")
def delete_phone(id: int):
    with DBConnection() as connection:
        with connection:
            phone = connection.execute("SELECT *  FROM phone_book WHERE (id=:id)", {"id": id}).fetchone()
            if phone is not None:
                connection.execute("DELETE  FROM phone_book WHERE (id=:id)", {"id": id})
            return f"There isn't phone id ={id}"
    return "Phone number deleted!"


@app.route("/phones/update/<int:id>")
@use_args({"contact_name": fields.Str(), "phone_value": fields.Str()}, location="query")
def update_phone(args, id: int):
    with DBConnection() as connection:
        with connection:
            phone = connection.execute("SELECT *  FROM phone_book WHERE (id=:id)", {"id": id}).fetchone()
            print(phone)
            if phone is None:
                return f"There isn't phone id ={id}"
            contact_name = args.get("contact_name")
            phone_value = args.get("phone_value")
            if contact_name is None and phone_value is None:
                return Response("Need to put at least one argument!", status=400)
            args_request = []
            if contact_name is not None:
                args_request.append("contact_name=:contact_name")
            if phone_value is not None:
                args_request.append("phone_value=:phone_value")

            args_out = ", ".join(args_request)

            connection.execute(
                "UPDATE phone_book " f"SET {args_out} " "WHERE id=:id;",
                {"id": id, "contact_name": contact_name, "phone_value": phone_value},
            )
    return "Phone updated!"


create_phonebook_table()
if __name__ == "__main__":
    app.run()
