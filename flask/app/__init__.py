from flask import Flask

# Initialize the app
app = Flask(__name__, instance_relative_config=True)

# Load the config file
if app.config["ENV"] == "production":
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

print("Environment is set to -", app.config['ENV'])

# Load the views
from app import views
from app import todo