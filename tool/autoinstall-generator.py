import os

import jinja2
from dotenv import load_dotenv

load_dotenv()

TEMPLATE_FILE="autoinstall.yaml.jinja"
templateloader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateloader)
template = templateEnv.get_template(TEMPLATE_FILE)

# Password can be generated with `openssl passwd`
if os.getenv("DEVICEHOSTNAME") == "":
    print(".env file not set!")
    exit()

output = template.render(
    hostname=os.getenv("DEVICEHOSTNAME"),
    name=os.getenv("USERNAME"),
    keyboard=os.getenv("KEYBOARDLAYOUT"),
    password=os.getenv("PASSWORD"),
    timezone=os.getenv("TIMEZONE"),
    ssh_key=os.getenv("SSH_KEY_PUB")
)

print(output)