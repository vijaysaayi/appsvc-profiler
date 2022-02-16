from flask import Flask

def create_app():
   # create a minimal app
   app = Flask(__name__)
   
   # simple hello world view
   @app.route('/')
   def hello():
      return 'Testing, Flask!'

   return app