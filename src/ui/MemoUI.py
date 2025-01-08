import wx
from wx.lib import sized_controls

from util.clipboardutil import on_get_uri_from_clipboard
from util.textutil import get_today

WINDOW_SIZE_W = 900
WINDOW_SIZE_H = 500
NEXT_STEP = 800


class MemoDialog(sized_controls.SizedDialog):
    def __init__(self, *args, **kwargs):
        super(MemoDialog, self).__init__(*args, **kwargs)
        panel = self.GetContentsPane()
        self.pos = 0

        self.topic = wx.TextCtrl(panel, size=(WINDOW_SIZE_W,30))
        self.topic.SetValue("")
        self.saved_topic = ""

        self.text = wx.TextCtrl(panel, style = wx.TE_MULTILINE,size=(WINDOW_SIZE_W,WINDOW_SIZE_H))
        self.text.SetValue("")
        self.saved_text = ""
        self.text.SetFont(wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL))

        static_line = wx.StaticLine(panel, style=wx.LI_HORIZONTAL)
        static_line.SetSizerProps(border=('all', 0), expand=True)

        panel_btns = sized_controls.SizedPanel(panel)
        panel_btns.SetSizerType('horizontal')
        panel_btns.SetSizerProps(align='center')

        button_ok = wx.Button(panel_btns, wx.ID_OK, label='&OK')
        button_ok.Bind(wx.EVT_BUTTON, self.on_button)

        button_cancel = wx.Button(panel_btns, wx.ID_CANCEL, label='Cance&l')
        button_cancel.Bind(wx.EVT_BUTTON, self.on_button)

        add_info_btn = wx.Button(panel_btns, (add_info_btn_id := wx.NewId()), label='&Add Info')
        add_info_btn.Bind(wx.EVT_BUTTON, self.add_info)

        append_btn = wx.Button(panel_btns, (append_btn_id := wx.NewId()), label='A&ppend')
        append_btn.Bind(wx.EVT_BUTTON, self.append_from_clipboard)

        remove_space_btn = wx.Button(panel_btns, (remove_space_btn_id := wx.NewId()), label='&Trim')
        remove_space_btn.Bind(wx.EVT_BUTTON, self.remove_space)

        undo_btn = wx.Button(panel_btns, (undo_btn_id := wx.NewId()), label='&Undo')
        undo_btn.Bind(wx.EVT_BUTTON, self.undo)

        key_map = [
            (wx.ACCEL_ALT, ord('A'), self.add_info, add_info_btn_id),  # Add Info
            (wx.ACCEL_ALT, ord('B'), self.move_backward, None),  # Move Backward
            (wx.ACCEL_ALT, ord('D'), self.insert_date, None),  # Move End
            (wx.ACCEL_ALT, ord('E'), self.move_end, None),  # Move End
            (wx.ACCEL_ALT, ord('F'), self.move_forward, None),  # Move Forward
            (wx.ACCEL_ALT, ord('H'), self.move_home, None), # Move Home
            (wx.ACCEL_ALT, ord('L'), self.on_button, wx.ID_CANCEL),  # Cancel
            (wx.ACCEL_ALT, ord('O'), self.on_button, wx.ID_OK),  # OK
            (wx.ACCEL_ALT, ord('P'), self.append_from_clipboard, append_btn_id),  # Append
            (wx.ACCEL_ALT, ord('S'), self.save_text, None),  # Save Text
            (wx.ACCEL_ALT, ord('T'), self.remove_space, remove_space_btn_id),  # Remove Space
            (wx.ACCEL_ALT, ord('U'), self.undo, undo_btn_id),  # Undo
            (wx.ACCEL_ALT, ord('1'), self.set_focus_topic, None),
            (wx.ACCEL_ALT, ord('2'), self.set_focus_memo, None),
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('A'), self.insert_arrow, None),  # Insert Arrow
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('B'), self.insert_black_box, None),  # Insert Black Box
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('C'), self.insert_check_box, None),  # Insert Check Box
            (wx.ACCEL_CTRL | wx.ACCEL_SHIFT, ord('W'), self.insert_white_box, None)  # Insert White Box
        ]

        accel_tbl = []
        for func_key, key, func, key_id in key_map:
            if key_id is None:
                key_id = wx.NewId()
            self.Bind(wx.EVT_MENU, func, id = key_id)
            accel_tbl.append((func_key, key, key_id))


        self.SetAcceleratorTable(wx.AcceleratorTable(accel_tbl))
        self.Fit()

    def set_focus_topic(self, event):
        self.topic.SetFocus()

    def set_focus_memo(self, event):
        self.text.SetFocus()

    def on_button(self, event):
        if self.IsModal():
            self.EndModal(event.EventObject.Id)
        else:
            self.Close()

    def add_info(self, event):
        text = f"{self.text.GetValue()}\n\n---[Memo]---\nCreate: {get_today()}\nUpdate:\n\n●○▶▷✿"
        self.text.SetValue(text)

    def append_from_clipboard(self, event):
        text = self.text.GetValue() + "\n"
        text += on_get_uri_from_clipboard()
        self.text.SetValue(text)
        self.text.SetInsertionPoint(len(text))
        self.text.SetFocus()

    def undo(self, event):
        self._undo()

    def _undo(self):
        self.topic.SetValue(self.saved_topic)
        self.text.SetValue(self.saved_text)

    def save_text(self, event):
        self.saved_topic = self.topic.GetValue()
        self.saved_text = self.text.GetValue()

    def remove_space(self, evnet):
        text = self.text.GetValue()
        if len(text) == 0:
            return

        text = text.strip()
        lines = text.split('\n')

        result = []
        for line in lines:
            tmp_line = line.strip()
            if len(tmp_line) > 0:
                result.append(tmp_line)

        self.text.SetValue('\n'.join(result))

    def move_home(self, event):
        self.text.SetInsertionPoint(0)
        self.text.SetFocus()

    def move_end(self, event):
        self.text.SetInsertionPointEnd()
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

    def insert_date(self, event):
        self.text.WriteText(get_today())

    def insert_string(self, str):
        pos = self.text.GetInsertionPoint()
        self.text.WriteText(str)
        self.text.SetInsertionPoint(pos + len(str))

    def insert_arrow(self, event):
        self.insert_string('→')

    def insert_check_box(self, event):
        self.insert_string('√')

    def insert_black_box(self, event):
        self.insert_string('■')

    def insert_white_box(self, event):
        self.insert_string('□')

    def GetValue(self):
        return self.text.GetValue()

    def SetValue(self, memo):
        self.saved_text = memo
        return self.text.SetValue(memo)

    def GetTopic(self):
        return self.topic.GetValue()

    def SetTopic(self, topic):
        self.saved_topic = topic
        return self.topic.SetValue(topic)