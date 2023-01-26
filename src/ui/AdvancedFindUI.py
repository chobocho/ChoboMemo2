import wx
from wx.lib import sized_controls

from util.clipboardutil import on_get_uri_from_clipboard

WINDOW_SIZE_W = 750
WINDOW_SIZE_H = 500
NEXT_STEP = 800
LIST_SIZE_W = 250

class AdvanceFindUI(sized_controls.SizedDialog):
    def __init__(self, *args, ctrl_btn_list=[], recent_item_list=[], user_memo_list=[], **kwargs):
        super(AdvanceFindUI, self).__init__(*args, **kwargs)
        self.user_memo_list = user_memo_list
        self.is_update_memo = True
        font = wx.Font(14, wx.FONTFAMILY_TELETYPE, wx.NORMAL, wx.NORMAL)
        pane = self.GetContentsPane()
        self._add_result_text_box(font, pane)

        static_line = wx.StaticLine(pane, style=wx.LI_HORIZONTAL)
        static_line.SetSizerProps(border=('all', 0), expand=True)

        ##
        # list ctrl1 Ctrl+1-0
        ctrl_list_panel = sized_controls.SizedPanel(pane)
        ctrl_list_panel.SetSizerType('horizontal')
        ctrl_list_panel.SetSizerProps(align='center')

        self._add_ctrl_btn_list(ctrl_list_panel, ctrl_btn_list)
        self._add_recent_item_list(ctrl_list_panel, recent_item_list)
        self._add_user_item_list(ctrl_list_panel, font, self.user_memo_list)

        static_line = wx.StaticLine(pane, style=wx.LI_HORIZONTAL)
        static_line.SetSizerProps(border=('all', 0), expand=True)

        self._add_ok_cancel_btn_box(pane)

        set_focus_input_field_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.on_set_focus_input_field, id=set_focus_input_field_id)

        accel_tbl = wx.AcceleratorTable([
            (wx.ACCEL_ALT, ord('D'), set_focus_input_field_id),
            (wx.ACCEL_ALT, ord('L'), wx.ID_CANCEL),
            (wx.ACCEL_ALT, ord('O'), wx.ID_OK)
        ])
        self.SetAcceleratorTable(accel_tbl)
        self.Fit()

    def _add_ok_cancel_btn_box(self, pane):
        pane_btns = sized_controls.SizedPanel(pane)
        pane_btns.SetSizerType('horizontal')
        pane_btns.SetSizerProps(align='center')

        button_ok = wx.Button(pane_btns, wx.ID_OK, label='&OK')
        button_ok.Bind(wx.EVT_BUTTON, self.on_button)
        button_cancel = wx.Button(pane_btns, wx.ID_CANCEL, label='Cance&l')
        button_cancel.Bind(wx.EVT_BUTTON, self.on_button)

    def _add_ctrl_btn_list(self, pane, list_data=[]):
        ctrl_btn_list_id = wx.NewId()
        self.ctrl_btn_list = wx.ListCtrl(pane, ctrl_btn_list_id,
                                         style=wx.LC_REPORT
                                               | wx.BORDER_NONE
                                               | wx.LC_NO_HEADER
                                               | wx.LC_EDIT_LABELS,
                                         size=(LIST_SIZE_W, 400))
        self.ctrl_btn_list.InsertColumn(0, "Keyword", width=LIST_SIZE_W)
        self.ctrl_btn_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_ctrl_btn_list_selected)
        self.ctrl_btn_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_ctrl_btn_list_dclicked)
        self.ctrl_btn_list_selected = -1

        self.ctrl_btn_list.DeleteAllItems()
        self.insert_data_to_listctrl(self.ctrl_btn_list, list_data)

    def _add_recent_item_list(self, pane, list_data=[]):
        recent_item_list_id = wx.NewId()
        self.recent_item_list = wx.ListCtrl(pane, recent_item_list_id,
                                         style=wx.LC_REPORT
                                               | wx.BORDER_NONE
                                               | wx.LC_NO_HEADER
                                               | wx.LC_EDIT_LABELS,
                                         size=(LIST_SIZE_W, 400))
        self.recent_item_list.InsertColumn(0, "Keyword", width=LIST_SIZE_W)
        self.recent_item_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_recent_item_list_selected)
        self.recent_item_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_recent_item_list_dclicked)
        self.recent_item_list_selected = -1

        self.recent_item_list.DeleteAllItems()
        self.insert_data_to_listctrl(self.recent_item_list, list_data, 1)

    def _add_user_item_list(self, pane, font, list_data=[]):
        user_item_panel = sized_controls.SizedPanel(pane)
        user_item_panel.SetSizerType('vectical')
        user_item_panel.SetSizerProps(align='center')

        user_input_panel = sized_controls.SizedPanel(user_item_panel)
        user_input_panel.SetSizerType('horizontal')
        user_input_panel.SetSizerProps(align='center')

        self.user_input_text = wx.TextCtrl(user_input_panel, style=wx.TE_PROCESS_ENTER, size=(230, 25))
        self.user_input_text.Bind(wx.EVT_TEXT_ENTER, self.on_add_user_input)
        self.user_input_text.SetValue("")
        self.user_input_text.SetFont(font)

        user_input_clear_btn = wx.Button(user_input_panel, wx.NewId(), label='C', size=(20, 25))
        user_input_clear_btn.Bind(wx.EVT_BUTTON, self.on_clear_user_input)

        user_item_list_id = wx.NewId()
        self.user_item_list = wx.ListCtrl(user_item_panel, user_item_list_id,
                                         style=wx.LC_REPORT
                                               | wx.BORDER_NONE
                                               | wx.LC_NO_HEADER
                                               | wx.LC_EDIT_LABELS,
                                         size=(250, 340))
        self.user_item_list.InsertColumn(0, "Keyword", width=LIST_SIZE_W)
        self.user_item_list.Bind(wx.EVT_LIST_ITEM_SELECTED, self._on_user_item_list_selected)
        self.user_item_list.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self._on_user_item_list_dclicked)
        self.user_item_list.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self._on_user_item_list_remove)
        self.user_item_list_selected = -1

        self.user_item_list.DeleteAllItems()
        self.insert_data_to_listctrl(self.user_item_list, list_data)

        lbl_hint = wx.StaticText(user_item_panel, id=wx.NewId(), label="Delete: Mouse Right Click")

    def _add_result_text_box(self, font, pane):
        result_panel = sized_controls.SizedPanel(pane)
        result_panel.SetSizerType('horizontal')
        result_panel.SetSizerProps(align='center')

        self.result_text = wx.TextCtrl(result_panel, style=wx.TE_PROCESS_ENTER, size=(WINDOW_SIZE_W-50, 25))
        self.result_text.Bind(wx.EVT_TEXT_ENTER, self.on_button)
        self.result_text.SetValue("")
        self.result_text.SetFont(font)
        self.result_text.SetFocus()

        result_clear_btn = wx.Button(result_panel, wx.NewId(), label='Clear')
        result_clear_btn.Bind(wx.EVT_BUTTON, self.on_clear_result_btn)

    def insert_data_to_listctrl(self, list_ctrl, list_data, num=0):
        for item in list_data:
            item_data = item.strip()
            if len(item_data) == 0:
                continue
            index = list_ctrl.InsertItem(list_ctrl.GetItemCount(), 1)
            list_ctrl.SetItem(index, 0, item)

            if index % 2 == num:
                list_ctrl.SetItemBackgroundColour(index, "Light blue")

    def on_button(self, event):
        if self.IsModal():
            self.EndModal(event.EventObject.Id)
        else:
            self.Close()

    def _on_ctrl_btn_list_selected(self, event):
        if self.ctrl_btn_list.GetItemCount() == 0:
            return
        self.ctrl_btn_list_selected = event.Index
        self.on_list_selected(self.ctrl_btn_list, self.ctrl_btn_list_selected)

    def _on_ctrl_btn_list_dclicked(self, event):
        self.on_list_dclicked(self.ctrl_btn_list, self.ctrl_btn_list_selected, event)

    def _on_recent_item_list_selected(self, event):
        if self.recent_item_list.GetItemCount() == 0:
            return
        self.recent_item_list_selected = event.Index
        self.on_list_selected(self.recent_item_list, self.recent_item_list_selected)

    def _on_recent_item_list_dclicked(self, event):
        self.on_list_dclicked(self.recent_item_list, self.recent_item_list_selected, event)

    def _on_user_item_list_selected(self, event):
        if self.user_item_list.GetItemCount() == 0:
            return
        self.user_item_list_selected = event.Index
        self.on_list_selected(self.user_item_list, self.user_item_list_selected)

    def _on_user_item_list_dclicked(self, event):
        self.on_list_dclicked(self.user_item_list, self.user_item_list_selected, event)

    def _on_user_item_list_remove(self, event):
        if self.user_item_list.GetItemCount() == 0 or self.user_item_list_selected < 0:
            return
        index = self.user_item_list_selected
        chosen_item = self.user_item_list.GetItem(index, 0).GetText()
        self.user_memo_list.remove(chosen_item)
        self.result_text.SetValue("")
        self.is_update_memo = True

        self.user_item_list.DeleteAllItems()
        self.insert_data_to_listctrl(self.user_item_list, self.user_memo_list)

    def on_add_user_input(self, event):
        new_item = self.user_input_text.GetValue()
        self.user_input_text.SetValue("")

        new_item = new_item.strip()
        if len(new_item) == 0:
            return
        if new_item in self.user_memo_list:
            return
        self.user_memo_list.append(new_item)

        index = self.user_item_list.InsertItem(self.user_item_list.GetItemCount(), 1)
        self.user_item_list.SetItem(index, 0, new_item)
        if index % 2 == 0:
            self.user_item_list.SetItemBackgroundColour(index, "Light blue")
        self.is_update_memo = True

    def on_clear_user_input(self, event):
        self.user_input_text.SetValue("")

    def on_list_selected(self, list_name, index):
        if index < 0:
            index = 0
        chosen_item = list_name.GetItem(index, 0).GetText()
        self.on_add_result_text(chosen_item)

    def on_list_dclicked(self, list_name, index, event):
        if list_name.GetItemCount() == 0:
            return

        if index < 0:
            index = 0
        chosen_item = list_name.GetItem(index, 0).GetText()
        self.result_text.SetValue(chosen_item)
        self.on_button(event)

    def on_clear_result_btn(self, event):
        self.result_text.SetValue("")

    def GetValue(self):
        return self.result_text.GetValue()

    def SetValue(self, memo):
        return self.result_text.SetValue(memo)

    def on_set_focus_input_field(self, event):
        self.result_text.SetFocus()

    def on_add_result_text(self, new_text):
        text = new_text.strip()
        if len(text) == 0:
            return

        current_data = self.result_text.GetValue()
        if len(current_data) == 0:
            self.result_text.SetValue(text)
        elif text not in current_data:
            self.result_text.SetValue(f'{current_data}, {text}')

    def on_get_user_memo(self):
        return self.is_update_memo, self.user_memo_list