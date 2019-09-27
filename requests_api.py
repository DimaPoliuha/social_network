import requests


def signup(username, email, password):
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


def signin(username, password):
    req_params = {"username": username, "password": password}
    try:
        response = requests.post("http://127.0.0.1:8000/api/v1/token/", data=req_params)
        return response.json()
    except requests.exceptions.RequestException:
        return None


def create_post(token, author, post_title, post_text):
    hed = {"Authorization": f"Bearer {token}"}
    req_params = {"author": author, "post_text": post_text, "post_title": post_title}
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/posts/create", data=req_params, headers=hed
        )
        return response.json()
    except requests.exceptions.RequestException:
        return None


def create_like(token, user, post_id):
    hed = {"Authorization": f"Bearer {token}"}
    req_params = {"user": user, "post_id": post_id}
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/v1/posts/like", data=req_params, headers=hed
        )
        return response.json()
    except requests.exceptions.RequestException:
        return None


def get_posts_list():
    try:
        response = requests.get("http://127.0.0.1:8000/api/v1/posts")
        return response.json()
    except requests.exceptions.RequestException:
        return None
