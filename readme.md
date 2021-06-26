# Flask based app to get distance from MKAD

Nothing.
Prediction Heart Disease

## Requirements

- Python 3.8
- IDE (I use VScode)

## Set Up

- Create an virtual enviroment and make sure to run inside it
- Run `pip install -r requirements.txt` to install the dependencies

## Set Up environment variables (Linux)

Set up environment variable from root project directory
Set for development mode

```bash
export FLASK_ENV=production
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
docker 
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)