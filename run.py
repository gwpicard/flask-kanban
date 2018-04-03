from app.app import Kanban_app, init_db

if __name__ == '__main__':
    init_db() # initialise database
    Kanban_app.run(port=5000, host='localhost', debug=True)
