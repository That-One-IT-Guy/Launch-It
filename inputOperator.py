import mido
import threading
import renderingEngine

global suicide
suicide = False


def startUp(prefData, noteData, context):
    print("Looking for device...")
    inputController = connectInput(prefData)
    startHandle(inputController, prefData, noteData, context)
    return


def connectInput(prefData):
    alreadySaid = False
    input_ports = mido.get_input_names()
    while not input_ports:
        input_ports = mido.get_input_names()
        if input_ports and prefData["midi_input_port"] < 0 or prefData["midi_input_port"] >= len(input_ports) and alreadySaid == False:
            print("Invalid port index, we'll keep looking.")
            alreadySaid = True
    print("Found input: " + input_ports[prefData["midi_input_port"]])
    return mido.open_input(input_ports[prefData["midi_input_port"]])


def startHandle(inputController, prefData, noteData, context):
    global suicide
    if context[0] == True:
        suicide = True
        return
    thread = threading.Thread(target=mainHandler, args=(
        inputController, prefData, noteData, context,))
    thread.start()


def mainHandler(inputController, prefData, noteData, context):
    global suicide
    print("Now handling input requests.")
    while not suicide:
        for message in inputController.iter_pending():
            renderingEngine.mainLighting(prefData, noteData, context, message)