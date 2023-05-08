import pickle
class fichero:
    def  __init__(self, ruta, delimitador = None) -> None:
        self.__info_fichero = []
        self.ruta = ruta
        self.delimitador = delimitador

    @property
    def _info_fichero (self):
        return self.__info_fichero

    @_info_fichero.setter
    def _info_fichero(self,item):
        if type(item) is str:
            self.__info_fichero.append(item)

    def generarListaChistes(self):
        with open(self.ruta,"r") as fichero:
            aux = ""
            while True:
                letra =  fichero.read(1)
                if letra ==  "":
                    break
                elif letra == self.delimitador:
                    self._info_fichero = aux
                    aux = ""
                else:
                    aux += letra

    def obtenerListaChistes(self):
        return  self._info_fichero

    def serializar(self,objeto):
        with open(self.ruta,"wb") as fichero:
            pickle.dump(objeto,fichero,-1)


    def deserializar(self):
        with open(self.ruta,"rb") as fichero:
            return pickle.load(fichero)