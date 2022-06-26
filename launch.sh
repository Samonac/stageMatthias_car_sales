python ./get-pip.py
python -m pip install --upgrade pip setuptools wheel
pip -r requirements.txt

start http://127.0.0.1:5000/
python ./carsale.py
sleep 1
echo "Thanks for watching ! Going to sleep now"