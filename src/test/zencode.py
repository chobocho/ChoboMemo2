code = "'ctrl_{0}' : self.config.GetValue('ctrl_{0}'),"

code2 = """
        ctrl_{0}_pane = sized_controls.SizedPanel(pane)
        ctrl_{0}_pane.SetSizerType('horizontal')
        ctrl_{0}_pane.SetSizerProps(align='center')

        ctrl_{0}_lbl = wx.StaticText(ctrl_{0}_pane, id=wx.NewId(), label="Ctrl+{0}", size=(50,30))
        self.ctrl_{0}_text = wx.TextCtrl(ctrl_{0}_pane, size=(TEXT_SIZE_W,30))
        self.ctrl_{0}_text.SetValue("")
"""

code3 = "self.ctrl_{0}_text.SetValue(config_data['ctrl_{0}'])"
code4 = "'ctrl_{0}' : self.ctrl_{0}_text.GetValue(),"
code5 = "self.config['ctrl_{0}'] = key['ctrl_{0}']"
code6 = "self.ctrl_{0}_item.SetItemLabel(key['ctrl_{0}'] + '\\tCtrl+{0}')"

def main():
    for i in range(10):
        print(code6.format(i))


if __name__ == '__main__':
    main()
