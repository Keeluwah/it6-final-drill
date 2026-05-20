# IT6 Final Hands-On Drill

This project is a Flask CRUD REST API for an `actors` table. It supports:

- Create, read, update, and delete operations
- Input validation and error handling
- JSON output by default
- XML output with the `format=xml` URI parameter
- Search and filtering with query parameters
- Automated tests with `pytest`

## Step-by-step setup

1. Create and enter the project folder.

```powershell
cd C:\Users\Keeluwah\Downloads\it6\handsondrill
```

2. Create a virtual environment.

```powershell
python -m venv .venv
```

3. Activate the virtual environment.

```powershell
.venv\Scripts\Activate.ps1
```

4. Install dependencies.

```powershell
pip install -r requirements.txt
```

5. Create the MySQL database and seed data.

Open MySQL and run:

```sql
SOURCE database/mysql_schema.sql;
```

6. Set your database connection string.

```powershell
$env:DATABASE_URL = "mysql://root:your_password@localhost:3306/it6_final_drill"
```

7. Run the Flask app.

```powershell
python app.py
```

8. Run the tests.

```powershell
python -m pytest -q tests -p no:cacheprovider
```

## Endpoints

- `GET /actors`
- `GET /actors/<id>`
- `POST /actors`
- `PUT /actors/<id>`
- `DELETE /actors/<id>`

## Query parameters

- `format=json`
- `format=xml`
- `first_name`
- `last_name`
- `nationality`
- `born_after`
- `born_before`
- `q`

## Example requests

Get all actors as JSON:

```powershell
curl "http://127.0.0.1:5000/actors"
```

Get all Filipino actors as XML:

```powershell
curl "http://127.0.0.1:5000/actors?nationality=Filipino&format=xml"
```

Create an actor:

```powershell
curl -X POST "http://127.0.0.1:5000/actors" `
  -H "Content-Type: application/json" `
  -d "{\"first_name\":\"Toshiro\",\"last_name\":\"Mifune\",\"birth_year\":1920,\"nationality\":\"Japanese\"}"
```

Update an actor:

```powershell
curl -X PUT "http://127.0.0.1:5000/actors/1" `
  -H "Content-Type: application/json" `
  -d "{\"nationality\":\"Filipino\"}"
```

Delete an actor:

```powershell
curl -X DELETE "http://127.0.0.1:5000/actors/1"
```

## Notes

- Runtime database: MySQL
- Test database: SQLite
- Seed data: 20+ actor records in [database/mysql_schema.sql](database/mysql_schema.sql)
