import base64, json, requests, re, pathlib, os
from io import BytesIO
from PIL import Image
from datetime import datetime

url = 'http://127.0.0.1:7860'
t2i_url = 'http://127.0.0.1:7860/sdapi/v1/txt2img'

def __base64_to_image(base64_string, output_file) -> None:
    """
    Decode base64 to Image. You probably don't need it
    """
    image_bytes = base64.b64decode(base64_string)
    image_buffer = BytesIO(image_bytes)
    image = Image.open(image_buffer)
    path_out_file = pathlib.Path(output_file)
    image.save(path_out_file)

def __makeJSON(p, np, s, w, h) -> json:
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

def CheckConnectionToServer() -> bool:
    """
    Check connection to SD api server:
    - returns True when: server responds
    - returns False when: server unavailable
    """
    if __name__ == "__main__": 
        print("Trying connect...")
    try:
        r = requests.get(f'{url}/app_id', auth=("sdweb","ssdd")) 
        if (r.status_code) == 200:
            if __name__ == "__main__": 
                print("Successful Response, connection established")
            return True
    except requests.exceptions.RequestException as e:
        if __name__ == "__main__": 
            print(f"[{datetime.now()}] Connection error: server unavailable")
        return False

def txt2img(prompt, negative_p, seed, width, height, directory, model: str) -> json:
    """
    Send a POST-request to Stable diffusion.\n
    Better using:
    -- generated = json.loads(SDGEN.txt2img(prompt, negative_prompt, seed, width, height, directory, model/hash: str))\n
    then you can just use generated['info']['prompt'] etc\n
    Returns:
    - json { 'info' & 'path' } to generated image
    - json error code when server is unavailable
    """
    if (CheckConnectionToServer()):
        if __name__ == "__main__": 
            print("Sending POST-request...")
            print(f"send req to {t2i_url}")
        switchModel(str(model))
        makedJSON = __makeJSON(prompt, negative_p, seed, width, height)
        r = requests.post(t2i_url, makedJSON, auth=("sdweb","ssdd"))
        respond = r.json()
        if "images" in respond:
            match = re.search(r'"seed": (\d+)', respond['info'])
            if match:
                seed = match.group(1)
            date = datetime.now().strftime("%Y-%m-%d %H-%M")
            out_name = f"{model}_{str(seed)}_{date}.png"
            print("Generation complete: " + out_name)
            path = directory + out_name
            __base64_to_image(respond['images'][0], path)
            forReturn = json.dumps({
            'info': json.loads(__makeJSON(prompt, negative_p, seed, width, height)),
            'path': path                
            })
            return forReturn
    else: return json.dumps({'error': 503})

def txt2img_TEST(directory, model) -> json:
    """
    This method is intended for testing, it contains
    a pre-generated image and does not respond to any form input (just specify the directory and model)
    """
    if (True):
        print("[test] Sending POST-request...")
        print(f"[test] send req to {t2i_url}")
        print(f"[test] server returns <Response [200]>")
        if True == True:
            print('[test] we think that all is ok, so there is yours loaded model '+ model.name)
            with open(directory + "based.txt", 'r') as file:
                base64_data = file.read().strip()
            date = datetime.now().strftime("%Y-%m-%d %H-%M")
            out_name = f"defaultmodel_{str(1659743771)}_{date}.png"
            print("Generation complete: " + out_name)
            print(f"|{directory}{out_name}|")
            path = os.path.join(directory, out_name)
            __base64_to_image(base64_data.encode('ascii'), path)
            forReturn = json.dumps({
            'info': {'prompt': "test image, no any promts here", 'seed': 1659743771},
            'path': path                
            })
            return forReturn
        
def getModelsList() -> json:
    """
    Get list of models, available for use right now
    Returns:
    - json {
    "title": "string",
    "model_name": "string",
    "hash": "string",
    "sha256": "string",
    "filename": "string",
    "config": "string"
    }
    - json {'error': int -> code}
    """
    if CheckConnectionToServer():
        try:
            r = requests.get(f'{url}/sdapi/v1/sd-models', auth=("sdweb","ssdd"))
            print(r.status_code)
            if (r.status_code) == 200:
                respond = r.json()
                return respond
        except Exception as e:
            print("Catched exception on getModelList")
            return json.dumps({'error': 503})
    else: return json.dumps({'error': 503})

def switchModel(modelName: str) -> None:
    """
    ok it may be ok, just print here 'model_name' or 'hash'\n
    returns smth but you dont need that i guess:
    {'result': code, 'desc': description}
    """
    if CheckConnectionToServer():
        try:
            opt = requests.get(url=f'{url}/sdapi/v1/options')
            opt_json = opt.json()
            opt_json['sd_model_checkpoint'] = f'{modelName}'
            requests.post(url=f'{url}/sdapi/v1/options', json=opt_json)
            return json.dumps({'result': 200, 'desc': f"Changed model to ['{modelName}']"})
        except Exception as e:
            return json.dumps({'result': 503, 'desc': e})
    else: return json.dumps({'result': 503, 'desc': 'Server unavailable'})

if __name__ == "__main__":
    #txt2img("","",-1,512,512,'../media/generated_images/')
    #print(getModelsList())
    switchModel('a074b8864e')