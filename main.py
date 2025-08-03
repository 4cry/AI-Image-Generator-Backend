import scratchattach as sa
import random
import time
from image_gen import generate_image
from encoder_decoder import *

project_path = ""

session = sa.login("username", "password") # enter credentials
cloud = session.connect_scratch_cloud("project_id") # enter your project id

n = 256-6 # we need 6 numbers for confirming to whom the packet belongs, and whether the packet is a client request or a server response

events = cloud.events()

@events.event
def on_set(activity):
    if str(list(activity.value)[0]) != "1":
        id = "".join(str(activity.value)[:3])
        value = "".join(str(activity.value)[3:])
        decoded = decode(int(value))
        username = decoded.split("|")[0]
        value = decoded.split("|")[1].strip()
        if username in open(f"{project_path}/banned_users.txt").read():
            print(f"User {username} is banned. Ignoring activity.") # server ignores the user, if they don't know they're banned they're less likely to try to find a bypass! (e.g. using an alt account)
            return
        bad_words = open(f"{project_path}/bad_words.txt").read().splitlines()
        if any(word in value.lower() for word in bad_words): # fill in the bad_words list to your heart's content
            print(f"User {username} used a banned word: {value}. Banning user.")
            with open(f"{project_path}/banned_users.txt", "a") as f:
                f.write(f"{username}\n") # automatic banning, zero tolerance policy lol, it's nice that you don't need to manually ban someone (though you can) and can sleep peacefully
            return
        print(f"User: {username}")
        print(f"Prompt: {value}")
        with open(f"{project_path}/logs.txt", "a") as f:
            f.write(f"{username}: {value}\n") # keeping logs is always useful
        if value == "None":
            print("No prompt provided.")
            return
        try:
            s = generate_image(prompt=value)
            if not s:
                print("Image generation failed.")
                return
            chunks = [s[i:i+n] for i in range(0, len(s), n)]
            var = str(list(id)[0])
            print(f"Variable #: {var}")
            chunk_idx = 1
            for chunk in chunks:
                chunk_idx_str = str(chunk_idx).zfill(len(str(len(chunks)))) # makes sure a chunk 'id' is always 3 digits long e.g. 001 not 1
                cloud.set_var(var, f"{1}{id}{chunk_idx_str}{chunk}")
                time.sleep(0.1)
                chunk_idx += 1
        except:
            print("Image generation failed.")
            return

@events.event
def on_ready():
   print("Event listener ready!")

events.start()
