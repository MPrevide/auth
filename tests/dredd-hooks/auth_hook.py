import dredd_hooks as hooks
import json
import controller.CRUDController as crud
from database.flaskAlchemyInit import db
from database.flaskAlchemyInit import HTTPRequestError


@hooks.before("Auth > Session management > Create session")
@hooks.before("Auth > Known users manipulation > List known users")
def create_sample_users(transaction):
    user = {
        "name": "admin",
        "username": "admin",
        "service": "admin",
        "email": "admin@noemail.com",
        "profile": "admin"
    }
    requester = {
        "userid": 0,
        "username": "dredd"
    }

    user_id = 0

    try:
        results = crud.create_user(db.session, user, requester)
        user_id = results["user"]["id"]
        print(f"Results are: {results}")
    except HTTPRequestError as e:
        print(f"Error: {e.message}")

    user = {
        "name": "test",
        "username": "test",
        "service": "test",
        "email": "test@noemail.com",
        "profile": "user"
    }

    try:
        results = crud.create_user(db.session, user, requester)
        print(f"Results are: {results}")
    except HTTPRequestError as e:
        print(f"Error: {e.message}")
    return user_id


@hooks.before("Auth > Session management > Create session")
def change_user_password(transaction):
    body = json.loads(transaction['request']['body'])
    body['passwd'] = 'temppwd'
    transaction['request']['body'] = json.dumps(body)


@hooks.before("Auth > Individual user settings > Get user info")
@hooks.before("Auth > Individual user settings > Update user info")
@hooks.before("Auth > Individual user settings > Remove user")
def change_user_id(transaction):
    user_id = create_sample_users(transaction)
    transaction['fullPath'] = transaction['fullPath'].replace('1', f'{user_id}')


