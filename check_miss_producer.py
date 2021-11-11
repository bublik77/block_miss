#!/usr/bin/env python3

import requests
import json
from time import sleep
from call import call, envirement_data
import os

try:
    envirement_data()
except:
    print("can't loda data")

try:
    cryptolions_producers = ["cryptolions1"]
    url = 'https://api.ultra.cryptolions.io/v1/chain/get_info' #'https://jungle3.cryptolions.io/v1/chain/get_info' #'http://wax.cryptolions.io/v1/chain/get_info'
    shedule_url = 'https://api.ultra.cryptolions.io/v1/chain/get_producer_schedule' #'https://jungle3.cryptolions.io/v1/chain/get_producer_schedule'
    resp_shed_url = requests.get(url=shedule_url)
    data_shed = resp_shed_url.json()
    prod_shedule_quee = dict()
    chain = "WAX"
    max_prod_count= len(data_shed['active']['producers'])
    print(data_shed, max_prod_count)
    for i in range(0,max_prod_count):
        #print(data_shed['active']['producers'][i]['producer_name'])
        if data_shed['active']['producers'][i]['producer_name'] not in prod_shedule_quee:
            prod_shedule_quee[i+1] = data_shed['active']['producers'][i]['producer_name']

    #print(prod_shedule_quee)
    resp = requests.get(url=url)
    data = resp.json()
    serverVersion = data['server_version_string']
    start_block_num = data['head_block_num']
    current_block_producer = data['head_block_producer']
    blocks_produced = 0
    first_run = 1
    netx_producer = prod_shedule_quee[(list(prod_shedule_quee.values()).index(current_block_producer)+1)+1]
    
    print("Starting from: ", start_block_num, current_block_producer)
    url = 'https://api.ultra.cryptolions.io/v1/chain/get_block' #'http://jungle3.cryptolions.io/v1/chain/get_block' #'https://bp.cryptolions.io/v1/chain/get_block' 

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
                # print(producer)
                # print(netx_producer)
                current_block_producer = producer
                if list(prod_shedule_quee.values()).index(current_block_producer) == max_prod_count -1:
                    netx_producer = prod_shedule_quee[1]
                else:
                    netx_producer = prod_shedule_quee[(list(prod_shedule_quee.values()).index(current_block_producer)+1)+1]
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
