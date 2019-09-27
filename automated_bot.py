import argparse
import json
import random
from pathlib import Path

from requests_api import create_like, create_post, get_posts_list, signin, signup


def generate_text(text_len=8):
    s = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()?"
    return "".join(random.sample(s, text_len))


class AutomatedBot:
    def __init__(
        self, data_path, number_of_users, max_posts_per_user, max_likes_per_user
    ):
        self.data_path = data_path
        self.number_of_users = number_of_users
        self.max_posts_per_user = max_posts_per_user
        self.max_likes_per_user = max_likes_per_user
        self.users_auth_data = None

    def __str__(self):
        return f"AutomatedBot({self.data_path}, {self.number_of_users}, {self.max_posts_per_user}, {self.max_likes_per_user})"

    def __call__(self, *args, **kwargs):
        self.create_users()
        self.login_users()
        self.create_posts()
        self.like_posts()
        with open("auth_data.json", "w") as file:
            json.dump(self.users_auth_data, file)

    def create_users(self):
        count = self.number_of_users
        users = []
        while count:
            bot_index = random.randint(0, 10000)
            username = f"bot{bot_index}"
            email = f"bot{bot_index}@gmail.com"
            password = generate_text()
            user = signup(username, email, password)
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

    def login_users(self):
        users_data = self.users_auth_data["auth_data"]
        for index, user in enumerate(users_data):
            response = signin(user["username"], user["password"])
            self.users_auth_data["auth_data"][index]["access_token"] = response[
                "access"
            ]

    def create_posts(self):
        users_data = self.users_auth_data["auth_data"]
        for user in users_data:
            for _ in range(random.randint(0, self.max_posts_per_user)):
                create_post(
                    user["access_token"],
                    user["username"],
                    generate_text(10),
                    generate_text(30),
                )

    def like_posts(self):
        users_data = self.users_auth_data["auth_data"]
        posts = get_posts_list()
        posts_id = [post["id"] for post in posts]
        for user in users_data:
            for _ in range(random.randint(0, self.max_likes_per_user)):
                post_id = random.choice(posts_id)
                create_like(user["access_token"], user["username"], post_id)


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
