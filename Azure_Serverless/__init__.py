import logging
import azure.functions as func
from . import visiontest
from twilio.rest import Client
import os


def main(myblob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: https://testfunctionappstorageak.blob.core.windows.net/{myblob.name}\n"
                 f"Blob Size: {myblob.length} bytes")
    
    imgurl=f"https://testfunctionappstorageak.blob.core.windows.net/{myblob.name}"
    #logging.info(visiontest.image(imgurl))
    deets=visiontest.image(imgurl)
    logging.info(deets)

    #Twilio message setup
    account=os.environ['TwilioAccount']
    token=os.environ['TwilioToken']
    client = Client(account, token)
 
    client.messages.create(to="+<To Phone #>", from_="+<From Phone #>", body="Motion Detected: "+deets)