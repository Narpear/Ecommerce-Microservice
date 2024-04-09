CREATE DATABASE ecommerce_microservices;
USE ecommerce_microservices;

CREATE TABLE user (
    name VARCHAR(255),
    email VARCHAR(255),
    password VARCHAR(255)
);

CREATE TABLE cart
(
    ID VARCHAR(255) NOT NULL PRIMARY KEY,
    order_details VARCHAR(1000)
);
