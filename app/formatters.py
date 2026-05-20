from xml.etree.ElementTree import Element, SubElement, tostring

from flask import Response, jsonify, request


def build_response(payload, status=200, root="response"):
    response_format = request.args.get("format", "json").strip().lower()
    if response_format not in {"json", "xml"}:
        return jsonify({"error": "Unsupported format. Use json or xml."}), 400

    if response_format == "xml":
        xml_body = dict_to_xml(root, payload)
        return Response(xml_body, status=status, mimetype="application/xml")

    return jsonify(payload), status


def dict_to_xml(root_name, payload):
    root = Element(root_name)
    _append_xml(root, payload)
    return tostring(root, encoding="unicode")


def _append_xml(parent, value, item_name="item"):
    if isinstance(value, dict):
        for key, nested_value in value.items():
            child = SubElement(parent, str(key))
            _append_xml(child, nested_value)
        return

    if isinstance(value, list):
        for nested_value in value:
            child = SubElement(parent, item_name)
            _append_xml(child, nested_value)
        return

    parent.text = "" if value is None else str(value)

