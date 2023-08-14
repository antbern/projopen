# projopen

A small utility for quickly accessing predefined project folders. Uses [`rofi`](https://github.com/davatorium/rofi)
to perform the fuzzy selection.

## Requirements
Make sure you have [`rofi`](https://github.com/davatorium/rofi) and [`pyyaml`](https://pypi.org/project/PyYAML/) installed.
The project has been tested using `rofi` version `1.7.5` and `python 3.10`.

## Configuration
`projopen` looks for a configuration `yaml` file in the following places (in order of priority):
 - `$XDG_CONFIG_HOME/projopen/config.yaml` 
 - `$XDG_CONFIG_HOME/projopen.yaml` 
 - `~/.projopen.yaml`
 - `config.yaml` next to the script itself

A sample configuration:

```yaml
# A list of glob patterns to extract the options to send to rofi. Can be
# used for both directories and files if wanted.
folders:
  - "~/Projects/*"
  - "~/dev/projects/*"

# The commands to execute upon completion with Alt+{1,2,3} in rofi. ${path} is 
# replaced with the selected path returned by rofi.
commands:
  alt1:
    text: Terminal
    cmd: kitty --single-instance --directory ${path}
  alt2: 
    text: Neovim
    cmd: kitty --single-instance --directory ${path} tmux -c "nvim ."
  alt3: 
    text: File Explorer
    cmd: pcmanfm ${path}
```

