import wx

def on_get_uri_from_clipboard():
    uri_from_clipboard = wx.TextDataObject()
    uri = ""

    if wx.TheClipboard.Open():
        success = wx.TheClipboard.GetData(uri_from_clipboard)
        wx.TheClipboard.Close()
    if success:
        uri = uri_from_clipboard.GetText()

    return uri.strip()