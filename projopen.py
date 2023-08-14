#!/bin/env python3

from typing import Optional
import glob
import os
import yaml
import subprocess
from string import Template

# first found is used
config_locations = [
    "$XDG_CONFIG_HOME/projopen/config.yaml",
    "$XDG_CONFIG_HOME/projopen.yaml",
    "~/.projopen.yaml",
    "config.yml",
]

config: Optional[dict[str, str]] = None

for loc in config_locations:
    path = os.path.expanduser(os.path.expandvars(loc))

    if os.path.isfile(path):
        print(f"Loading config file {path}")
        try:
            with open(path, "r") as f:
                config = yaml.safe_load(f)
            break
        except Exception as e:
            print(f"Could not load config file {path}", e)

if config is None:
    print("Config is empty, exiting...")
    exit(1)

globs = config["folders"]


folders = sum([glob.glob(os.path.expanduser(path)) for path in globs], [])

# generate a string with the help from the config
message = ", ".join(
    f'{cmd.title()} => {config["commands"][cmd]["text"]}' for cmd in config["commands"]
)

rofi = subprocess.run(
    [
        "rofi",
        "-dmenu",
        "-p",
        "Project Folder",
        "-i",
        "-mesg",
        f"{message}",
    ],
    input="\n".join(folders),
    text=True,
    capture_output=True,
)

outpath = rofi.stdout.rstrip("\n")

# mapping from return code to name of command in config
cmds = {
    0: "alt1",
    10: "alt1",
    11: "alt2",
    12: "alt3",
}

if not rofi.returncode in cmds:
    print(f"Return code did not match any command: {rofi.returncode}")
    exit(1)

cmd = cmds[rofi.returncode]

if not cmd in config["commands"]:
    print(f"No command available for: {cmd}")
    exit(1)

cmdline = Template(config["commands"][cmd]["cmd"]).substitute(path=outpath)

# finally execute the command
subprocess.run(cmdline, shell=True)
