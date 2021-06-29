# Flask based app to get distance from MKAD

## Requirements

- Python 3.8
- IDE

## Set Up

- Create an virtual enviroment and make sure to run inside it
- Run `pip install -r requirements.txt` to install the dependencies

## Set Up environment variables (Linux)

Set up environment variable from root project directory
Set for development mode

```bash
export FLASK_ENV=development
export FLASK_APP=setup.py
```

## Run Test
```bash
pytest -vv
```

## Run

Run this command and access the web app at `localhost:5000`

```bash
flask run
```

## Run in docker
```bash
docker build -t geocode-flask:1.0 .
docker run --name flaskgeo -d -p 5000:5000 --env FLASK_APP=setup.py --env FLASK_ENV=production geocode-flask:1.0
```
Access `localhost:5000` and input the destination

## How to use
* Make sure the application running well using above instructions
* Access `http://localhost:5000`
* Type the destination and hit 'Get'
* The result will served in json format if valid, otherwise will return with several status code, list of status code
    - 0: location or destination not found
    - 1: resulting destination and origin distance
    - 2: distance between origin and destination not found, destination might too far from origin
    - 3: destination location is inside origin's area

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)