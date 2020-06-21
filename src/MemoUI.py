import wx
from wx.lib import sized_controls

class MemoDialog(sized_controls.SizedDialog):

    def __init__(self, *args, **kwargs):
        super(MemoDialog, self).__init__(*args, **kwargs)
        pane = self.GetContentsPane()

        self.topic = wx.TextCtrl(pane, size=(600,30))
        self.topic.SetValue("")

        self.text = wx.TextCtrl(pane, style = wx.TE_MULTILINE,size=(600,300))
        self.text.SetValue("")
        font = wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font)

        static_line = wx.StaticLine(pane, style=wx.LI_HORIZONTAL)
        static_line.SetSizerProps(border=(('all', 0)), expand=True)

        pane_btns = sized_controls.SizedPanel(pane)
        pane_btns.SetSizerType('horizontal')
        pane_btns.SetSizerProps(align='center')

        button_ok = wx.Button(pane_btns, wx.ID_OK, label='OK')
        button_ok.Bind(wx.EVT_BUTTON, self.on_button)

        button_ok = wx.Button(pane_btns, wx.ID_CANCEL, label='Cancel')
        button_ok.Bind(wx.EVT_BUTTON, self.on_button)

        self.Fit()


    def on_button(self, event):
        if self.IsModal():
            self.EndModal(event.EventObject.Id)
        else:
            self.Close()

    def GetValue(self):
        return self.text.GetValue()

    def SetValue(self, memo):
        return self.text.SetValue(memo)

    def GetTopic(self):
        return self.topic.GetValue()

    def SetTopic(self, topic):
        return self.topic.SetValue(topic)