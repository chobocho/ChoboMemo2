import wx
from wx.lib import sized_controls

TEXT_SIZE_W = 150


class ConfigSettingUI(sized_controls.SizedDialog):
    def __init__(self, *args, **kwargs):
        super(ConfigSettingUI, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        config_pane = self.GetContentsPane()

        main_pane = sized_controls.SizedPanel(config_pane)
        main_pane.SetSizerType('horizontal')
        main_pane.SetSizerProps(align='center')

        self._add_ctrl_list_ui(main_pane)
        self._add_config_list_ui(main_pane)
        self._add_memo_pane(config_pane)
        self._add_button_pane(config_pane)
        self.Fit()

    def _add_memo_pane(self, config_pane):
        memo_pane = sized_controls.SizedPanel(config_pane)
        memo_pane.SetSizerType('horizontal')
        memo_pane.SetSizerProps(align='center')
        memo_lbl = wx.StaticText(memo_pane, id=wx.NewId(), label="Memo", size=(50, 30))
        self.memo_text = wx.TextCtrl(memo_pane, style=wx.TE_MULTILINE, size=(TEXT_SIZE_W + 200, 120))
        self.memo_text.SetValue("")

    def _add_button_pane(self, config_pane):
        pane_btns = sized_controls.SizedPanel(config_pane)
        pane_btns.SetSizerType('horizontal')
        pane_btns.SetSizerProps(align='center')
        button_ok = wx.Button(pane_btns, wx.ID_OK, label='&OK')
        button_ok.Bind(wx.EVT_BUTTON, self.on_button)
        button_cancel = wx.Button(pane_btns, wx.ID_CANCEL, label='Cance&l')
        button_cancel.Bind(wx.EVT_BUTTON, self.on_button)

    def _add_config_list_ui(self, main_pane):
        pane = sized_controls.SizedPanel(main_pane)
        pane.SetSizerType('vectical')
        pane.SetSizerProps(halign='left', valign='top')

        self.cb_ask_before_quit = wx.CheckBox(pane, wx.NewId(), "Ask before quit", size=(200,25))
        self.cb_save_cfm = wx.CheckBox(pane, wx.NewId(), "Save with CFM", size=(200,25))
        self.cb_save_cfm.Bind(wx.EVT_CHECKBOX, self.on_toggle_save_cfm)
        self.cb_save_compressed_mode = wx.CheckBox(pane, wx.NewId(), "Save CFM as compressed mode", size=(200, 25))

    def _add_ctrl_list_ui(self, main_pane):
        pane = sized_controls.SizedPanel(main_pane)
        pane.SetSizerType('vectical')
        pane.SetSizerProps(align='center')
        ctrl_i_pane = sized_controls.SizedPanel(pane)
        ctrl_i_pane.SetSizerType('horizontal')
        ctrl_i_pane.SetSizerProps(align='center')
        ctrl_i_lbl = wx.StaticText(ctrl_i_pane, id=wx.NewId(), label="Ctrl+i", size=(50, 30))
        self.ctrl_i_text = wx.TextCtrl(ctrl_i_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_i_text.SetValue("")
        ctrl_1_pane = sized_controls.SizedPanel(pane)
        ctrl_1_pane.SetSizerType('horizontal')
        ctrl_1_pane.SetSizerProps(align='center')
        ctrl_1_lbl = wx.StaticText(ctrl_1_pane, id=wx.NewId(), label="Ctrl+1", size=(50, 30))
        self.ctrl_1_text = wx.TextCtrl(ctrl_1_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_1_text.SetValue("")
        ctrl_2_pane = sized_controls.SizedPanel(pane)
        ctrl_2_pane.SetSizerType('horizontal')
        ctrl_2_pane.SetSizerProps(align='center')
        ctrl_2_lbl = wx.StaticText(ctrl_2_pane, id=wx.NewId(), label="Ctrl+2", size=(50, 30))
        self.ctrl_2_text = wx.TextCtrl(ctrl_2_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_2_text.SetValue("")
        ctrl_3_pane = sized_controls.SizedPanel(pane)
        ctrl_3_pane.SetSizerType('horizontal')
        ctrl_3_pane.SetSizerProps(align='center')
        ctrl_3_lbl = wx.StaticText(ctrl_3_pane, id=wx.NewId(), label="Ctrl+3", size=(50, 30))
        self.ctrl_3_text = wx.TextCtrl(ctrl_3_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_3_text.SetValue("")
        ctrl_4_pane = sized_controls.SizedPanel(pane)
        ctrl_4_pane.SetSizerType('horizontal')
        ctrl_4_pane.SetSizerProps(align='center')
        ctrl_4_lbl = wx.StaticText(ctrl_4_pane, id=wx.NewId(), label="Ctrl+4", size=(50, 30))
        self.ctrl_4_text = wx.TextCtrl(ctrl_4_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_4_text.SetValue("")
        ctrl_5_pane = sized_controls.SizedPanel(pane)
        ctrl_5_pane.SetSizerType('horizontal')
        ctrl_5_pane.SetSizerProps(align='center')
        ctrl_5_lbl = wx.StaticText(ctrl_5_pane, id=wx.NewId(), label="Ctrl+5", size=(50, 30))
        self.ctrl_5_text = wx.TextCtrl(ctrl_5_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_5_text.SetValue("")
        ctrl_6_pane = sized_controls.SizedPanel(pane)
        ctrl_6_pane.SetSizerType('horizontal')
        ctrl_6_pane.SetSizerProps(align='center')
        ctrl_6_lbl = wx.StaticText(ctrl_6_pane, id=wx.NewId(), label="Ctrl+6", size=(50, 30))
        self.ctrl_6_text = wx.TextCtrl(ctrl_6_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_6_text.SetValue("")
        ctrl_7_pane = sized_controls.SizedPanel(pane)
        ctrl_7_pane.SetSizerType('horizontal')
        ctrl_7_pane.SetSizerProps(align='center')
        ctrl_7_lbl = wx.StaticText(ctrl_7_pane, id=wx.NewId(), label="Ctrl+7", size=(50, 30))
        self.ctrl_7_text = wx.TextCtrl(ctrl_7_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_7_text.SetValue("")
        ctrl_8_pane = sized_controls.SizedPanel(pane)
        ctrl_8_pane.SetSizerType('horizontal')
        ctrl_8_pane.SetSizerProps(align='center')
        ctrl_8_lbl = wx.StaticText(ctrl_8_pane, id=wx.NewId(), label="Ctrl+8", size=(50, 30))
        self.ctrl_8_text = wx.TextCtrl(ctrl_8_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_8_text.SetValue("")
        ctrl_9_pane = sized_controls.SizedPanel(pane)
        ctrl_9_pane.SetSizerType('horizontal')
        ctrl_9_pane.SetSizerProps(align='center')
        ctrl_9_lbl = wx.StaticText(ctrl_9_pane, id=wx.NewId(), label="Ctrl+9", size=(50, 30))
        self.ctrl_9_text = wx.TextCtrl(ctrl_9_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_9_text.SetValue("")
        ctrl_0_pane = sized_controls.SizedPanel(pane)
        ctrl_0_pane.SetSizerType('horizontal')
        ctrl_0_pane.SetSizerProps(align='center')
        ctrl_0_lbl = wx.StaticText(ctrl_0_pane, id=wx.NewId(), label="Ctrl+0", size=(50, 30))
        self.ctrl_0_text = wx.TextCtrl(ctrl_0_pane, size=(TEXT_SIZE_W, 30))
        self.ctrl_0_text.SetValue("")
        memo_pane = sized_controls.SizedPanel(pane)
        memo_pane.SetSizerType('horizontal')
        memo_pane.SetSizerProps(align='center')

    def on_toggle_save_cfm(self, event):
        if self.cb_save_cfm.GetValue():
            self.cb_save_compressed_mode.Enable(True)
        else:
            self.cb_save_compressed_mode.Enable(False)

    def on_button(self, event):
        if self.IsModal():
            self.EndModal(event.EventObject.Id)
        else:
            self.Close()

    def GetValue(self):
        config_data = {
            'ctrl_0': self.ctrl_0_text.GetValue(),
            'ctrl_1': self.ctrl_1_text.GetValue(),
            'ctrl_2': self.ctrl_2_text.GetValue(),
            'ctrl_3': self.ctrl_3_text.GetValue(),
            'ctrl_4': self.ctrl_4_text.GetValue(),
            'ctrl_5': self.ctrl_5_text.GetValue(),
            'ctrl_6': self.ctrl_6_text.GetValue(),
            'ctrl_7': self.ctrl_7_text.GetValue(),
            'ctrl_8': self.ctrl_8_text.GetValue(),
            'ctrl_9': self.ctrl_9_text.GetValue(),
            'ctrl_i': self.ctrl_i_text.GetValue(),
            'memo': self.memo_text.GetValue(),
            'ask_before_quit': self.cb_ask_before_quit.GetValue(),
            'compressedSave': self.cb_save_compressed_mode.GetValue(),
            'save_cfm': self.cb_save_cfm.GetValue()
        }
        return config_data

    def SetValue(self, config_data):
        self.ctrl_0_text.SetValue(config_data['ctrl_0'])
        self.ctrl_1_text.SetValue(config_data['ctrl_1'])
        self.ctrl_2_text.SetValue(config_data['ctrl_2'])
        self.ctrl_3_text.SetValue(config_data['ctrl_3'])
        self.ctrl_4_text.SetValue(config_data['ctrl_4'])
        self.ctrl_5_text.SetValue(config_data['ctrl_5'])
        self.ctrl_6_text.SetValue(config_data['ctrl_6'])
        self.ctrl_7_text.SetValue(config_data['ctrl_7'])
        self.ctrl_8_text.SetValue(config_data['ctrl_8'])
        self.ctrl_9_text.SetValue(config_data['ctrl_9'])
        self.ctrl_i_text.SetValue(config_data['ctrl_i'])
        self.memo_text.SetValue(config_data['memo'])
        self.cb_save_cfm.SetValue(config_data['save_cfm'])
        self.cb_save_compressed_mode.SetValue(config_data['compressedSave'])
        self.cb_save_compressed_mode.Enable(config_data['save_cfm'])
        self.cb_ask_before_quit.SetValue(config_data['ask_before_quit'])
