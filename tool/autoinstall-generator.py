import os
import argparse

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
output = ""
if os.getenv("SSH_KEY_PUB") != "":
    with open(os.getenv("SSH_KEY_PUB")) as secrets_file:
        secrets_array = secrets_file.readlines()
        output = template.render(
            hostname=os.getenv("DEVICEHOSTNAME"),
            name=os.getenv("USERNAME"),
            keyboard=os.getenv("KEYBOARDLAYOUT"),
            password="",
            timezone=os.getenv("TIMEZONE"),
            ssh_key=secrets_array
        )
elif os.getenv("PASSWORD") != "":
    output = template.render(
        hostname=os.getenv("DEVICEHOSTNAME"),
        name=os.getenv("USERNAME"),
        keyboard=os.getenv("KEYBOARDLAYOUT"),
        password=os.getenv("PASSWORD"),
        timezone=os.getenv("TIMEZONE"),
        ssh_key=os.getenv("SSH_KEY_PUB")
    )
print(output)
parser = argparse.ArgumentParser("Ubuntu autoinstall generator")
parser.add_argument("outputfile", help="The outputfile to create", type=str)
args = parser.parse_args()

if args.outputfile :
    with open(args.outputfile, "w") as text_file:
        text_file.write(output)