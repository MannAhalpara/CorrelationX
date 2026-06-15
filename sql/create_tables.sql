CREATE TABLE stocks (
    ticker VARCHAR(20) PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    sector VARCHAR(50) NOT NULL
);

CREATE TABLE prices (
    ticker VARCHAR(20) NOT NULL,
    date DATE NOT NULL,
    open_price NUMERIC,
    high_price NUMERIC,
    low_price NUMERIC,
    close_price NUMERIC,
    volume BIGINT,

    PRIMARY KEY (ticker, date),

    CONSTRAINT fk_prices_stock
    FOREIGN KEY (ticker)
    REFERENCES stocks(ticker)
);

CREATE TABLE research_universe (
    ticker VARCHAR(20) PRIMARY KEY,

    CONSTRAINT fk_research_stock
    FOREIGN KEY (ticker)
    REFERENCES stocks(ticker)
);