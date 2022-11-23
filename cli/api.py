from random import random, randrange
import requests
from helpers import get_resource, error
import os
import json

base_url = "http://127.0.0.1:"


def get_port():
    home = os.getenv("HOME")
    with open(f"{home}/.port_connected_to", "r") as f:
        return f.readline().strip()


def random_income(i):
    return {
        "sender_index": round(random() * 1000),
        "sender_address": "akjgbwekjgbewgaewgwq4gwq3q",
        "amount": round(random() * 100),
        "index": i + 1,
    }


def random_outcome(i):
    return {
        "receiver_index": round(random() * 1000),
        "receiver_address": "akjgbwekjgbewgaewgwq4gwq3q",
        "amount": round(random() * 100),
        "index": i + 1,
    }


def random_node(i):
    return {"id": i, "label": "asjgbhwjegbewkjgbewg"}


def request(requestUrl):
    try:
        resp = requests.get(base_url + get_port() + requestUrl)
    except Exception as e:
        resp = []
        error(e)
        error("Request failed")
    return json.loads(resp.text)


def getIncomes():
    # return [random_income(i) for i in range(round(random()*100))]
    return request("/incomes")


def getOutcomes():
    # return [random_outcome(i) for i in range(round(random()*100))]
    return request("/outcomes")


def getTransactions():
    # return [random_income(i) for i in range(round(random()*100))]
    return request("/transactions")


def getProfileInfo():
    # return {
    #     "public_key": "ajfanbgajb29365bgk3b3947tr52bj",
    #     "index": 214,
    # }
    return request("/profile")


def getBalance():
    try:
        resp = requests.get(base_url + get_port() +"/balance")
    except Exception as e:
        error(e)
        error("Request failed")
        return 0
    return resp.text

def getNodes():
    # return [random_node(i) for i in range(100)]
    return request("/nodes")


def hello():
    try:
        resp = requests.get(base_url + get_port() +"/whoami")
    except Exception as e:
        error(e)
        error("Request failed")
        return 0
    return resp.text



def postTransaction(id, amount):
    body = {
        "id": id,
        "amount": amount,
    }
    response = requests.post(base_url +get_port()+ "/create_transaction", data=json.dumps(body))
    if response.status_code > 299:
        error("Request failed")
        return ""
    return "Posted successfully"
