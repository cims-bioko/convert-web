from pyxform.builder import create_survey_element_from_dict as json2survey
from pyxform.xls2json import parse_file_to_json
from pyxform.utils import has_external_choices, sheet_to_csv
from os.path import join  
from .fileio import write_zip


def xls2json(xls_path, instance_name="data"):
    warnings = []
    json = parse_file_to_json(xls_path, warnings=warnings)
    json['name'] = instance_name
    return (json, warnings)


def survey2xform(survey, xform_path, formatted=False):
    warnings = []
    survey.print_xform_to_file(xform_path, validate=False, 
            pretty_print=formatted, warnings=warnings, enketo=False)
    return warnings


def xls2zip(work_dir, xls_path, xform_name="form.xml",
        items_name="itemsets.csv", zip_name="form.zip", formatted=False):

    xform_path = join(work_dir, xform_name)
    items_path = join(work_dir, items_name)
    zip_path = join(work_dir, zip_name)

    (json, json_warnings) = xls2json(xls_path)
    survey = json2survey(json)
    xform_warnings = survey2xform(survey, xform_path, formatted=formatted)

    items_warnings = []
    if has_external_choices(json):
        items_warnings = _xls2itemset(xls_path, items_path)

    write_zip(zip_path, xform_path, items_path)

    return (zip_path, json_warnings + xform_warnings + items_warnings)


def xls2xform(work_dir, xls_path, xform_name="form.xml", formatted=False):

    xform_path = join(work_dir, xform_name)

    (json, json_warnings) = xls2json(xls_path)
    survey = json2survey(json)
    xform_warnings = survey2xform(survey, xform_path, formatted=formatted)

    return (xform_path, json_warnings + xform_warnings)


def xls2itemset(work_dir, xls_path, items_name="itemsets.csv"):

    items_path = join(work_dir, items_name)

    warnings = _xls2itemset(xls_path, items_path)

    return (items_path, warnings)


def _xls2itemset(xls_path, items_path):
    warnings = []
    if not sheet_to_csv(xls_path, items_path, "external_choices"):
        return warnings.append("Could not export itemsets.csv, perhaps the external choices"
                " sheet is missing.")
    return warnings

