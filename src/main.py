"""This is the products-ecommerce service"""

import os
import psycopg2
import psycopg2.extras
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request bodies
class CreateProductRequest(BaseModel):
    name: str
    price: float
    description: str

# Database connection
def get_db():
    return psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        dbname=os.environ.get('DB_NAME', 'ecommerce'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'password'),
        port=5432,
    )

# Health check
@app.get('/health')
def health():
    return 'OK'

# Get all products
@app.get('/products')
def get_products():
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute('SELECT * FROM products')
            rows = cur.fetchall()
        conn.close()
        return [dict(r) for r in rows]
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail='Database error')

# Get single product
@app.get('/products/{product_id}')
def get_product(product_id: int):
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
            row = cur.fetchone()
        conn.close()
        if row is None:
            raise HTTPException(status_code=404, detail='Product not found')
        return dict(row)
    except HTTPException:
        raise
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail='Database error')

# Create product
@app.post('/products', status_code=201)
def create_product(body: CreateProductRequest):
    try:
        conn = get_db()
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                'INSERT INTO products (name, price, description) VALUES (%s, %s, %s) RETURNING *',
                (body.name, body.price, body.description)
            )
            row = cur.fetchone()
        conn.commit()
        conn.close()
        return dict(row)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=500, detail='Database error')

########################################################################
######################## DISCLAIMER ####################################
### For this part I used Claude Code to translate the code given by the professor in JS to Python ###