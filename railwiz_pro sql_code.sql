CREATE DATABASE railway_management;

USE railway_management;

CREATE TABLE trains (
    train_id INT PRIMARY KEY AUTO_INCREMENT,
    train_name VARCHAR(255),
    source VARCHAR(100),
    destination VARCHAR(100),
available_seats INT
);

CREATE TABLE passengers (
    passenger_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255),
    age INT,
    gender VARCHAR(10),
    phone VARCHAR(15)
);

CREATE TABLE tickets (
    ticket_id INT PRIMARY KEY AUTO_INCREMENT,
    passenger_id INT,
    train_id INT,
    booking_date DATE,
    seat_number INT,
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id),
FOREIGN KEY (train_id) REFERENCES trains(train_id));
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Rajdhani Express', 'Delhi', 'Mumbai', 100);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Shatabdi Express', 'Chennai', 'Bangalore', 120);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Duronto Express', 'Kolkata', 'Delhi', 150);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Garib Rath', 'Lucknow', 'Delhi', 80);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Jan Shatabdi', 'Mumbai', 'Goa', 75);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Howrah Express', 'Ahmedabad', 'Howrah', 110);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Tejas Express', 'Delhi', 'Chandigarh', 90);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Vande Bharat', 'Varanasi', 'Delhi', 160);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Intercity Express', 'Patna', 'Ranchi', 85);
INSERT INTO trains (train_name, source, destination, available_seats) VALUES ('Gatiman Express', 'Delhi', 'Agra', 200);
