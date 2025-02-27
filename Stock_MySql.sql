CREATE DATABASE STOCKMARKET;

USE STOCKMARKET;

CREATE TABLE tblstockmarket (
  Ticker text,
  close double,
  date text,
  high double,
  low double,
  month text,
  open double,
  volume bigint,
  filename text,
  stockyear bigint,
  stockmonth bigint,
  yearly_return double,
  monthly_return double,
  daily_return double,
  cumulative_return double,
  volatility double,
  stockID INT AUTO_INCREMENT PRIMARY KEY
);

CREATE TABLE tblsectorstocks (
  Ticker text,
  close double,
  date text,
  high double,
  low double,
  month text,
  open double,
  volume bigint,
  filename text,
  stockyear bigint,
  stockmonth bigint,
  yearly_return double,
  monthly_return double,
  daily_return double,
  cumulative_return double,
  volatility double,
  Company text,
  Sector text,
  stockID INT AUTO_INCREMENT PRIMARY KEY
);

select * from tblstockmarket;

select * from tblsectorstocks;
