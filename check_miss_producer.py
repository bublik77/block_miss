#!/usr/bin/env python3

import requests
import json
from time import sleep
from call import call, envirement_data
import os

chain = "WAX"
cryptolions_producers = ["cryptolions1"]
try:
    url_info = 'https://wax.cryptolions.io/v1/chain/get_info' #'https://jungle3.cryptolions.io/v1/chain/get_info' #'http://wax.cryptolions.io/v1/chain/get_info'
    shedule_url = 'https://wax.cryptolions.io/v1/chain/get_producer_schedule' #'https://jungle3.cryptolions.io/v1/chain/get_producer_schedule'
except Exception as ex:
    print(ex)

try:
    envirement_data()
except:
    print("can't loda data")

def bp_schedule_quee():
    resp_shed_url = requests.get(url=shedule_url)
    data_shed = resp_shed_url.json()
    prod_shedule_quee = dict()
    max_prod_count= len(data_shed['active']['producers'])
    #print(data_shed, max_prod_count)
    for i in range(0,max_prod_count):
        #print(data_shed['active']['producers'][i]['producer_name'])
        if data_shed['active']['producers'][i]['producer_name'] not in prod_shedule_quee:
            prod_shedule_quee[i+1] = data_shed['active']['producers'][i]['producer_name']
    return prod_shedule_quee

#print(len(bp_schedule_quee()))
try:
    resp = requests.get(url=url_info)
    data = resp.json()
    serverVersion = data['server_version_string']
    start_block_num = data['head_block_num']
    current_block_producer = data['head_block_producer']
    blocks_produced = 0
    first_run = 1
    netx_producer = bp_schedule_quee()[(list(bp_schedule_quee().values()).index(current_block_producer)+1)+1]
    
    print("Starting from: ", start_block_num, current_block_producer)
    url = 'https://wax.cryptolions.io/v1/chain/get_block' #'http://jungle3.cryptolions.io/v1/chain/get_block' #'https://bp.cryptolions.io/v1/chain/get_block' 

    headers = {
        'accept': "application/json",
        'content-type': "application/json"
        }
    while True:
        start_block_num = start_block_num +1
        data='{"block_num_or_id" : "'+str(start_block_num)+'"}'
        response = requests.request("POST", url, headers=headers, data=data)
        data=response.json()
        try:
            producer=data['producer']
        except KeyError:
    #        print (start_block_num, 'not produced yet, sleeping')
            sleep (10)
            start_block_num = start_block_num -1
            continue
        new_producers=data['new_producers']
        if current_block_producer == producer:
            blocks_produced = blocks_produced +1
        else:
            if producer == netx_producer:
                #print(producer)
                #print(netx_producer)
                current_block_producer = producer
                if list(bp_schedule_quee().values()).index(current_block_producer) == len(bp_schedule_quee()) -1:
                    netx_producer = bp_schedule_quee()[1]
                else:
                    netx_producer = bp_schedule_quee()[(list(bp_schedule_quee().values()).index(current_block_producer)+1)+1]
                #print(netx_producer,"new")
            elif netx_producer in cryptolions_producers:
                print(netx_producer, "miss round at", start_block_num)
                for i in os.environ["NUM_TO"].split(" "):
                    call(i, netx_producer, chain)
                netx_producer = producer
            else:
                print(netx_producer, "miss round at", start_block_num)
                netx_producer = producer
except Exception as ex:
    print(ex, "fin")
