import base64, json, requests, re, pathlib, os
from io import BytesIO
from PIL import Image
from datetime import datetime


url = 'http://127.0.0.1:7860'
t2i_url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'

def base64_to_image(base64_string, output_file):
    """
    Decode base64 to Image. You probably don't need it
    """
    image_bytes = base64.b64decode(base64_string)
    image_buffer = BytesIO(image_bytes)
    image = Image.open(image_buffer)
    path_out_file = pathlib.Path(output_file)
    image.save(path_out_file)
    print(f"Saved image as {image.format.lower()} file: {path_out_file}")
    print(image.info)

def makeJSON(p, np, s, w, h):
    """
    Make a JSON from the received data. You probably don't need it
    """
    return json.dumps({
    "prompt": p,
    "negative_prompt": np,
    "sampler": 'k_dpmpp_sde_ka',
    "seed": s,
    "steps": 25,
    "cfg_scale": 7,
    "width": w,
    "height": h
    })

def CheckConnectionToServer():
    """
    Check connection to SD api server:
    - returns True when: server responds
    - returns False when: server unavailable
    """
    print("Trying connect...")
    try:
        r = requests.get(f'{url}/app_id', auth=("sdweb","ssdd")) 
        if (r.status_code) == 200:
            print("Successful Response, connection established")
            return True
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] Connection error: server unavailable")
        return False

def txt2img(prompt, negative_p, seed, width, height, directory):
    """
    Send a POST-request to Stable diffusion.
    Returns:
    - str path to generated image
    - int 503 when server is unavailable
    """
    if (CheckConnectionToServer()):
        print("Sending POST-request...")
        print(f"send req to {t2i_url}")
        r = requests.post(t2i_url, makeJSON(prompt, negative_p, seed, width, height), auth=("sdweb","ssdd"))
        print(f"server returns {r}")
        respond = r.json()
        if "images" in respond:
            match = re.search(r'"seed": (\d+)', respond['info'])
            if match:
                seed = match.group(1)
            print("Generation complete")
            date = datetime.now().strftime("%Y-%m-%d %H-%M")
            out_name = f"{str(seed)}_{date}.png"
            path = directory + out_name
            base64_to_image(respond['images'][0], path)
            return path
    else: return 503

def txt2img_TEST(directory):
    """
    This method is intended for testing, it contains a pre-generated image and does not respond to any form input (just specify the directory)
    """
    if (True):
        print("Sending POST-request...")
        print(f"send req to {t2i_url}")
        #r = requests.post(t2i_url, makeJSON(prompt, negative_p, seed, width, height), auth=("sdweb","ssdd"))
        print(f"server returns <Response [200]>")
        if True == True:
            with open(directory + "based.txt", 'r') as file:
                base64_data = file.read().strip()
            print("Generation complete")
            date = datetime.now().strftime("%Y-%m-%d %H-%M")
            out_name = "1659743771_2024-04-27 20-17.png"
            print(f"|{directory}{out_name}|")
            path = os.path.join(directory, out_name)
            base64_to_image(base64_data.encode('ascii'), path)
            return path