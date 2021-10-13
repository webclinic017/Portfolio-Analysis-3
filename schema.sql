-- Drop all tables before attempting to re-create them
DROP TABLE IF EXISTS portfolio;
DROP TABLE IF EXISTS user_profile;

-- Create the user_profile table
CREATE TABLE user_profile(
	id SERIAL PRIMARY KEY,
	username VARCHAR(20) NOT NULL,
	password VARCHAR(255) NOT NULL
);

-- Create the portfolio table
CREATE TABLE portfolio(
	id SERIAL PRIMARY KEY,
	data JSON NOT NULL,
	user_profile_id INT, FOREIGN KEY (user_profile_id) REFERENCES user_profile(id)
);