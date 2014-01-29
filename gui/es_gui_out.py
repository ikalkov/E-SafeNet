#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.5 on Wed Jan 22 13:38:37 2014
#Probable plaintext decryption of XOR-encrypted files with a key of 512 bytes (for E-Safenet)
#Copyright (C) 2014  Jan Laan, Cedric Van Bockhaven
#
#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; see the file LICENSE. if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
from esafenet import Esafenet
import wx
import numpy
import os
# begin wxGlade: extracode
# end wxGlade


class MainFrame(wx.Frame):
    text = None
    texts = []
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.frame_2_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        self.opf = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "Open folder..", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.opf)

        self.opfi = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "Open file..", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.opfi)
        wxglade_tmp_menu.AppendSeparator()
        self.ana = wx.MenuItem(wxglade_tmp_menu, wx.NewId(), "Analyze", "", wx.ITEM_NORMAL)
        wxglade_tmp_menu.AppendItem(self.ana)
        self.frame_2_menubar.Append(wxglade_tmp_menu, "File")
        self.SetMenuBar(self.frame_2_menubar)
        # Menu Bar end
        self.list_ctrl_1 = wx.ListCtrl(self, -1, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        for i in range(512):
            self.list_ctrl_1.InsertColumn(i, str(i), width=30)
        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.of, self.opf)
        self.Bind(wx.EVT_MENU, self.anlz, self.ana)
        self.Bind(wx.EVT_MENU, self.ofi, self.opfi)
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("E-Safenet decrypt")
        self.list_ctrl_1.SetMinSize((1800, 500))
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.list_ctrl_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade

    def of(self, event):  # wxGlade: MainFrame.<event_handler>
        filename = ""  # Use  filename as a flag
        dlg = wx.DirDialog(self, message="Choose a folder")
 
        if dlg.ShowModal() == wx.ID_OK:
            dirname = dlg.GetPath()
        dlg.Destroy()
        self.texts.append("")
        if dirname:
           for(root, dirs, files) in os.walk(dirname):
               for f in files:
                   with open(root + "/" + f, "rb") as fh:
                       fi = fh.read()[512:]
                       l_off = len(fi) % 512
                       self.texts[0] += fi + "\x00"*(512-l_off)
                       #self.texts.append(fh.read())

    def ofi(self, event):  # wxGlade: MainFrame.<event_handler>
        filename = ""  # Use  filename as a flag
        dlg = wx.FileDialog(self, message="Choose a file")
 
        if dlg.ShowModal() == wx.ID_OK:
            filename = dlg.GetPath()
        dlg.Destroy()
 
        if filename:
            with open(filename, "rb") as fh:
                self.texts.append(fh.read())
    def xor_with_key(self, text, key):
        xored = ""
        for idx, c in enumerate(text):
            xored += chr(ord(c) ^ key[idx % len(key)])
        return xored

    def anlz(self, event):  # wxGlade: MainFrame.<event_handler>
        #maximize plaintext
        if len(self.texts) > 0:
            print "Analyzing, this can take a while..."
            keyval = [None]*512
            #keyval2 = [None]*512
            for i in range(512):
                keyval[i] = [0]*256
                #keyval2[i] = [0]*8

            for t in range(len(self.texts)):
               text_ord = [ord(c) for c in self.texts[t]]
               rows = ((len(self.texts[t])-1) // 512) + 1
               for i in range(512):
                   for pos_key in range(256):
                       for idx in range(i+512, len(self.texts[t]), 512):
                           o = text_ord[idx] ^ pos_key
                           if (o >= 32 and o <= 126) or o == 9 or o == 10 or o == 13:
                               keyval[i][pos_key] += 1
                               #for q in range(8):
                                #   bit = pos_key >> q & 1
                                 #  if bit == 0:
                                  #     bit = -1
                                   #keyval2[i][q] += bit


            assumed_key = [None]*512
            assumed_key2 = [None]*512
            for i in range(512):
                assumed_key2[i] = [None]*8
            for i in range(512):
                assumed_key[i] = keyval[i].index(max(keyval[i]))
                #for j in range(8):
                    #assumed_key2[i][j] = keyval2[i][j] > 0
                
            print "Analyzing done"
            print assumed_key
            #print assumed_key2
            self.show_dec(assumed_key)

    def show_dec(self, key):
        if len(self.texts) > 0:
            rows = ((len(self.texts[0])-1) // 512) + 1
            for i in range(rows):
                row_txt = self.xor_with_key(self.texts[0][512*i:512*i+512],key)
                self.list_ctrl_1.InsertStringItem(i, "-")
                for j in range(len(row_txt)):
                    if ord(row_txt[j]) >= 32 and ord(row_txt[j]) <= 126:
                        self.list_ctrl_1.SetStringItem(i, j, row_txt[j])
        
            

# end of class MainFrame
class ES_Gui(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MainFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class ES_Gui

if __name__ == "__main__":
    Esafenet = ES_Gui(0)
    Esafenet.MainLoop()
