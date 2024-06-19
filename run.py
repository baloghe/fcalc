import os
import sys

sys.path.append(os.path.dirname(__name__))

from calcapp import create_app

# create an app instance
app = create_app()
if __name__ == '__main__':
    app.run(debug=True)