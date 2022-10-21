import requests
import configparser
import os
import subprocess
import sys
import urllib.parse

api_conversations_url = "https://api2.frontapp.com/conversations/search/"
conversation_page_size = 100

api_update_conversation_url = "https://api2.frontapp.com/conversations/"

marked_for_deletion_tag_name = "marked-for-deletion"


def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def openLogFile():
    main_path = os.path.dirname(__file__)
    file_path = os.path.join(main_path, 'logs/logs.txt')
    return open(file_path, "w")


def openErrorFile():
    main_path = os.path.dirname(__file__)
    file_path = os.path.join(main_path, 'error/error.txt')
    return open(file_path, "w")


def openResultsFile():
    main_path = os.path.dirname(__file__)
    file_path = os.path.join(main_path, 'results/results.txt')
    return open(file_path, "w")


def writeLog(message):
    print(message)
    logFile.write(message + '\n')


def writeResult(message):
    resultFile.write(message + '\n')


def writeError(message):
    errorFile.write(message + '\n')


def setup_config():
    config_file = configparser.RawConfigParser()
    main_path = os.path.dirname(__file__)
    file_path = os.path.join(main_path, 'config/config.cfg')
    config_file.read(file_path)
    return config_file


def delete_marked_conversation(conversation_id):
    update_conversation_url = "https://api2.frontapp.com/conversations/" + conversation_id

    payload = {
        "status": "deleted"
    }
    requests.patch(update_conversation_url, headers=header, json=payload)


def find_conversations_with_input_and_tag_them(input, marked_for_deletion_tag_id):

    apiResponse = requests.get(api_conversations_url + input + "?limit=" + str(conversation_page_size), headers=header)
    conversations = apiResponse.json()

    mark_for_deletion(conversations, input, marked_for_deletion_tag_id, False)


    is_deleted_search_criteria = urllib.parse.quote(" is:deleted")
    apiResponse = requests.get(
        api_conversations_url + input + is_deleted_search_criteria + "?limit=" + str(conversation_page_size),
        headers=header)
    conversations = apiResponse.json()

    mark_for_deletion(conversations, input, marked_for_deletion_tag_id, True)


def is_marked_for_deletion_tag_exists(tags):
    found_marked_for_deletion = False
    for tag in tags:
        if tag['name'] == marked_for_deletion_tag_name:
            found_marked_for_deletion = True

    return found_marked_for_deletion


def mark_for_deletion(conversations, input, marked_for_deletion_tag_id, isDeletedCriteria):
    decodedInput = urllib.parse.unquote(input)
    conversationsFoundCounter = 0
    isDeletedLogString = " in trash inbox" if isDeletedCriteria else ""

    while True:
        for conversation in conversations['_results']:
            conversation_id = conversation['id']

            marked_for_deletion_tag_exists = is_marked_for_deletion_tag_exists(conversation['tags'])

            if not marked_for_deletion_tag_exists:
                tag_conversation_url = "https://api2.frontapp.com/conversations/" + conversation_id + "/tags"
                payload = {
                    "tag_ids": [marked_for_deletion_tag_id]
                }
                requests.post(tag_conversation_url, headers=header, json=payload)

                delete_marked_conversation(conversation_id)

                conversationsFoundCounter+=1

        if conversations["_total"] < conversation_page_size or conversations["_pagination"]["next"] is None:

            if conversationsFoundCounter > 0:
                writeLog('------FOUND total conversations'+isDeletedLogString+' for input '"" + decodedInput + '" : ' + str(conversationsFoundCounter))
                writeResult('------FOUND total conversations '+isDeletedLogString+' for input '"" + decodedInput + '" : ' + str(conversationsFoundCounter))

            if conversationsFoundCounter == 0:
                writeLog('------NOTHING FOUND '+isDeletedLogString+' for input '"" + decodedInput)
                writeError('------NOTHING FOUND '+isDeletedLogString+' for input '"" + decodedInput)

            break

        if conversationsFoundCounter > 0:
            writeLog( '------FOUND '+isDeletedLogString+' total conversations for input '"" + decodedInput + '" : ' + str(conversations["_total"]))
            writeResult('------FOUND '+isDeletedLogString+' total conversations for input '"" + decodedInput + '" : ' + str(conversations["_total"]))

        page_token = conversations["_pagination"]["next"]
        apiResponse = requests.get(page_token, headers=header)
        conversations = apiResponse.json()


def create_or_get_tag():
    create_tag_url = "https://api2.frontapp.com/tags"

    writeLog('Creating tag "' + marked_for_deletion_tag_name + '" ')
    payload = {
        "name": marked_for_deletion_tag_name,
        "highlight": "red"
    }

    response = requests.post(create_tag_url, headers=header, json=payload)
    if '_error' not in response.json():
        return response.json()['id']


try:
    install('requests')

    config = setup_config()
    logFile = openLogFile()
    errorFile = openErrorFile()
    resultFile = openResultsFile()

    writeLog('APP FRONT SCAN STARTED')

    if config.get('ApiSection', 'api.access.token').strip() == '':
        writeLog("No access token found")
        writeError("No access token found")

    header = {
        'Authorization': 'Bearer ' + config.get('ApiSection', 'api.access.token'),
        'accept': 'application/json'
    }

    main_path = os.path.dirname(__file__)
    file_path = os.path.join(main_path, 'input/input.txt')

    marked_for_deletion_tag_id = create_or_get_tag()
    with open(file_path) as f:
        for line in f:
            input = line.strip()

            find_conversations_with_input_and_tag_them(urllib.parse.quote(input), marked_for_deletion_tag_id)

    writeLog('APP FRONT SCAN COMPLETED')
    logFile.close()
    resultFile.close()
    errorFile.close()

except Exception as e:
    writeLog(e)
    writeError(e)
finally:
    logFile.close()
    resultFile.close()
    errorFile.close()
