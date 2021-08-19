import json
from RDS import ROParser
import logging
import os
from flask import jsonify, request, g, current_app
from werkzeug.exceptions import abort
from lib.Util import require_api_key, from_jsonld
from RDS import Util

logger = logging.getLogger()


@require_api_key
def index():
    req = request.json.get("metadata")

    depoResponse = g.osf.projects()
    return jsonify(
        [
            {"projectId": str(depo.id), "metadata": depo.metadata(jsonld=True)}
            for depo in depoResponse
        ]
    )


@require_api_key
def get(project_id):
    req = request.json.get("metadata")

    depoResponse = g.osf.project(project_id)

    return jsonify(depoResponse)


def osf(res):
    result = {}

    result["title"] = res["name"]
    result["category"] = res["osfcategory"]
    result["description"] = res["description"].replace("\n", " ")

    return result


@require_api_key
def post():
    try:
        req = request.get_json(force=True)
        metadata = req.get("metadata")

        doc = ROParser(json.load(metadata))
        kwargs = doc.getElement(doc.rootIdentifier, expand=True, clean=True)

        logger.debug("send kwargs: {}".format(kwargs))
        project = g.osf.create_project(**kwargs)
    except Exception as e:
        logger.error(e, exc_info=True)
        abort(500)

    return jsonify({"projectId": project.id, "metadata": project.metadata(jsonld=True)})


@require_api_key
def delete(project_id):
    if g.osf.project(project_id).delete():
        return "", 204

    abort(404)


@require_api_key
def patch(project_id):
    req = request.get_json(force=True, cache=True).get("metadata")

    try:
        req = from_jsonld(req)
    except Exception as e:
        logger.error(e, exc_info=True)

    project = g.osf.project(project_id)

    if project.update(req):
        return jsonify(project.metadata(jsonld=True))

    abort(500)


@require_api_key
def put(project_id):
    project = g.osf.project(project_id)
    project.public = True

    if project.update():
        project.create_doi()
        return True, 200

    abort(400)
