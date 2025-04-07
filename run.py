from app import create_app

# this is the entry point to our app and what we run to start it.

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)