import http.client, urllib.request, urllib.parse, urllib.error, base64, json

# Replace the subscription_key string value with your valid subscription key.
subscription_key = '<your azure cognitive sub key>'

#this will also be different based on your cognitive api/location
uri_base = 'westus.api.cognitive.microsoft.com'

headers = {
    # Request headers.
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

params = urllib.parse.urlencode({
    # Request parameters. All of them are optional.
    'visualFeatures': 'Categories,Description,Color',
    'language': 'en',
})

#sample image url for testing
imgurl='https://upload.wikimedia.org/wikipedia/commons/1/12/Broadway_and_Times_Square_by_night.jpg'

def image(img):
    
    body = "{'url':'%s'}" % img
   
    # Execute the REST API call and get the response.
    conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/analyze?%s" % params, body, headers)
    response = conn.getresponse()
    data = response.read()

    # 'data' contains the JSON data. The following formats the JSON data for display.
    parsed = json.loads(data)
    conn.close()
    #return parsed
    return 'description: '+parsed['description']['captions'][0]['text'] + ', Confidence score of: '+str(parsed['description']['captions'][0]['confidence'])