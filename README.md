# Personal-blog-website

## Intro

This is a final project of CS465/565P for bulding a personal blog website using Python and Flask!

Demo: https://yq-blogsite.herokuapp.com/

## Installation

1. Clone:
	
	git clone https://github.com/full-stack-final-project/Personal-blog-website.git
	
	cd Personal-blog-website

2. Install pipenv: pip install pipenv

3. Create and activate virtual env for this project:

	pipenv install
	
	pipenv shell

## Run

1. Generate database data using command: flask make-faker

2. Run the project using command: flask run

* running on http://127.0.0.1:5000/

## Other commands

1. flask init -- setting username & password & site_title for the website.

2. flask init-database -- clearing all the original data in the database and then creating new empty database.

3. flask routes -- showing the routes for the app

4. flask shell --- running a shell in the app context.

## Login information

Username: admin

Password: fullstack
