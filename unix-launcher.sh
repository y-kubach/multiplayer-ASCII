P3=$(which python3)
P=$(which python)
if [ $P3 ]
then
    python3 -m venv venv
    source venv/bin/activate
    P3=$(which python3)
    pip install -r requirements.txt
    cd src
    sudo $P3 start.py
else
    if [ $P ]
    then
        python -m venv venv
        source venv/bin/activate
        P=$(which python3)
        pip install -r requirements.txt
        cd src
        sudo $P start.py
    else
        echo "No python or python3 installation found"
    fi
fi
