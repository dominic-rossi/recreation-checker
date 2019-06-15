import datetime
import os
import time

import dotenv
import requests
from twilio.rest import Client

dotenv.load_dotenv()


def send_message(message):
    account_sid = os.environ.get('TWILIO_SID')
    auth_token = os.environ.get('TWILIO_TOKEN')
    twilio_phone = os.environ.get('TWILIO_PHONE')
    dest_phone = os.environ.get('DEST_PHONE')
    client = Client(account_sid, auth_token)

    response = client.messages.create(
        body=message,
        from_=twilio_phone,
        to=dest_phone
    )
    print(f'Got response from twilio: {response.sid}')


def check():
    trail_index = os.environ.get('TRAIL_INDEX')
    # Convert DATE_OF_INTEREST to a string with a specific format
    day_of_interest = os.environ.get('DATE_OF_INTEREST')
    day_of_interest = datetime.datetime.strptime(day_of_interest, '%Y-%m-%d')
    day_of_interest_param = day_of_interest.strftime('%Y-%m-%dT%H:%M:%SZ')

    # Create a url param which is the the first of the month of the 
    # DATE_OF_INTEREST
    search_start = day_of_interest.replace(day=1)
    search_start_param = search_start.strftime('%Y-%m-%dT%H:%M:%SZ')
    url_date = f'{search_start.month}/{search_start.day}/{search_start.year}'

    booking_url = f'https://www.recreation.gov/permits/233262/registration/detailed-availability?type=overnight-permit&date={url_date}'
    url = 'https://www.recreation.gov/api/permits/233262/availability/month'
    params = {
        'start_date': f'{search_start_param}',
        'commercial_acct': 'false',
        'is_lottery': 'false',
    }
    headers = {
        'Referer': f'https://www.recreation.gov/permits/233262/registration/detailed-availability?type=overnight-permit&date={url_date}',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:67.0) Gecko/20100101 Firefox/67.0'
    }
    messages_sent = 0

    while messages_sent < 5:
        response = requests.get(url, headers=headers, params=params)
        availability = response.json()['payload']['availability']
        trail = availability[trail_index]
        day_avilability = trail['date_availability'][day_of_interest_param]

        current_time = datetime.datetime.now()
        num_available = day_avilability["remaining"]
        total_permits = day_avilability["total"]
        if num_available > 0:
            print(f'{current_time}: Going to send message for {num_available} available at .')
            message = f'There are {num_available} permits available. {booking_url}'
            send_message(message)
            messages_sent += 1
            print(f'{current_time}: Sent message for {num_available}.')
        else:
            print(f'Avilability at {current_time}: {num_available}/{total_permits}')
            time.sleep(5*60)


if __name__ == '__main__':
    check()
