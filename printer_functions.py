from octorest import OctoRest
import config


def make_client(url, apikey):
    """Creates and returns an instance of the OctoRest client.

    Args:
        url - the url to the OctoPrint server
        apikey - the apikey from the OctoPrint server found in settings
    """
    try:
        client = OctoRest(url=url, apikey=apikey)
        return client
    except ConnectionError as ex:
        # Handle exception as you wish
        print(ex)


def get_printer_info(client):
    try:
        message = ""
        message += str(client.version) + "\n"
        message += str(client.job_info()) + "\n"
        printing = client.printer()['state']['flags']['printing']
        if printing:
            message += "Currently printing!\n"
        else:
            message += "Not currently printing...\n"
        return message
    except Exception as e:
        print(e)


def get_extruder_temp(client):
    try:
        return client.printer()["temperature"]["tool0"]["actual"]
    except:
        return 0.0


def get_bed_temp(client):
    try:
        return client.printer()["temperature"]["bed"]["actual"]
    except:
        return 0.0


def is_printing(client):
    return