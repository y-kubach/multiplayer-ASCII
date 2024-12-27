# Multiplayer ASCII
### terminal, bombs, and multiplayer, what more could you want.

## Controls
- WASD - Movement
- F - Throw bomb
- L - Lay mine
- C - Place Wall

## Run game 
**Requires: Python 3 with pip and virtualenv (venv)**
###### Conda instead of virtualenv would also work but I don't know how to make the bash script work for both.

### Linux / WSL

- Run unix-launcher.sh (untested for mac).
```bash
$ ./unix-launcher.sh
```
##### Troubleshooting:
- Conda sometimes doesn't like our requirements. Try uninstalling it.
- Can fail if your python has a bajillion modules (try a relatively clean python install with virtual environments containing the modules)
  
### Windows (without VSCode)

- Run scr/start.py (probably will need administrator privileges).
```cmd
> pip install -r requirements.txt
> python3 scr/start.py
```
### Windows (with VSCode)

- Open VSCode and navigate to multiplayer-ascii.
- In the top left, select Terminal -> New Terminal.
- Install modules with:
```cmd
> pip install -r requirements.txt
```
- Select start.py, then press the run button.

### Mac

- ???

#### Manually Launching
- Run scr/start.py. You will need to be root in linux, which probably will fuck with your virtual environment. 


#### Credits
- Dalmador was here
- Sarius was here
- Falafel was here
