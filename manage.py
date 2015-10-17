#!/usr/bin/env python
from flask.ext.script import Manager

from app import create_app
from extensions import socketio

app = create_app()
manager = Manager(app)


@manager.command
def runserver():
    socketio.run(app)


def main():
    manager.run()


if __name__ == '__main__':
    main()
