import argparse
import json
import random
from pathlib import Path

import requests


def create_password(passlen=8):
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    return "".join(random.sample(s, passlen))


class AutomatedBot:
    def __init__(
        self, data_path, number_of_users, max_posts_per_user, max_likes_per_user
    ):
        self.data_path = data_path
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.users_auth_data = None
        # self.number_of_posts = random.randint(0, max_posts_per_user)
        # self.number_of_likes = random.randint(0, max_likes_per_user)

    def __str__(self):
        return f"AutomatedBot({self.data_path}, {self.number_of_users}, {self.max_posts_per_user}, {self.max_likes_per_user})"

    def __call__(self, *args, **kwargs):
        self.create_users()

    def create_users(self):
        count = self.number_of_users
        users = []
        while count:
            bot_index = random.randint(0, 10000)
            username = f"bot{bot_index}"
            email = f"bot{bot_index}@gmail.com"
            password = create_password()
            user = self.signup(username, email, password)
            if user:
                if "status" in user:
                    if user["status"] == "success":
                        count -= 1
                        user = {
                            "username": username,
                            "email": email,
                            "password": password,
                        }
                        users.append(user)
        self.users_auth_data = {"auth_data": users}
        with open("auth_data.json", "w") as file:
            json.dump(self.users_auth_data, file)

    def signup(self, username, email, password):
        req_params = {
            "username": username,
            "email": email,
            "password1": password,
            "password2": password,
        }
        try:
            response = requests.post(
                "http://127.0.0.1:8000/api/v1/signup/", data=req_params
            )
            return response.json()

        except requests.exceptions.RequestException:
            return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated bot")

    parser.add_argument(
        "--config_path",
        help="path to bot config in json format",
        required=False,
        default=Path("bot_config.json"),
        type=Path,
    )
    parser.add_argument(
        "--data_path",
        help="path to store bot data",
        required=False,
        default=Path("bot_data/"),
        type=Path,
    )
    args = parser.parse_args()
    config_path = args.config_path
    data_path = args.data_path
    with open(config_path, "r", encoding="utf-8") as parameter_file:
        bot_config = json.load(parameter_file)
    bot = AutomatedBot(data_path, **bot_config)
    bot()
