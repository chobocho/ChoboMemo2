import webbrowser
import os


def open_uri(uri):
    if "http" in uri[:5]:
        webbrowser.open_new(uri)
        return

    if not os.path.exists(uri):
        return

    chosenItem = '"' + uri + '"'
    print(chosenItem)
    os.startfile(chosenItem)
