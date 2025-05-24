import os
import json
import firebase_admin
from firebase_admin import credentials
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def initialize_firebase():
    # Check if the script is running in a management command like makemigrations or migrate
    management_commands = ["makemigrations", "migrate", "collectstatic", "test", "runserver"]
    is_management_command = any(cmd in os.getenv("COMMAND", "") for cmd in management_commands)

    print('================================')
    print('Initializing Firebase...')
    print('================================')
    if not is_management_command:

        # Load Firebase credentials from .env
        firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")
        if firebase_credentials:
            try:
                firebase_credentials_dict = json.loads(firebase_credentials)

                # Initialize Firebase Admin SDK
                if not firebase_admin._apps:  # Prevent reinitialization
                    cred = credentials.Certificate(firebase_credentials_dict)
                    firebase_admin.initialize_app(cred)
                print('================================')
                print('Firebase Initialized Successfully')
                print('================================')
            except Exception as e:
                print(f"Error initializing Firebase: {e}")
        else:
            print("Firebase credentials not found in environment variables.")