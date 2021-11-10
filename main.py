from website_Sql import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host ="localhost", port = int("5000") , debug = True)