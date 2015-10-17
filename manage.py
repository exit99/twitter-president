#!/usr/bin/env python
from flask.ext.script import Manager

from app import create_app

app = create_app()
manager = Manager(app)


@manager.command
def runserver():
    app.run()


def main():
    manager.run()


if __name__ == '__main__':
    main()
