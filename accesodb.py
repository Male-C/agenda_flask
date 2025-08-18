'''
Módulo encargado de hacer una abstracción de la conexión a la base de datos
independiente a la tecnología utilizada.
'''
from typing import Any, Optional
import pymysql as db
from pymysql.cursors import DictCursor

class AccesoDB:
    """
        Esta clase hace la conexión con la base de datos...
    """
    
    __coneccion : db.Connection|None = None
    
    def __init__(self, host : str, user : str, password :str, database : str) -> None:
        if AccesoDB.__coneccion is None:
            AccesoDB.__coneccion = db.connect(
                                        host=host, 
                                        user=user, 
                                        password=password, 
                                        database=database,
                                        cursorclass=DictCursor) # las consultas devuelven diccionarios

    def consulta_generica(self, consulta : str) -> list[dict[str, Any]]:
        """Hace una consulta la base de datos

        Args:
            consulta (str): Consulta en SQL para hacer en la BD

        Returns:
            list[dict[str, Any]]: Una lista de tuplas donde cada tupla es un registro y 
            cada elemento de la tupla es un campo del registro.
        """
        cursor = self.__coneccion.cursor()
        cursor.execute(consulta)
        resultado = cursor.fetchall()
        cursor.close()
        return resultado
    
    def modificacion_generica(self, query: str) -> int:
        """Hace una inserción, actualización o elimina datos de la base de datos
        INSERT, UPDATE, DELETE.
        
        Args:
            query (str): consulta en SQL a ejecutar en la BD

        Returns:
            int: Cantidad de registros afectados
        """
        cursor : DictCursor = self.__coneccion.cursor()
        resultado = cursor.execute(query)
        cursor.close()
        self.__coneccion.commit()
        return resultado
    
    def obtener(self, tabla: str, columnas: list[str], filtro: Optional[tuple[str,str]] = None) \
        -> list[dict[str,Any]]:
        """Obtiene información de la base de datos
        Args:
            tabla (str): Nombre de la tabla
            columnas (list[str]): Lista de columnas a consultar
            filtro (tuple[str,str], optional): filtro a aplicar. Defaults to None.
        Returns:
            list[dict[str,Any]]: lista de diccionarios del tipo {'columna': 'valor', ...}
        """
        if not columnas:
            raise ValueError("La lista de columnas no puede estar vacía")
        cols = ', '.join(columnas)
        query = f"SELECT {cols} FROM {tabla}"
        if filtro is not None:
            if len(filtro) != 2:
                raise ValueError("El filtro debe ser una tupla de dos elementos: (columna, valor)")
            col, val = filtro
            query += f" WHERE `{col}` = '{val}'"
        return self.consulta_generica(query)
          
    def borrar(self, tabla: str, filtro: tuple[str,str]) -> int:
        """Borra elementos de una tabla que coincidan con el filtro

        Args:
            tabla (str): tabla del registro a borrar
            filtro (tuple[str,str]): filtro que se evalua (columna,valor) en una igualdad

        Raises:
            ValueError: Si el filtro no contiene 2 elementos está mal

        Returns:
            int: Cantidad de registros borrados
        """
        if len(filtro) != 2:
            raise ValueError("El filtro debe tener dos elementos")
        query = f"DELETE FROM `{tabla}` WHERE (`{filtro[0]}` = '{filtro[1]}')"
        print(query)
        return self.modificacion_generica(query)
        
        
        
    def crear(self, tabla: str, data: dict[str,str]) -> int:
        """Crea un registro en la base de datos

        Args:
            tabla (str): tabla donde se inserta el registro
            data (dict[str,str]): datos del registro en forma de diccionario en el cual
            el primer elemento es el nombre de la columna y el segundo es el valor

        Raises:
            ValueError: Di el diccionario está vació

        Returns:
            int: Cantidad de registros creados, la versión actual solo admite 1 registro
        """
        if not data:
            raise ValueError("El diccionario está vació")
        
        columnas = ', '.join(f"`{col}`" for col in data.keys())
        values = ', '.join(f"'{val}'" for val in data.values())    
        consulta = f"INSERT INTO `{tabla}` ({columnas}) VALUES ({values})"
        return self.modificacion_generica(consulta)

    def modificar(self, tabla: str, data: dict[str,str], condicion: tuple[str,str]) -> int:
        """Modifica registros de la base de datos

        Args:
            tabla (str): tabla que contiene los registros a modificar
            data (dict[str,str]): Los datos en formato de diccionario {columna:valor}
            condicion (tuple[str,str]): condición a cumplir para modificar los registros
            del tipo (columna, valor), cuando coincidan se modifica el registro

        Raises:
            ValueError: si los datos o la condición son vacíos

        Returns:
            int: cantidad de registros modificados
        """
        
        pass

    def __del__(self) -> None:
        if AccesoDB.__coneccion is not None:
            AccesoDB.__coneccion.close()
            AccesoDB.__coneccion = None

if __name__ == '__main__':
    pass