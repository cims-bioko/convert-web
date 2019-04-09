from flask import Blueprint, request, Response, send_file
from flask_negotiate import consumes, produces
from tempfile import TemporaryDirectory
from os.path import isfile, join
from .api import xls2zip, xls2xform, xls2itemset
from .fileio import write_file


convert_api = Blueprint('convert_api', __name__)


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

