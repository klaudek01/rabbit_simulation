import wx
from sprawozdanie import Symulator
import os

class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        super(MainFrame, self).__init__(*args, **kw)
        self.symulator = Symulator()
        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)# Ustawienie układu za pomocą sizerów

        # Ścieżka do pliku
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.file_path_text_ctrl = wx.TextCtrl(panel, value="Tutaj podaj plik z populacją")
        self.file_path_text_ctrl.Bind(wx.EVT_LEFT_DOWN, self.OnClickClearFileText)
        self.file_path_text_ctrl.Bind(wx.EVT_SET_FOCUS, self.OnClickClearFileText)
        self.file_path_text_ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocusFileText)
        self.load_button = wx.Button(panel, label='Wczytaj')
        self.load_button.Bind(wx.EVT_BUTTON, self.OnLoad)

        hbox1.Add(self.file_path_text_ctrl, proportion=1, flag=wx.EXPAND)
        hbox1.Add(self.load_button, flag=wx.LEFT, border=5)

        vbox.Add(hbox1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        #Dodanie przycisku i kontrolki do wyświetlania statystyk
        self.stats_button = wx.Button(panel, label='Wyświetl statystyki')
        self.stats_button.Bind(wx.EVT_BUTTON, self.OnDisplayStats)
        vbox.Add(self.stats_button, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Dodanie pola tekstowego do wyświetlania wyników
        self.results_text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        vbox.Add(self.results_text_ctrl, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Dodanie kontrolek do krzyżówki
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        self.id1_text_ctrl = wx.TextCtrl(panel, value="Podaj ID pierwszego osobnika")
        self.id1_text_ctrl.Bind(wx.EVT_LEFT_DOWN, self.OnClickClearID1Text)
        self.id1_text_ctrl.Bind(wx.EVT_SET_FOCUS, self.OnClickClearID1Text)
        self.id1_text_ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocusID1Text)
        self.id2_text_ctrl = wx.TextCtrl(panel, value="Podaj ID drugiego osobnika")
        self.id2_text_ctrl.Bind(wx.EVT_LEFT_DOWN, self.OnClickClearID2Text)
        self.id2_text_ctrl.Bind(wx.EVT_SET_FOCUS, self.OnClickClearID2Text)
        self.id2_text_ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocusID2Text)
        self.cross_button = wx.Button(panel, label='Wykonaj krzyżówkę')
        self.cross_button.Bind(wx.EVT_BUTTON, self.OnCross)

        hbox2.Add(self.id1_text_ctrl, proportion=1, flag=wx.EXPAND)
        hbox2.Add(self.id2_text_ctrl, proportion=1, flag=wx.EXPAND)
        hbox2.Add(self.cross_button, flag=wx.LEFT, border=5)

        vbox.Add(hbox2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Dodanie przycisku wyszukiwania po ID
        self.search_id_button = wx.Button(panel, label='Znajdź po ID')
        self.search_id_button.Bind(wx.EVT_BUTTON, self.OnSearchID)
        vbox.Add(self.search_id_button, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Dodanie pola tekstowego dla ID
        self.id_search_text_ctrl = wx.TextCtrl(panel, value="Podaj ID szukanego królika")
        self.id_search_text_ctrl.Bind(wx.EVT_LEFT_DOWN, self.OnClickClearSearchIDText)
        self.id_search_text_ctrl.Bind(wx.EVT_SET_FOCUS, self.OnClickClearSearchIDText)
        self.id_search_text_ctrl.Bind(wx.EVT_KILL_FOCUS, self.OnLoseFocusSearchIDText)
        vbox.Add(self.id_search_text_ctrl, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Dodanie przycisku zapisu historii do pliku
        self.save_history_button = wx.Button(panel, label='Zapisz historię do pliku')
        self.save_history_button.Bind(wx.EVT_BUTTON, self.OnSaveHistory)
        vbox.Add(self.save_history_button, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Dodanie przycisku zakończenia programu
        self.exit_button = wx.Button(panel, label='Zakończ działanie programu')
        self.exit_button.Bind(wx.EVT_BUTTON, self.OnExit)
        vbox.Add(self.exit_button, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP, border=10)

        # Ustawienie sizerów dla panelu
        panel.SetSizer(vbox)

        # Ustawienie rozmiaru okna
        self.SetSize((800, 600))
        self.SetTitle('Symulator Krzyżowania Królików')
        self.Centre()

    def OnLoad(self, event):
        file_path = self.file_path_text_ctrl.GetValue()
        # Dopisanie rozszerzenia .txt, jeśli nie zostało podane
        if not file_path.endswith('.txt'):
            file_path += '.txt'
        
        # Sprawdzenie, czy plik istnieje po dopisaniu rozszerzenia
        if not os.path.exists(file_path):
            wx.MessageBox('Podany plik nie istnieje.', 'Błąd', wx.OK | wx.ICON_ERROR)
            return  # Przerwanie metody, jeśli plik nie istnieje
        
        try:
            self.symulator.wczytaj_dane(file_path)
            wx.MessageBox('Dane wczytane pomyślnie.', 'Info', wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f'Wystąpił błąd: {e}', 'Błąd', wx.OK | wx.ICON_ERROR)
            
    def OnDisplayStats(self, event):
        statystyki = self.symulator.populacja.wyświetl_statystyki_kolorów()
        self.results_text_ctrl.SetValue(statystyki)

    def OnCross(self, event):
        id_rodzica1 = self.id1_text_ctrl.GetValue()
        id_rodzica2 = self.id2_text_ctrl.GetValue()
        try:
            wynik_krzyzowki = self.symulator.wykonaj_krzyżówkę(id_rodzica1, id_rodzica2)
            genotyp_rodzica1 = self.symulator.populacja.sprawdź_genotyp(id_rodzica1)
            genotyp_rodzica2 = self.symulator.populacja.sprawdź_genotyp(id_rodzica2)
            wynik_text = f"Rodzic #1 (ID: {id_rodzica1}, Genotyp: {genotyp_rodzica1})\n" \
                         f"Rodzic #2 (ID: {id_rodzica2}, Genotyp: {genotyp_rodzica2})\n" \
                         "Potomkowie:\n"
            if isinstance(wynik_krzyzowki, list):  # Jeśli wynik to lista ID potomstwa
                for id_potomka in wynik_krzyzowki:
                    genotyp_potomka = self.symulator.populacja.sprawdź_genotyp(id_potomka)
                    wynik_text += f"ID: {id_potomka}, Genotyp: {genotyp_potomka}\n"
            else:
                wynik_text += wynik_krzyzowki  # Jeśli wynik to komunikat o błędzie
            self.results_text_ctrl.SetValue(wynik_text)
        except Exception as e:
            wx.MessageBox(f'Wystąpił błąd: {e}', 'Błąd', wx.OK | wx.ICON_ERROR)

    def OnSearchID(self, event):
        id_królika = self.id_search_text_ctrl.GetValue()
        genotyp = self.symulator.populacja.sprawdź_genotyp(id_królika)
        self.results_text_ctrl.SetValue(f"Genotyp królika {id_królika}: {genotyp}")
        
    def OnClickClearSearchIDText(self, event):
        if self.id_search_text_ctrl.GetValue() == "Podaj ID szukanego królika":
            self.id_search_text_ctrl.Clear()
        event.Skip()

    def OnLoseFocusSearchIDText(self, event):
        if not self.id_search_text_ctrl.GetValue():
            self.id_search_text_ctrl.SetValue("Podaj ID szukanego królika")
        event.Skip()
       
    def OnSaveHistory(self, event):
        with wx.TextEntryDialog(self, "Podaj nazwę pliku do zapisu:", "Zapisz historię do pliku") as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                nazwa_pliku = dialog.GetValue()
                # Sprawdź, czy nazwa pliku kończy się na .txt. Jeśli nie, dodaj rozszerzenie.
                if not nazwa_pliku.lower().endswith('.txt'):
                    nazwa_pliku += '.txt'
                self.symulator.zapisz_historię_do_pliku_txt(nazwa_pliku)

    def OnExit(self, event):
        self.Close(True)

    def OnClickClearFileText(self, event):
        # Usuwa tekst tylko jeśli jest to domyślny tekst informacyjny
        if self.file_path_text_ctrl.GetValue() == "Tutaj podaj plik z populacją":
            self.file_path_text_ctrl.Clear()
        event.Skip()  # Pozwala na dalsze przetwarzanie zdarzenia, np. ustawienie fokusu


    def OnLoseFocusFileText(self, event):
        # Jeśli pole jest puste po utracie fokusu, przywraca domyślny tekst
        if not self.file_path_text_ctrl.GetValue():
            self.file_path_text_ctrl.SetValue("Tutaj podaj plik z populacją")
        event.Skip()
        
    def OnClickClearID1Text(self, event):
        if self.id1_text_ctrl.GetValue() == "Podaj ID pierwszego osobnika":
            self.id1_text_ctrl.Clear()
        event.Skip()

    def OnLoseFocusID1Text(self, event):
        if not self.id1_text_ctrl.GetValue():
            self.id1_text_ctrl.SetValue("Podaj ID pierwszego osobnika")
        event.Skip()

    def OnClickClearID2Text(self, event):
        if self.id2_text_ctrl.GetValue() == "Podaj ID drugiego osobnika":
            self.id2_text_ctrl.Clear()
        event.Skip()

    def OnLoseFocusID2Text(self, event):
        if not self.id2_text_ctrl.GetValue():
            self.id2_text_ctrl.SetValue("Podaj ID drugiego osobnika")
        event.Skip()
             
def main():
    app = wx.App()
    frame = MainFrame(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
