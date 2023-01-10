import wx
from wx.lib import sized_controls

TEXT_SIZE_W = 150

class ConfigSettingUI(sized_controls.SizedDialog):
    def __init__(self, *args, **kwargs):
        super(ConfigSettingUI, self).__init__(*args, **kwargs)
        pane = self.GetContentsPane()

        ctrl_1_pane = sized_controls.SizedPanel(pane)
        ctrl_1_pane.SetSizerType('horizontal')
        ctrl_1_pane.SetSizerProps(align='center')

        ctrl_1_lbl = wx.StaticText(ctrl_1_pane, id=wx.NewId(), label="Ctrl+1", size=(50,30))
        self.ctrl_1_text = wx.TextCtrl(ctrl_1_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_1_text.SetValue("")

        ctrl_2_pane = sized_controls.SizedPanel(pane)
        ctrl_2_pane.SetSizerType('horizontal')
        ctrl_2_pane.SetSizerProps(align='center')

        ctrl_2_lbl = wx.StaticText(ctrl_2_pane, id=wx.NewId(), label="Ctrl+2", size=(50,30))
        self.ctrl_2_text = wx.TextCtrl(ctrl_2_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_2_text.SetValue("")

        ctrl_3_pane = sized_controls.SizedPanel(pane)
        ctrl_3_pane.SetSizerType('horizontal')
        ctrl_3_pane.SetSizerProps(align='center')

        ctrl_3_lbl = wx.StaticText(ctrl_3_pane, id=wx.NewId(), label="Ctrl+3", size=(50,30))
        self.ctrl_3_text = wx.TextCtrl(ctrl_3_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_3_text.SetValue("")

        ctrl_4_pane = sized_controls.SizedPanel(pane)
        ctrl_4_pane.SetSizerType('horizontal')
        ctrl_4_pane.SetSizerProps(align='center')

        ctrl_4_lbl = wx.StaticText(ctrl_4_pane, id=wx.NewId(), label="Ctrl+4", size=(50,30))
        self.ctrl_4_text = wx.TextCtrl(ctrl_4_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_4_text.SetValue("")

        ctrl_5_pane = sized_controls.SizedPanel(pane)
        ctrl_5_pane.SetSizerType('horizontal')
        ctrl_5_pane.SetSizerProps(align='center')

        ctrl_5_lbl = wx.StaticText(ctrl_5_pane, id=wx.NewId(), label="Ctrl+5", size=(50,30))
        self.ctrl_5_text = wx.TextCtrl(ctrl_5_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_5_text.SetValue("")

        ctrl_6_pane = sized_controls.SizedPanel(pane)
        ctrl_6_pane.SetSizerType('horizontal')
        ctrl_6_pane.SetSizerProps(align='center')

        ctrl_6_lbl = wx.StaticText(ctrl_6_pane, id=wx.NewId(), label="Ctrl+6", size=(50,30))
        self.ctrl_6_text = wx.TextCtrl(ctrl_6_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_6_text.SetValue("")

        ctrl_7_pane = sized_controls.SizedPanel(pane)
        ctrl_7_pane.SetSizerType('horizontal')
        ctrl_7_pane.SetSizerProps(align='center')

        ctrl_7_lbl = wx.StaticText(ctrl_7_pane, id=wx.NewId(), label="Ctrl+7", size=(50,30))
        self.ctrl_7_text = wx.TextCtrl(ctrl_7_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_7_text.SetValue("")

        ctrl_8_pane = sized_controls.SizedPanel(pane)
        ctrl_8_pane.SetSizerType('horizontal')
        ctrl_8_pane.SetSizerProps(align='center')

        ctrl_8_lbl = wx.StaticText(ctrl_8_pane, id=wx.NewId(), label="Ctrl+8", size=(50,30))
        self.ctrl_8_text = wx.TextCtrl(ctrl_8_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_8_text.SetValue("")

        ctrl_9_pane = sized_controls.SizedPanel(pane)
        ctrl_9_pane.SetSizerType('horizontal')
        ctrl_9_pane.SetSizerProps(align='center')

        ctrl_9_lbl = wx.StaticText(ctrl_9_pane, id=wx.NewId(), label="Ctrl+9", size=(50,30))
        self.ctrl_9_text = wx.TextCtrl(ctrl_9_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_9_text.SetValue("")

        ctrl_0_pane = sized_controls.SizedPanel(pane)
        ctrl_0_pane.SetSizerType('horizontal')
        ctrl_0_pane.SetSizerProps(align='center')

        ctrl_0_lbl = wx.StaticText(ctrl_0_pane, id=wx.NewId(), label="Ctrl+0", size=(50,30))
        self.ctrl_0_text = wx.TextCtrl(ctrl_0_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_0_text.SetValue("")

        pane_btns = sized_controls.SizedPanel(pane)
        pane_btns.SetSizerType('horizontal')
        pane_btns.SetSizerProps(align='center')

        button_ok = wx.Button(pane_btns, wx.ID_OK, label='&OK')
        button_ok.Bind(wx.EVT_BUTTON, self.on_button)

        button_cancel = wx.Button(pane_btns, wx.ID_CANCEL, label='Cance&l')
        button_cancel.Bind(wx.EVT_BUTTON, self.on_button)
        self.Fit()

    def on_button(self, event):
        if self.IsModal():
            self.EndModal(event.EventObject.Id)
        else:
            self.Close()

    def GetValue(self):
        config_data = {
            'ctrl_0' : self.ctrl_0_text.GetValue(),
            'ctrl_1' : self.ctrl_1_text.GetValue(),
            'ctrl_2' : self.ctrl_2_text.GetValue(),
            'ctrl_3' : self.ctrl_3_text.GetValue(),
            'ctrl_4' : self.ctrl_4_text.GetValue(),
            'ctrl_5' : self.ctrl_5_text.GetValue(),
            'ctrl_6' : self.ctrl_6_text.GetValue(),
            'ctrl_7' : self.ctrl_7_text.GetValue(),
            'ctrl_8' : self.ctrl_8_text.GetValue(),
            'ctrl_9' : self.ctrl_9_text.GetValue(),
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