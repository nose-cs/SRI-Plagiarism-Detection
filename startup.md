## Prerequisites

- Python   3.6 or higher

## Setup

1. **Create a virtual environment (optional but recommended):**
```
python3 -m venv myenv
source myenv/bin/activate
```

2. **Install dependencies:**
```
pip install -r requirements.txt
```

3. **Run django migrations:**
```
 python ./src/gui/manage.py migrate
```

## Running the Server

1. **Start the development server:**
```
python ./src/gui/manage.py runserver
```

2. **Visit the site:**
   Open your web browser and go to 
`http://127.0.0.1:8000/`
