from lambda_function import lambda_handler
import logging

logging.basicConfig()

test_payload = {
  "messageVersion": "1.0",
  "invocationSource": "DialogCodeHook",
  "userId": "John",
  "sessionAttributes": {},
  "bot": {
    "name": "test",
    "alias": "$LATEST",
    "version": "$LATEST"
  },
  "outputDialogMode": "Text",
  "currentIntent": {
    "name": "Zoo",
    "slots": {
      "Weather": "Sunny",
      "GoBefore": "Yes",
      "Animals": "I don't know",
      "FavoriteAnimal": None,
      "EatFood": None
    },
    "confirmationStatus": "None"
  }
}

lambda_handler(test_payload, "")
