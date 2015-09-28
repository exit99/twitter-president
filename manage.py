#!/usr/bin/env python
from flask.ext.script import Manager

from app import create_app
from constants import CANDIDATES
from extensions import socketio, db


app = create_app()
manager = Manager(app)


@manager.command
def runserver():
    socketio.run(app, use_reloader=False)


@manager.command
def syncdb():
    print("Initializing app...")
    db.init_app(app)
    print("Syncing...")
    db.create_all()
    print("Done!")


def main():
    manager.run()


if __name__ == '__main__':
    main()
