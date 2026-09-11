import gc
import os
import scratchattach as sa
import time
from image_gen import generate_image
from encoder_decoder import *
from nsfw_detector import check_prompt

project_path = os.path.dirname(os.path.abspath(__file__))

_banned_users = set()
try:
    with open(os.path.join(project_path, "banned_users.txt")) as f:
        _banned_users = {line.strip() for line in f if line.strip()}
except FileNotFoundError:
    pass

scratch_user = "REDACTED_USER"
scratch_pass = "REDACTED_PASSWORD"
scratch_project = "1203338747"

session = sa.login(scratch_user, scratch_pass)
cloud = session.connect_scratch_cloud(scratch_project)

n = 250

events = cloud.events()

@events.event
def on_set(activity):
    if str(list(activity.value)[0]) != "1":
        id = "".join(str(activity.value)[:3])
        value = "".join(str(activity.value)[3:])
        decoded = decode(int(value))
        username = decoded.split("|")[0]
        value = decoded.split("|")[1].strip()
        if username in _banned_users:
            print(f"Banned user ignored: {username}")
            return
        result = check_prompt(value)
        print(f"NSFW check: {result['label']} ({result['confidence']:.2%}) | {username}: {value}")
        if result["label"] == "NSFW" and result["confidence"] > 0.85:
            print(f"Banning user: {username}")
            _banned_users.add(username)
            with open(os.path.join(project_path, "banned_users.txt"), "a") as f:
                f.write(f"{username}\n")
            return
        if value == "None":
            print("No prompt provided.")
            return
        with open(os.path.join(project_path, "logs.txt"), "a") as f:
            f.write(f"{username}: {value}\n")
        try:
            s = generate_image(prompt=value)
            if not s:
                print("Image generation failed.")
                return
            chunks = [s[i:i+n] for i in range(0, len(s), n)]
            var = str(list(id)[0])
            chunk_idx = 1
            for chunk in chunks:
                chunk_idx_str = str(chunk_idx).zfill(len(str(len(chunks))))
                cloud.set_var(var, f"{1}{id}{chunk_idx_str}{chunk}")
                time.sleep(0.1)
                chunk_idx += 1
        except Exception as e:
            print(f"Image generation failed: {e}")
        finally:
            gc.collect()

@events.event
def on_ready():
    print("Event listener ready!")

events.start()
