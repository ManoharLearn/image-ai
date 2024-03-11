import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import os

def home(request):
    image_data = None
    invoke_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/89848fb8-549f-41bb-88cb-95d6597044a4"
    fetch_url_format = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status/"
    headers = {
    "Authorization": "Bearer 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",
    "Accept": "application/json",
    }
    print('OK1')
    if request.method == 'POST':
        input_text = request.POST.get('textbox', '')
        print(input_text)
        payload = {
            "prompt": input_text,
            "negative_prompt": "beach",
            "sampler": "DPM",
            "seed": 0,
            "guidance_scale": 5,
            "inference_steps": 25
        }
        session = requests.Session()

        response = session.post(invoke_url, headers=headers, json=payload)
        print('OK2')
        while response.status_code == 202:
            request_id = response.headers.get("NVCF-REQID")
            fetch_url = fetch_url_format + request_id
            response = session.get(fetch_url, headers=headers)

        response.raise_for_status()
        if response.status_code == 200:
            image_data = response.json().get('b64_json', '')
        print('OK3')

    return render(request, 'myapp/home.html', {'image_data': image_data})
