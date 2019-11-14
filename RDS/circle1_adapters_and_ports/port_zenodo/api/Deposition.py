import os
import requests
import logging

logger = logging.getLogger('')

def search():
    return "deposition list", 200

def get(deposition_id):
    return "deposit {}".format(deposition_id), 200

def put(deposition_id):
    return "deposit update {}".format(deposition_id), 200

def post():
    return "add deposit", 200

def delete(deposition_id):
    return "delete deposit", 200
