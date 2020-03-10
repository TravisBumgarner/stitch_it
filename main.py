from app import routes
from app import app


def hello_flask(request):
    return routes.stitch(request)


if __name__ == '__main__':
    app.run()