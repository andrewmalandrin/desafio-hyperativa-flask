'''Routes module'''
import jwt
from app.data.repositories import CardsRepository, UsersRepository
from app.services.config import CONFIG
from app.services.auth import token_required
from app.services.validation import validate_email_and_pwd
from app.services.helpers import extract_batch_file_data
from flask import request
from main import app

log = app.logger

@app.route('/user/create', methods=['POST'])
def create_user():
    log.info("Beginning user creation process")
    data = request.json
    if (not data)\
    or (not data.get("name", None))\
    or (not data.get("email", None))\
    or (not data.get("password", None)):
        log.error("User details not provided")
        return {
            "message": "Provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    log.info("Starting email and password validation")
    is_valid = validate_email_and_pwd(data.get("email"), data.get("password"))
    if not is_valid:
        log.error("Invalid email or password")
        return {
            "message": "Invalid email or password",
            "data": None,
            "error": "Bad request"
        }
    log.info("Email and password verified")
    log.info("Inserting user into database")
    users_repo = UsersRepository()
    result = users_repo.create_user(
        name=data.get("name"), email=data.get("email"), password=data.get("password")
    )
    log.info(result)

    return {
        "message": result,
        "data": {"name": data.get("name"), "email": data.get("email")}
    }



@app.route('/user/auth', methods=['POST'])
def authenticate():
    log.info("Beginning authentication process")
    data = request.json
    if (not data) or (not data.get("email", None)) or (not data.get("password", None)):
        log.error("User details not provided")
        return {
            "message": "Provide user details",
            "data": None,
            "error": "Bad request"
        }, 400
    
    is_valid = validate_email_and_pwd(data.get("email"), data.get("password"))
    if not is_valid:
        log.error("Invalid email or password")
        return {
            "message": "Invalid email or password",
            "data": None,
            "error": "Bad request"
        }, 400
    users_repo = UsersRepository()
    user = users_repo.auth_user(data.get("email", None), data.get("password", None))
    if not user:
        log.error("Invalid email or password")
        return {
            "message": "Invalid email or password",
            "data": None,
            "error": "Bad request"
        }, 400
    log.info("User logged in")
    try:
        log.info("Creating token")
        token = jwt.encode(
            {"user_id": user.id},
            CONFIG['jwt']['secret'],
            algorithm="HS256"
        )
        log.info("Token created successfully")
        log.info("Authentication process done")

        return {
            "message": "Usuário autenticado",
            "data": {
                "token": token
            }
        }, 200
    except Exception as e:
        log.error(str(e))
        return {
            "message": f"Erro na geração do token: {e}",
            "data": None,
            "error": "Bad request"
        }, 500

@app.route('/user/get', methods=['GET'])
@token_required
def get_user(current_user):
    try:
        log.info("Beginning get process")
        user_id = request.args.get('user_id', None)
        if not user_id:
            log.error("Parameter user_id missing")
            return {
                "message": "Bad Request",
                "data": {},
                "error": "Parameter user_id missing"
            }, 400
        users_repo = UsersRepository()
        user = users_repo.get_by_id(user_id)
        log.info("Get process done")
        return {
            "message": "OK",
            "data": {
                "name": user.name,
                "email": user.email,
            }
        }, 200

    except Exception as e:
        log.error(str(e))
        return {
            "message": "Internal Server Error",
            "data": {},
            "error": str(e)
        }, 500

@app.route('/card/create', methods=['POST'])
@token_required
def create_card(current_user):
    try:
        log.info("Beginning card creation process")
        data = request.json
        cards_repo = CardsRepository()
        if not data.get("card_number"):
            log.error("Card number missing")
            return {
                "message": "Parameter card_number missing",
                "data": None,
                "error": "Bad request"
            }
        log.info("Verifying if card already exists")
        card = cards_repo.create_card(
            data.get("card_number")
        )
        log.info("Card creation process done")
        return {
            "message": "OK",
            "data": {
                "card_number": card.card_number
            }
        }, 200

    except Exception as e:
        log.error(str(e))
        return {
            "message": "Internal Server Error",
            "data": {},
            "error": str(e)
        }, 500

@app.route('/cards/create/batch', methods=['POST'])
@token_required
def create_cards(current_user):
    try:
        log.info("Beginning cards creation by batch file process")
        cards_repo = CardsRepository()
        txt_file = request.files.get('txt_file', None)
        if not txt_file:
            log.error("File txt_file missing")
            return {
                "message": "Bad Request",
                "data": {},
                "error": "File txt_file missing",
            }, 400

        file_data = extract_batch_file_data(txt_file)

        if (not file_data) or (not 'content' in file_data) or (not 'header' in file_data):
            log.error("Error in file layout")
            return {
                "message": "Error in file layout",
                "data": {},
                "error": "Error in file layout",
            }, 400
        response_cards = []
        for index, card in enumerate(file_data['content']):
            log.info("Processing card %s/%s", index+1, len(file_data['content']))
            try:
                result = cards_repo.create_card(
                    card_number=card.get("card_number"),
                    batch_number=file_data.get("header").get("batch_number"),
                    batch_date=file_data.get("header").get("batch_date"),
                    batch_name=file_data.get("header").get("batch_name"),
                    batch_position=card.get("num_in_batch")
                )
                response_cards.append(
                    {
                        "card_number": result.card_number,
                        "status": "created",
                        "batch_position": result.batch_position
                    }

                )
            except Exception as e:
                log.error(str(e))
                response_cards.append(
                    {
                        "card_number": card.get("card_number"),
                        "status": "error",
                        "error": str(e)
                    }
                )

        log.info("Cards creation by batch file process done")
        return {
            "message": "OK",
            "data": {
                "cards": response_cards
            }
        }, 200

    except Exception as e:
        log.error(str(e))
        return {
            "message": "Internal Server Error",
            "data": {},
            "error": str(e)
        }, 500


@app.route('/card/get', methods=['GET'])
@token_required
def get_card(current_user):
    try:
        args = request.args
        card_number= args['card_number']
        if not args.get("card_number", None):
            log.error("Card number missing")
            return {
                "message": "Parameter card_number missing",
                "data": None,
                "error": "Bad request"
            }, 400
        cards_repo = CardsRepository()
        card = cards_repo.get_card_by_card_number(card_number)
        if not card:
            log.info("Card not found")
            return {
                "data": {},
                "message": "Card not found",
            }, 200

        return {
            "data": {
                "batch_name": card.batch_name,
                "batch_number": card.batch_number,
                "batch_date": card.batch_date,
                "batch_row_id": card.batch_position,
                "card_number": card.card_number
            },
            "message": "OK",
        }, 200
    except Exception as e:
        log.error(str(e))
        return {
            "message": "Internal Server Error",
            "data": {},
            "error": str(e)
        }, 500
