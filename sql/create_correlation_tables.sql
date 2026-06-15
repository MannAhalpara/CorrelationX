CREATE TABLE pearson_correlations (
    ticker_1 VARCHAR(20),
    ticker_2 VARCHAR(20),
    correlation DOUBLE PRECISION,

    start_date DATE,
    end_date DATE,

    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (ticker_1, ticker_2)
);

CREATE TABLE spearman_correlations (
    ticker_1 VARCHAR(20),
    ticker_2 VARCHAR(20),
    correlation DOUBLE PRECISION,

    start_date DATE,
    end_date DATE,

    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (ticker_1, ticker_2)
);

CREATE TABLE kendall_correlations (
    ticker_1 VARCHAR(20),
    ticker_2 VARCHAR(20),
    correlation DOUBLE PRECISION,

    start_date DATE,
    end_date DATE,

    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (ticker_1, ticker_2)
);