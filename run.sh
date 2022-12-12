source ./venv/bin/activate
cd papapi/
uvicorn main:app --reload
deactivate