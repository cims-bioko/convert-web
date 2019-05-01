from flask import Blueprint, request, Response, send_file, render_template, jsonify
from flask_negotiate import consumes, produces
from tempfile import TemporaryDirectory
from os.path import isfile, join
from .api import xls2zip, xls2xform, xls2itemset
from .fileio import write_file
from pyxform.errors import PyXFormError


convert_api = Blueprint('convert_api', __name__, template_folder='templates')


@convert_api.errorhandler(Exception)
def handle_general_errors(error):
    response = jsonify({'output': [{'error': True, 'message': str(error)}]})
    response.status_code = 500
    return response


@convert_api.errorhandler(PyXFormError)
def handle_pyxform_errors(error):
    response = jsonify({'output': [{'error': True, 'message': str(error)}]})
    response.status_code = 400
    return response


@convert_api.route("/", methods=['GET'])
def index_page():
    return render_template('index.html')


@convert_api.route("/", methods=['POST'])
@consumes("multipart/form-data")
def manual():
    with TemporaryDirectory() as temp_dir:
        upload = request.files['xlsform']
        xls_path = join(temp_dir, "form.xls")
        upload.save(xls_path)
        try:
            (zip_path, warnings) = xls2zip(temp_dir, xls_path)
            return send_file(zip_path,
                    as_attachment=True,
                    attachment_filename="converted.zip",
                    mimetype="application/zip")
        except PyXFormError as e:
            return render_template('index.html', error=str(e)), 400


@convert_api.route("/xls2zip", methods=['POST'])
@consumes("application/vnd.ms-excel", 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
@produces("application/zip")
def zip():
    with TemporaryDirectory() as temp_dir:
        xls_path = join(temp_dir, "form.xls")
        write_file(xls_path, request.get_data())
        (zip_path, warnings) = xls2zip(temp_dir, xls_path)
        return send_file(zip_path, mimetype="application/zip")


@convert_api.route("/xls2xform", methods=['POST'])
@consumes("application/vnd.ms-excel", 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
@produces("application/xml")
def xform():
    with TemporaryDirectory() as temp_dir:
        xls_path = join(temp_dir, "form.xls")
        write_file(xls_path, request.get_data())
        (xform_path, warnings) = xls2xform(temp_dir, xls_path)
        return send_file(xform_path, mimetype="application/xml")


@convert_api.route("/xls2itemset", methods=['POST'])
@consumes("application/vnd.ms-excel", 
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
@produces("text/csv")
def itemset():
    with TemporaryDirectory() as temp_dir:
        xls_path = join(temp_dir, "form.xls")
        write_file(xls_path, request.get_data())
        (items_path, warnings) = xls2itemset(temp_dir, xls_path)
        if not isfile(items_path):
            return Response(status=404)
        else:
            return send_file(items_path, mimetype="text/csv")

