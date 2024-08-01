# City Information App

I have created a simple app that, when ran, asks for user input (city name) from the command line.
That input is then ran through simple validation and error checking. If the input is correct, for example the user
enters a valid city name, a short summary about the city along with the temperature will be saved in a file called
<city_name>.txt in the root folder of the app. There is a helper function that styles the summary.
If user input is invalid a simple error message will appear.

For running this app, I opted to use a virtual environment with a minimal set of dependencies specified in
the requirements.txt file - this should help with compatibility across various dev setups and should be
pretty straightforward to run.

Please create an .env file and use your own OPENWEATHER_API_KEY that you can get after you register
at https://openweathermap.org/api .


## Setup

1. **Create a virtual environment:**

    **Windows**:

    > python -m venv venv
    > venv\Scripts\activate

    **Linux**:

    > python -m venv venv
    > source venv/bin/activate

2. **Install dependencies:**

    > pip install -r requirements.txt

3. **Run the application:**

    > python main.py

4. **Run tests:**
    > pytest

## Configuration

Make sure to set up your `.env` file with the following environment variables:

-   `OPENWEATHER_API_KEY=<your_api_key>`
