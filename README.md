# Investment Portfolio Django

## Setup

### With `Docker`

- Build and run

```bash
docker-compose up -d --build
```

- Run database migrations

```bash
docker-compose exec backend python manage.py migrate
```

### Without `Docker`

#### API

- Install dependencies

```bash
pip install -r requirements.txt
```

- Run database migrations

```bash
python manage.py migrate
```

- Start the development server

```bash
python manage.py runserver
```

#### View (Dashboard)

- Install dependencies

```bash
cd view
npm install
```

- Start the development server

```bash
npm run dev
```

## Upload XLSX data

- Post the file to the `/upload/`.

```bash
curl -X POST http://localhost:8000/api/upload/ -F "file=@data/datos.xlsx"
```

## Usage

- API: http://localhost:8000/api/
- View (Dashboard): http://localhost:5173/

## Endpoints

- `POST /api/upload/`: Upload an XLSX file containing the investment data (It must have the same format as `data/datos.xlsx`).
- `GET /api/portfolios/<portfolio_id>/dates`: Get the available dates for a specific portfolio.
- `GET /api/portfolios/<portfolio_id>/evolution?start=<start_date>&end=<end_date>`: Get the evolution of the portfolio between the specified dates (Date format = "YYYY-MM-DD").
