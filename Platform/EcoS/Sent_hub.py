import requests, os
from dotenv import load_dotenv
from pathlib import Path


env_path = Path(__file__).resolve().parent.parent / 'EcoS.env'
load_dotenv(dotenv_path=env_path)

CLIENT_ID = "af5dea31-d9b8-4851-9119-f6e0ba4cf31d"
CLIENT_SECRET = "ylJNAKJBJ1ej8T9vIiEiKS8xPCXqVL1G"

print("🔐 CLIENT_ID =", CLIENT_ID)
print("🔐 CLIENT_SECRET =", CLIENT_SECRET)

def get_access_token():
    url = "https://services.sentinel-hub.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}  # <- correct content type
    payload = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, headers=headers, data=payload)  # <- use data=, not json=

    try:
        response.raise_for_status()
        print("✅ Access token obtained")
        return response.json().get("access_token")
    except Exception as e:
        print("❌ Failed to get token:", response.text)
        return None



evalscripts = {
        "true_color":"""
            //VERSION=3
            function setup(){
            return{
                input: ["B02", "B03", "B04", "dataMask"],
                output: {bands: 4}
            }
            }

            function evaluatePixel(sample){
            // Set gain for visualisation
            let gain = 2.5;
            // Return RGB
            return [sample.B04 * gain, sample.B03 * gain, sample.B02 * gain, sample.dataMask];
            }""",

        "ndwi": """
            //VERSION 3
            function setup() {
            return {
                input: ["B03", "B08", "dataMask"],
                output: { bands: 3 }
            }
            }

            const ramp = [
            [-0.8, 0x008000],
            [0, 0xFFFFFF],
            [0.8, 0x0000CC]
            ];

            let viz = new ColorRampVisualizer(ramp);

            function evaluatePixel(samples) {
            const val = index(samples.B03, samples.B08);
            let imgVals = viz.process(val);
            return imgVals.concat(samples.dataMask);
            }""",

        "ndmi": """//VERSION=3
            const moistureRamps = [
            [-0.8, 0x800000],
            [-0.24, 0xff0000],
            [-0.032, 0xffff00],
            [0.032, 0x00ffff],
            [0.24, 0x0000ff],
            [0.8, 0x000080]
            ];

            const viz = new ColorRampVisualizer(moistureRamps);

            function setup() {
            return {
                input: ["B8A", "B11", "dataMask"],
                output: { bands: 4 }
            };
            }

            function evaluatePixel(samples) {
            let val = index(samples.B8A, samples.B11);
            let imgVals = viz.process(val);
            return imgVals.concat(samples.dataMask);
            }""",

        "swir": """//VERSION=3
            function setup() {
            return {
                input: ["B12","B8A","B04", "dataMask"],
                output: { bands: 4 }
            };
            }

            function evaluatePixel(sample) {
            return [2.5 * sample.B12,2.5 * sample.B8A,2.5 * sample.B04, sample.dataMask ];
            }"""
    }
