import wx
from wx.lib import sized_controls

from util.clipboardutil import on_get_uri_from_clipboard

WINDOW_SIZE_W = 900
WINDOW_SIZE_H = 500
NEXT_STEP = 800

class MemoDialog(sized_controls.SizedDialog):

    def __init__(self, *args, **kwargs):
        super(MemoDialog, self).__init__(*args, **kwargs)
        pane = self.GetContentsPane()
        self.pos = 0

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

        button_ok = wx.Button(pane_btns, wx.ID_OK, label='&OK')
        button_ok.Bind(wx.EVT_BUTTON, self.on_button)

        button_cancel = wx.Button(pane_btns, wx.ID_CANCEL, label='Cance&l')
        button_cancel.Bind(wx.EVT_BUTTON, self.on_button)

        add_info_btn_id = wx.NewId()
        add_info_btn = wx.Button(pane_btns, add_info_btn_id, label='&Add Info')
        add_info_btn.Bind(wx.EVT_BUTTON, self.add_info)

        append_btn_id = wx.NewId()
        append_btn = wx.Button(pane_btns, append_btn_id, label='A&ppend')
        append_btn.Bind(wx.EVT_BUTTON, self.append_from_clipboard)

        remove_space_btn_id = wx.NewId()
        remove_space_btn = wx.Button(pane_btns, remove_space_btn_id, label='&Trim')
        remove_space_btn.Bind(wx.EVT_BUTTON, self.remove_space)

        move_home_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.move_home, id=move_home_id)

        move_end_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.move_end, id=move_end_id)

        move_forward_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.move_forward, id=move_forward_id)

        move_backward_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.move_backward, id=move_backward_id)

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_ALT, ord('A'), add_info_btn_id),
            (wx.ACCEL_ALT, ord('B'), move_backward_id),
            (wx.ACCEL_ALT, ord('E'), move_end_id),
            (wx.ACCEL_ALT, ord('F'), move_forward_id),
            (wx.ACCEL_ALT, ord('H'), move_home_id),
            (wx.ACCEL_ALT, ord('L'), wx.ID_CANCEL),
            (wx.ACCEL_ALT, ord('O'), wx.ID_OK),
            (wx.ACCEL_ALT, ord('P'), append_btn_id),
            (wx.ACCEL_ALT, ord('T'), remove_space_btn_id),
        ])
        self.SetAcceleratorTable(accel_tbl)

        self.Fit()


    def on_button(self, event):
        if self.IsModal():
            self.EndModal(event.EventObject.Id)
        else:
            self.Close()


    def add_info(self, event):
        text = self.text.GetValue() + "\n\n---[Memo]---\n"
        self.text.SetValue(text)


    def append_from_clipboard(self, event):
        text = self.text.GetValue() + "\n"
        text += on_get_uri_from_clipboard()
        self.text.SetValue(text)
        self.text.SetInsertionPoint(len(text))
        self.text.SetFocus()

    def remove_space(self, evnet):
        text = self.text.GetValue()
        if len(text) == 0:
            return

        text = text.strip()
        lines = text.split('\n')

        result = []
        for line in lines:
            tmpLine = line.strip()
            if len(tmpLine) > 0:
                result.append(tmpLine)

        self.text.SetValue('\n'.join(result))


    def move_home(self, event):
        self.text.SetInsertionPoint(0)
        self.text.SetFocus()


    def move_end(self, event):
        text = self.text.GetValue()
        self.text.SetInsertionPoint(len(text))
        self.text.SetFocus()


    def move_forward(self, event):
        endpos = len(self.text.GetValue())
        self.pos =  self.pos + NEXT_STEP
        self.pos = self.pos if self.pos < endpos else endpos

        self.text.SetInsertionPoint(self.pos)
        self.text.SetFocus()


    def move_backward(self, event):
        self.pos = self.pos - NEXT_STEP
        self.pos = self.pos if self.pos >= 0 else 0

        self.text.SetInsertionPoint(self.pos)
        self.text.SetFocus()


    def GetValue(self):
        return self.text.GetValue()


    def SetValue(self, memo):
        return self.text.SetValue(memo)


    def GetTopic(self):
        return self.topic.GetValue()


    def SetTopic(self, topic):
        return self.topic.SetValue(topic)