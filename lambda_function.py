import logging
import traceback
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_intent_name, is_request_type
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

from fonAPI import FonApi

sb = SkillBuilder()
fon = FonApi('2aa34af87f48dac8664a57d6aab647d3c4547a828c74b4d0')

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@sb.request_handler(can_handle_func = is_request_type("LaunchRequest"))
def LaunchRequestHandler(handler_input):
    speech_text = "Welcome to Mobile Specs, you can say tell me about new iphone X"
    return handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Device Description", speech_text)).set_should_end_session(False).response


@sb.request_handler(can_handle_func = is_intent_name("GetDeviceDescriptionIntent"))
def GetDeviceDescriptionIntent(handler_input):
    device = getSlotValue('DEVICE', handler_input)
    print("\nSLOT DEVICE", device)
    try:
        phones = fon.getDevice(device = device, limit = 2)
        if type(phones) != list:
            speech_text = "I couldn't find anything for {}. Please try again!!".format(device)
            return handler_input.response_builder.speak(speech_text).set_should_end_session(True).response
        # print("PHONES", phones)
        for phone in phones:
            printDeviceDescription(phone)
            speech_text = ""
            output_card = ""

            speech_text += phone['DeviceName'] 
            if 'resolution' in phone:
                speech_text += " comes with a stunning resolution of " + phone['resolution'].split(',')[0].split('(')[0] 
                output_card += "Resolution: " + phone['resolution'] + "\n"
            if 'internal' in phone:
                speech_text += ". It has a huge internal memory of " + phone['internal'] + ". "
                output_card += "Internal Memory: " + phone['internal'] + "\n"
            if 'cpu' in phone:
                speech_text += "It is comprised of a powerful " + phone['cpu'] + " processor, "
                output_card += "CPU: " + phone['cpu'] + "\n"
            if 'usb' in phone:
                speech_text += "and it has a " + phone['usb'] + "."
                output_card += "USB: " + phone['usb'] + "\n"
            if 'battery_c' in phone:
                output_card += "Battery: " + phone['battery_c']
            if 'dimensions' in phone:
                output_card += "Dimensions: " + phone['dimensions'] + "\n"
            if 'display' in phone:
                output_card += "Display: " + phone['display'] + "\n"
            
            return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(phone['DeviceName'], output_card)).set_should_end_session(True).response

    except BaseException as e:
        traceback.print_exc()


@sb.request_handler(can_handle_func = lambda handler_input : 
                    is_intent_name("AMAZON.CancelIntent")(handler_input) or 
                    is_intent_name("AMAZON.StopIntent")(handler_input))
def CancelStopIntentHandler(handler_input):
    speech_text = "Good Bye!"
    return handler_input.response_builder.speak(speech_text).response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    print("\n")
    print("Encountered following exception: {}".format(exception))
    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    help_text = "You can say tell me description of new I phone X ... or exit. What can I help you with?"
    handler_input.response_builder.speak(help_text).ask(help_text)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    speech = "The Mobile Specs skill can't help you with that. You can ask me a simple description of your mobile phone"
    reprompt = ("You can tell me your device name. What can I help you with")
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


def getSlotValue(key, handler_input):
    slots = handler_input.request_envelope.request.intent.slots
    try: 
        if key in slots:
            return slots[key].value
    except BaseException as e:
        traceback.print_exc()
        return -1 

def getErrorOutput(handler_input):
    speech_text = "Something went wrong please try again. If the problem persists try with different device or brand name or try contacting the skill developer."
    handler_input.response_builder.speak(speech_text).set_should_end_session(True).response


def printDeviceDescription(phone):
    try: 
        print("Device:", phone['DeviceName'])
        print("Resolution:", phone['resolution'])
        print("Internal Memor", phone['internal']) 
        print("CPU:", phone['cpu'])
        print("USB:", phone['usb'])
        print("Battery:", phone['battery_c'])
        print("Dimensions:", phone['dimensions'])
        print("Display:", phone['display'])
        print()
    except BaseException as e:
        traceback.print_exc()

lambda_handler = sb.lambda_handler()

