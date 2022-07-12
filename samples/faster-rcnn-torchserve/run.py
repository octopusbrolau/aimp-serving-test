from __future__ import print_function

import io
import os
import time
import base64
import json
import time

import requests
import pickle
import onepanel.core.api
from onepanel.core.api.rest import ApiException
import onepanel.core.auth
from pprint import pprint

# If inside of Onepanel, get mounted service account token to use as API Key
access_token = onepanel.core.auth.get_access_token()

print('---ONEPANEL_API_URL----', os.getenv('ONEPANEL_API_URL'))
# Configure API key authorization: Bearer
configuration = onepanel.core.api.Configuration(
    host=os.getenv('ONEPANEL_API_URL'),
    api_key={
        'authorization': access_token
    }
)
configuration.api_key_prefix['authorization'] = 'Bearer'


# In[5]:


namespace = 'mp'
model_name = 'faster-rcnn-torchserve'


# In[6]:


# Get status, endpoint
with onepanel.core.api.ApiClient(configuration) as api_client:
    api_instance = onepanel.core.api.InferenceServiceApi(api_client)

    try:
        ready = False
        while not ready:
            api_response = api_instance.get_inference_service(namespace, model_name)
            ready = api_response.ready
            endpoint = api_response.predict_url
            print('---api_response.predict_url---', endpoint)
            time.sleep(1)
    except ApiException as e:
        print("Exception when calling InferenceServiceApi->get_inference_service_status: %s\n" % e)




headers = {
    'Content-Type': 'application/json',
}

import base64
image = open('./persons.jpg', 'rb') #open binary file in read mode
image_read = image.read()
image_64_encode = base64.b64encode(image_read)
bytes_array = image_64_encode.decode('utf-8')

data = {
    'instances': [
        {'data': bytes_array}
    ]
}



headers = {
    'onepanel-access-token': access_token,
    'Content-Type': 'application/json',
}

print('headers', headers)
print('endpoint', endpoint)

r = requests.post(endpoint, headers=headers, data=json.dumps(data))

result = r.json()
print(result)

