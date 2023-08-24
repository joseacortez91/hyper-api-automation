DO $$ 
BEGIN
  CREATE TABLE IF NOT EXISTS Customers (
    customer_id CHARACTER VARYING(255) PRIMARY KEY,
    customer_name CHARACTER VARYING(255)
  );

  CREATE TABLE IF NOT EXISTS Managers (
    row_id SERIAL PRIMARY KEY,
    region CHARACTER VARYING(255),
    regional_manager CHARACTER VARYING(255)
  );

  CREATE TABLE IF NOT EXISTS Products (
    product_id CHARACTER VARYING(255) PRIMARY KEY,
    product_name CHARACTER VARYING(255),
    sub_category CHARACTER VARYING(255),
    category CHARACTER VARYING(255),
    segment CHARACTER VARYING(255)
  );

  CREATE TABLE IF NOT EXISTS Geography (
    postal_code CHARACTER VARYING(255) PRIMARY KEY,
    city CHARACTER VARYING(255),
    state CHARACTER VARYING(255),
    country CHARACTER VARYING(255),
    region CHARACTER VARYING(255)
  );

  CREATE TABLE IF NOT EXISTS Orders (
    order_id CHARACTER VARYING(255) PRIMARY KEY,
    customer_id CHARACTER VARYING(255) REFERENCES Customers(customer_id),
    postal_code CHARACTER VARYING(255) REFERENCES Geography(postal_code), 
    order_date DATE DEFAULT CURRENT_DATE NOT NULL
  );

  CREATE TABLE IF NOT EXISTS Items (
    item_id SERIAL PRIMARY KEY,
    order_id CHARACTER VARYING(255) REFERENCES Orders(order_id),
    product_id CHARACTER VARYING(255) REFERENCES Products(product_id),
    discount NUMERIC,
    profit NUMERIC,
    quantity INTEGER NOT NULL,
    sales NUMERIC NOT NULL
  );

  CREATE TABLE IF NOT EXISTS Shipments (
    shipment_id SERIAL PRIMARY KEY,
    order_id CHARACTER VARYING(255) REFERENCES Orders(order_id),
    ship_date DATE DEFAULT CURRENT_DATE NOT NULL,
    ship_mode CHARACTER VARYING(255)
    -- shipping_costs NUMERIC,
  );

  CREATE TABLE IF NOT EXISTS Returns (
    return_id SERIAL PRIMARY KEY,
    order_id CHARACTER VARYING(255) REFERENCES Orders(order_id),
    reason CHARACTER VARYING(255)
  );

  RAISE NOTICE 'INFO: tables created successfully!';
END $$;
