import flet as ft


class View(ft.UserControl):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self._page.title = "Generazioni Interpreti"
        self._page.horizontal_alignment = 'CENTER'
        self._page.theme_mode = ft.ThemeMode.LIGHT
        self._controller = None
        self._title = None
        self._txtN = None
        self._btnCreaGrafo = None
        self._btnAnalizza = None
        self._ddInterprete = None
        self._btnCatena = None
        self.txt_result = None

    def load_interface(self):
        self._title = ft.Text("Generazioni Interpreti", color="blue", size=24)
        self._page.controls.append(self._title)

        # PUNTO 1
        self._txtN = ft.TextField(label="Numero minimo film N", width=200, value="3")
        self._btnCreaGrafo = ft.ElevatedButton(text="Crea Grafo",
                                               on_click=self._controller.handleCreaGrafo)
        self._btnAnalizza = ft.ElevatedButton(text="Analizza",
                                              on_click=self._controller.handleAnalizza)
        row1 = ft.Row([self._txtN, self._btnCreaGrafo, self._btnAnalizza],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row1)

        # PUNTO 2
        self._ddInterprete = ft.Dropdown(label="Interprete di partenza", width=400)
        self._btnCatena = ft.ElevatedButton(text="Catena generazioni",
                                            on_click=self._controller.handleCatena)
        row2 = ft.Row([self._ddInterprete, self._btnCatena],
                      alignment=ft.MainAxisAlignment.CENTER)
        self._page.controls.append(row2)

        self.txt_result = ft.ListView(expand=1, spacing=10, padding=20, auto_scroll=True)
        self._page.controls.append(self.txt_result)
        self._page.update()

    @property
    def controller(self):
        return self._controller

    @controller.setter
    def controller(self, controller):
        self._controller = controller

    def set_controller(self, controller):
        self._controller = controller

    def create_alert(self, message):
        dlg = ft.AlertDialog(title=ft.Text(message))
        self._page.dialog = dlg
        dlg.open = True
        self._page.update()

    def update_page(self):
        self._page.update()
