import networkx as nx
from itertools import combinations

from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.DiGraph()
        self._idMap = {}
        self._solBest = []
        self._pesoBest = -1

    # -------------------- PUNTO 1 --------------------

    def buildGraph(self, minimo):
        self._grafo.clear()
        self._idMap = {}

        nodi = DAO.getNodes(minimo)
        for n in nodi:
            self._idMap[n.id] = n
        self._grafo.add_nodes_from(nodi)

        # a ogni interprete aggiungo i film in cui ha recitato
        for idP, idF in DAO.getCoppie():
            if idP in self._idMap:
                self._idMap[idP].film.add(idF)

        # arco dal più anziano al più giovane, peso = film in comune
        for a, b in combinations(nodi, 2):
            peso = len(a.film & b.film)
            if peso == 0:
                continue
            if a.date_of_birth < b.date_of_birth:
                self._grafo.add_edge(a, b, weight=peso)
            elif b.date_of_birth < a.date_of_birth:
                self._grafo.add_edge(b, a, weight=peso)

    def getNumNodi(self):
        return self._grafo.number_of_nodes()

    def getNumArchi(self):
        return self._grafo.number_of_edges()

    def getNodiOrdinati(self):
        return sorted(self._grafo.nodes, key=lambda x: x.name)


    def getMaxUscenti(self):
        massimo = -1
        lista = []
        for n in self._grafo.nodes:
            g = self._grafo.out_degree(n)
            if g > massimo:
                massimo = g
                lista = [n]
            elif g == massimo:
                lista.append(n)
        lista.sort(key=lambda x: x.name)
        return lista, massimo

    # interpreti con più archi entranti (colleghi più anziani), con i pari merito
    def getMaxEntranti(self):
        massimo = -1
        lista = []
        for n in self._grafo.nodes:
            g = self._grafo.in_degree(n)
            if g > massimo:
                massimo = g
                lista = [n]
            elif g == massimo:
                lista.append(n)
        lista.sort(key=lambda x: x.name)
        return lista, massimo

    # numero di componenti debolmente connesse e dimensione della più grande
    def getComponentiDeboli(self):
        componenti = list(nx.weakly_connected_components(self._grafo))
        numero = len(componenti)
        piuGrande = max(len(c) for c in componenti)
        return numero, piuGrande


    def getCammino(self,partenza):
        self._solBest = []
        self._pesoBest = 0
        self._ricorsione([partenza],0)
        return self._solBest, self._pesoBest


    def _ricorsione(self,parziale,peso):
        if len(parziale) > len(self._solBest) or (len(parziale) == len(self._solBest) and peso > self._pesoBest):
            self._solBest = list(parziale)
            self._pesoBest = peso

        ultimo = parziale[-1]
        for v in self._grafo.successors(ultimo):
            parziale.append(v)
            self._ricorsione(parziale,peso+ self._grafo[ultimo][v]["weight"])
            parziale.pop()


    def getPesoArco(self,u,v):
        return self._grafo[u][v]["weight"]


