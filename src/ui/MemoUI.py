import wx
from wx.lib import sized_controls

WINDOW_SIZE_W = 900
WINDOW_SIZE_H = 500

class MemoDialog(sized_controls.SizedDialog):

    def __init__(self, *args, **kwargs):
        super(MemoDialog, self).__init__(*args, **kwargs)
        pane = self.GetContentsPane()

        self.topic = wx.TextCtrl(pane, size=(WINDOW_SIZE_W,30))
        self.topic.SetValue("")

        self.text = wx.TextCtrl(pane, style = wx.TE_MULTILINE,size=(WINDOW_SIZE_W,WINDOW_SIZE_H))
        self.text.SetValue("")
        font = wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        self.text.SetFont(font)

        static_line = wx.StaticLine(pane, style=wx.LI_HORIZONTAL)
        static_line.SetSizerProps(border=('all', 0), expand=True)

        pane_btns = sized_controls.SizedPanel(pane)
        pane_btns.SetSizerType('horizontal')
        pane_btns.SetSizerProps(align='center')

        button_ok = wx.Button(pane_btns, wx.ID_OK, label='OK')
        button_ok.Bind(wx.EVT_BUTTON, self.on_button)

        button_cancel = wx.Button(pane_btns, wx.ID_CANCEL, label='Cancel')
        button_cancel.Bind(wx.EVT_BUTTON, self.on_button)

        add_info_btn_id = wx.NewId()
        add_info_btn = wx.Button(pane_btns, add_info_btn_id, label='Add Info')
        add_info_btn.Bind(wx.EVT_BUTTON, self.add_info)

        self.Fit()


    def on_button(self, event):
        if self.IsModal():
            self.EndModal(event.EventObject.Id)
        else:
            self.Close()


    def add_info(self, event):
        text = self.text.GetValue() + "\n\n---[Memo]---\n"
        self.text.SetValue(text)


    def GetValue(self):
        return self.text.GetValue()


    def SetValue(self, memo):
        return self.text.SetValue(memo)


    def GetTopic(self):
        return self.topic.GetValue()


    def SetTopic(self, topic):
        return self.topic.SetValue(topic)