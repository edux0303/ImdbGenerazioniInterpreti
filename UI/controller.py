import flet as ft


class Controller:
    def __init__(self, view, model):
        self._view = view
        self._model = model

    def _errore(self, msg):
        self._view.txt_result.controls.append(ft.Text(msg, color="red"))
        self._view.update_page()

    # -------------------- PUNTO 1 --------------------

    def handleCreaGrafo(self, e):
        self._view.txt_result.controls.clear()
        try:
            n = int(self._view._txtN.value)
        except (ValueError, TypeError):
            self._errore("N deve essere un intero!")
            return
        if n < 1:
            self._errore("N deve essere almeno 1!")
            return

        self._model.buildGraph(n)
        self._view.txt_result.controls.append(ft.Text("Grafo creato!"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di vertici: {self._model.getNumNodi()}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {self._model.getNumArchi()}"))

        # riempio il dropdown con i nodi in ordine alfabetico
        self._view._ddInterprete.options.clear()
        self._view._ddInterprete.value = None
        for i in self._model.getNodiOrdinati():
            self._view._ddInterprete.options.append(ft.dropdown.Option(key=i.id, text=i.name))
        self._view.update_page()

    def handleAnalizza(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        uscenti, maxOut = self._model.getMaxUscenti()
        nomi = ", ".join(str(i) for i in uscenti)
        self._view.txt_result.controls.append(
            ft.Text(f"Max archi uscenti (colleghi più giovani): {maxOut} -> {nomi}"))

        entranti, maxIn = self._model.getMaxEntranti()
        nomi = ", ".join(str(i) for i in entranti)
        self._view.txt_result.controls.append(
            ft.Text(f"Max archi entranti (colleghi più anziani): {maxIn} -> {nomi}"))

        numero, piuGrande = self._model.getComponentiDeboli()
        self._view.txt_result.controls.append(
            ft.Text(f"Componenti debolmente connesse: {numero}"))
        self._view.txt_result.controls.append(
            ft.Text(f"Dimensione della più grande: {piuGrande}"))
        self._view.update_page()

    # -------------------- PUNTO 2 --------------------

    def handleCatena(self, e):
        self._view.txt_result.controls.clear()
        if self._model.getNumNodi() == 0:
            self._errore("Crea prima il grafo!")
            return

        idScelto = self._view._ddInterprete.value
        if idScelto is None:
            self._errore("Seleziona un interprete!")
            return
        partenza = self._model._idMap[idScelto]

        catena, peso = self._model.getCammino(partenza)

        if len(catena) == 1:
            self._view.txt_result.controls.append(
                ft.Text(f"{partenza} non ha colleghi più giovani: è il più giovane della sua catena."))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(f"Catena da {partenza}:"))
        for i in range(len(catena) - 1):
            u = catena[i]
            v = catena[i + 1]
            self._view.txt_result.controls.append(
                ft.Text(f"{u} ({u.date_of_birth}) --({self._model.getPesoArco(u, v)})--> {v}"))
        ultimo = catena[-1]
        self._view.txt_result.controls.append(ft.Text(f"{ultimo} ({ultimo.date_of_birth})"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di interpreti: {len(catena)}"))
        self._view.txt_result.controls.append(ft.Text(f"Peso totale: {peso}"))
        self._view.update_page()
