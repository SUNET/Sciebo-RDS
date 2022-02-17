
import copy
import json

from flask import session


def checkForEmpty(response):
    if response.status_code == 404:
        return []
    else:
        return parseAllResearch(json.loads(response.text))


def parsePropBack(prop):
    types = ["fileStorage", "metadata"]

    data = [
        {"portType": typ, "value": True}
        for typ in types
        if typ in prop["type"]
    ]

    customProp = [{"key": key, "value": value}
                  for key, value in prop.get("customProperties", {}).items()]

    if len(customProp) > 0:
        data.append({"portType": "customProperties", "value": customProp})

    return data


def parsePortBack(port):
    return {
        "port": port["port"],
        "properties": parsePropBack(port["properties"])
    }


def parseResearchBack(response):
    data = {
        "portIn": [parsePortBack(port) for port in response["portIn"]],
        "portOut": [parsePortBack(port) for port in response["portOut"]]
    }
    d = copy.deepcopy(response)
    d.update(data)
    return d


def parseCustomProp(customProp):
    return {val["key"]: val["value"] for val in customProp}


def parseProp(prop):
    propList = {"type": []}
    for val in prop:
        if val["portType"] == "customProperties":
            propList["customProperties"] = parseCustomProp(val["value"])
        else:
            propList["type"].append(val["portType"])
    return propList


def parsePort(port):
    return {
        "port": port["port"],
        "properties": parseProp(port["properties"])
    }


def parseResearch(response):
    data = {
        "portIn": [parsePort(port) for port in response["portIn"]],
        "portOut": [parsePort(port) for port in response["portOut"]]
    }
    d = copy.deepcopy(response)
    d.update(data)
    return d


def parseAllResearch(response):
    return [parseResearch(research) for research in response]


def parseAllResearchBack(response):
    return [parseResearchBack(research) for research in response]


def listContainsService(arr, service):
    for el in arr:
        try:
            if el["servicename"] == service["servicename"]:
                return True
        except Exception as e:
            pass

        try:
            if el["informations"]["servicename"] == service["informations"]["servicename"]:
                return True
        except Exception as e:
            pass

    return False


def removeDuplicates(response):
    withoutDuplicates = []
    for service in response:
        if not listContainsService(withoutDuplicates, service):
            withoutDuplicates.append(service)
    return withoutDuplicates

def applyFilters(response, helperSession=None):
    """Applies filters for services

    Args:
        response (list): Take a look into openapi spec for services properties.
        filters (list): List of Dicts. Expected fieldnames in dict: `name` for servicename to filter, `only` for domainnames and `except` same as `only`.
    """
    
    result = response
    
    if helperSession is not None:
        session = helperSession
    
    filters = session["oauth"]
    
    if "filters" in filters:
        filters = session["oauth"]["filters"]
        onlyFiltered = []
        
        if "only" in filters:
            for service in response:
                if service["servicename"] in filters["only"]:
                    onlyFiltered.append(service)
        else:
            onlyFiltered = response
        
        if "except" in filters:
            exceptFiltered = []
            for service in onlyFiltered:
                if service["servicename"] not in filters["except"]:
                    exceptFiltered.append(service)
        else:
            exceptFiltered = onlyFiltered
            
        result = exceptFiltered
    
    session["servicelist"] = result
    return result
    
def isServiceInLastServicelist(servicename, helperSession=None):
    if isinstance(servicename, dict):
        servicename = servicename["servicename"]
        
    if helperSession is not None:
        session = helperSession
    
    return "serviceList" in session and any([servicename == service["servicename"] for service in session["serviceList"]])
    
