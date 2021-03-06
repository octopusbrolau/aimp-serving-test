


from __future__ import print_function

import io
import os
import time
import base64
import json
import time
import numpy as np 
import requests
import pickle
import onepanel.core.api
from onepanel.core.api.rest import ApiException
import onepanel.core.auth
from pprint import pprint


# ## Get Onepanel Access Token for network requests

# In[2]:


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
model_name = 'efficientnet-v2-tfserving'


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


# In[8]:

with open('./img.pkl','rb') as f:
    img_data = pickle.load(f)

data = {
    'instances': img_data
}



headers = {
    'onepanel-access-token': access_token
}


r = requests.post(endpoint, headers=headers, json=data)

result = r.json()

print(result)

with open('imagenet1000_clsidx_to_labels.txt') as f:
    labels = eval(f.read())
    
print(labels[np.array(result['predictions'][0]).argmax()])




