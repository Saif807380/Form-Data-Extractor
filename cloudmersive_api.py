#!/usr/bin/env python
# coding: utf-8
import cloudmersive_ocr_api_client
from cloudmersive_ocr_api_client.rest import ApiException
import os

def extract(image_file):
    api_instance = cloudmersive_ocr_api_client.ImageOcrApi()
    api_instance.api_client.configuration.api_key = {}
    api_instance.api_client.configuration.api_key['Apikey'] = os.environ.get("API_KEY")
    try:
        # Converts an uploaded image in common formats such as JPEG, PNG into text via Optical Character Recognition.
        api_response = api_instance.image_ocr_post(image_file,recognition_mode = 'Normal',preprocessing = 'Auto')
        
        return api_response.text_result
    except ApiException as e:
        print("Exception when calling ImageOcrApi->image_ocr_post: %s\n" % e)
        return ''
