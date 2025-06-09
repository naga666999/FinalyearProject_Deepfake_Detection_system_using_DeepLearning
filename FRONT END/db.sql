drop database if exists video_detection;
create database video_detection;
use video_detection;

create table users (
    id INT PRIMARY KEY AUTO_INCREMENT, 
    email VARCHAR(50), 
    password VARCHAR(50)
    );
