from app import create_app

# Create the application instance using the factory function
app = create_app()

if __name__ == "__main__":
    # Run the application in debug mode
    app.run(debug=True, port=8000, host='127.0.0.1')