import logging
import os
import time

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

FAVORITEANIMAL = ['monkey']

# --- Helpers that build all of the responses ---


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, intent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# --- Helper Functions ---


# --- Functions that control the bot's behavior ---


def zoo_chatter(intent_request):
    """
    Performs dialog management and chat with the end user.
    """
    session_attributes = intent_request['sessionAttributes'] if intent_request['sessionAttributes'] is not None else {}
    slots = intent_request['currentIntent']['slots']
    weather = slots['Weather']
    go_before = slots['GoBefore']
    animals = slots['Animals']
    favorite_animal = slots['FavoriteAnimal']
    eat_food = slots['EatFood']

    if (not weather) or (not go_before):
        return delegate(session_attributes, intent_request['currentIntent']['slots'])
    elif (not animals) and (go_before == 'Yes'):
    	return elicit_slot(
            session_attributes,
            intent_request['currentIntent']['name'],
            intent_request['currentIntent']['slots'],
            'Animals',
            {
                'contentType': 'PlainText',
                'content': 'What animals can you see in the zoo this time?'
            }
        )
    elif (not animals) and (go_before == 'No'):
    	return elicit_slot(
            session_attributes,
            intent_request['currentIntent']['name'],
            intent_request['currentIntent']['slots'],
            'Animals',
            {
                'contentType': 'PlainText',
                'content': 'So it\'s your first time to go to zoo, what animals can you see in the zoo?'
            }
        )
    elif (not favorite_animal) and (animals == 'I don\'t know'):
        if session_attributes.has_key('animals_retry'):
        	# int() is needed because any parameter in session_attributes will be changed to string as transfered
            session_attributes['animals_retry'] = int(session_attributes['animals_retry'])
            logger.debug('session_attributes.animals_retry={}'.format(session_attributes['animals_retry']))
            print (session_attributes['animals_retry'] > 3)

        if (session_attributes.has_key('animals_retry')) and (session_attributes['animals_retry'] > 2):
            return close(
                session_attributes,
                'Fulfilled',
                {
                    'contentType': 'PlainText',
                    'content': 'You need to learn how to describe animals in English. See you.'
                }
            )
        elif session_attributes.has_key('animals_retry'):
            session_attributes['animals_retry'] += 1
        else:
            session_attributes['animals_retry'] = 1

    	if session_attributes.has_key('animals_retry'):
        	logger.debug('session_attributes.animals_retry={}'.format(session_attributes['animals_retry']))
        	print (session_attributes['animals_retry'] > 3)

        return elicit_slot(
            session_attributes,
            intent_request['currentIntent']['name'],
            intent_request['currentIntent']['slots'],
            'Animals',
            {
                'contentType': 'PlainText',
                'content': 'Normally it could see monkeys, lions, elephants and pandas in the zoo. What animals can you see in the zoo?'
            }
        )
    elif not favorite_animal:
        return delegate(session_attributes, intent_request['currentIntent']['slots'])
    elif not eat_food:
        if favorite_animal in FAVORITEANIMAL:
        	content = 'My favorite animal is {0} too! Do you know what {0} like to eat?'.format(favorite_animal)
        else:
        	content = 'My favorite animal is monkey! Do you know what monkeys like to eat?'

        return elicit_slot(
            session_attributes,
            intent_request['currentIntent']['name'],
            intent_request['currentIntent']['slots'],
            'EatFood',
            {
                'contentType': 'PlainText',
                'content': content
            }
        )
    else:
        return close(
	        session_attributes,
	        'Fulfilled',
	        {
	            'contentType': 'PlainText',
	            'content': 'It\'s really nice to chat with you! See you.'
	        }
	    )


# --- Intents ---


def dispatch(intent_request):
    """
    Called when the user specifies an intent for this bot.
    """
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))

    intent_name = intent_request['currentIntent']['name']

    # Dispatch to your bot's intent handlers
    if intent_name == 'Zoo':
        return zoo_chatter(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# --- Main handler ---


def lambda_handler(event, context):
    """
    Route the incoming request based on intent.
    The JSON body of the request is provided in the event slot.
    """
    # By default, treat the user request as coming from the America/New_York time zone.
    os.environ['TZ'] = 'America/New_York'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)
