from kubernetes import client, config
from flask import Flask,request
from os import path
import yaml, random, string, json
import sys
import json
from pprint import pprint
# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()
v1 = client.BatchV1Api()
app = Flask(__name__)
# app.run(debug = True)

@app.route('/config', methods=['GET'])
def get_config():
    pods = []
    v11 = client.CoreV1Api()
    result = v11.list_pod_for_all_namespaces()
    # your code here
    for item in result.items:
        dict = {
            "name":item.metadata.name,
            "ip":item.status.pod_ip,
            "namespace":item.metadata.namespace,
            "node": item.spec.node_name,
            "status": item.status.phase
        }
        pods.append(dict)
    # your code here

    output = {"pods": pods}
    output = json.dumps(output)

    return output

@app.route('/img-classification/free',methods=['POST'])
def post_free():
    # your code here
    if request.is_json:
        body = request.get_json()
    else:
        body = request.get_data()
        body = body.decode('utf-8')
        body = json.loads(body)
        #print(body)
    body = getFreeJob()
    api_response = v1.create_namespaced_job(namespace="free-service", body=body)
    pprint(api_response)
    # dataset =  body["dataset"]
    # namespace = 'free-service'  # str | object name and auth scope, such as for teams and projects
    # configuration = client.Configuration()
    # api_client = client.BatchV1Api(client.ApiClient(configuration))
    # body = client.V1Job()  # V1Job |
    # pretty = 'true'  # str | If 'true', then the output is pretty printed. (optional)
    # apiResponse = api_client.create_namespaced_job(namespace, body)
    # pprint(api_response)

    return "success"
def getFreeJob():
    jobName = 'mp12-free'
    container = client.V1Container(
        name="mp12-free",
        image="mp12-docker",
        command=["python3", "classify.py", "DATASET=mnist", "TYPE=ff"])
    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"name": "mp12-free"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=4)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(generate_name=jobName),
        spec=spec)
    return job


@app.route('/img-classification/premium', methods=['POST'])
def post_premium():
    # your code here
    body = getPremiumJob()
    api_response = v1.create_namespaced_job(namespace="default", body=body)
    return "success"
def getPremiumJob():
    jobName = 'mp12-premium'
    container = client.V1Container(
        name="mp12-premium",
        image="mp12-docker",
        command=["python3", "classify.py", "DATASET=kmnist", "TYPE=cnn"])
    # Create and configure a spec section
    template = client.V1PodTemplateSpec(
        metadata=client.V1ObjectMeta(labels={"name": "mp12-premium"}),
        spec=client.V1PodSpec(restart_policy="Never", containers=[container]))
    # Create the specification of deployment
    spec = client.V1JobSpec(
        template=template,
        backoff_limit=2,
        parallelism=2)
    # Instantiate the job object
    job = client.V1Job(
        api_version="batch/v1",
        kind="Job",
        metadata=client.V1ObjectMeta(generate_name=jobName),
        spec=spec)
    return job

    
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)

