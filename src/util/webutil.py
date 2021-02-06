import webbrowser
import os


def open_uri(uri):
    if len(uri) < 3:
        return

    if is_special_uri(uri):
        return

    if "http" in uri[:5]:
        webbrowser.open_new(uri)
        return

    if not os.path.exists(uri):
        print("Not exist ", uri)
        return


    chosenItem = '"' + uri + '"'
    print(chosenItem)
    os.startfile(chosenItem)


def is_special_uri(uri):
    """
    For cumstomize
    """
    if len(uri) == 0:
        return False
    return False
