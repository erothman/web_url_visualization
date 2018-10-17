from flask import Flask
import json
from flask_jsonpify import jsonify

app = Flask(__name__)

full_data = [{}]

def getInput(fileName):
    with open(fileName) as f:
        data = json.load(f)
    return data

def processInput(data):
    print(json.dumps(data["CVE_Items"][0]["cve"], sort_keys=True))
    for i in data["CVE_Items"]:
        entry = {}
        entry["ID"] = i["cve"]["CVE_data_meta"]["ID"]
        if len(i["cve"]["problemtype"]["problemtype_data"]) > 0:
            if len(i["cve"]["problemtype"]["problemtype_data"][0]["description"]) > 0:
                entry["problem_type"] = i["cve"]["problemtype"]["problemtype_data"][0]["description"][0]["value"]
        if len(i["cve"]["description"]["description_data"]) > 0:
            entry["description"] = i["cve"]["description"]["description_data"][0]["value"]
        if bool(i["impact"]):
            entry["accessVector"] = i["impact"]["baseMetricV2"]["cvssV2"]["accessVector"]
            entry["severity"] = i["impact"]["baseMetricV2"]["severity"]
            entry["impactScore"] = i["impact"]["baseMetricV2"]["impactScore"]
            entry["exploitabilityScore"] = i["impact"]["baseMetricV2"]["exploitabilityScore"]
        entry["publishedDate"] = i["publishedDate"]
        entry["lastModifiedDate"] = i["lastModifiedDate"]
        full_data.append(entry)
    print(full_data)

@app.route("/")
def hello():
    data = getInput('nvdcve-1.0-recent.json')
    processInput(data)
    return jsonify({'text':'Hellow World!', 'data': full_data})

if __name__ == '__main__':
     app.run(port=5002)
