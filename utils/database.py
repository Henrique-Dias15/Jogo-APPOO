import os
import sqlite3
class DatabaseManager:
    def __init__(self, db_path:str="db.db")->None:
        self._db_path = db_path
        self._conexao = None
        if not os.path.exists(self._db_path):
            self.__criar(script_path="scripts/init.sql")
        self._conexao = self.__conectar()

    def __conectar(self)-> sqlite3.Connection:
        if not self._conexao:
            self._conexao = sqlite3.connect(self._db_path)
            self._conexao.execute("PRAGMA foreign_keys = ON")
            self._cursor = self._conexao.cursor()
        return self._conexao
    
    def __criar(self, script_path:str) -> None:
        with open(script_path, 'r', encoding='utf-8') as script_file:
            self._script = script_file.read()
        
        with self.__conectar() as conexao:
            self._cursor = conexao.cursor()
            self._cursor.executescript(self._script)
            conexao.commit()

    def adicionar(self, player_name:str, player_time:int)->None:
        query = "INSERT INTO player (name, time) VALUES (?, ?)"
        params = (player_name, player_time)
        self._cursor.execute(query, params)
        self._conexao.commit()
    

    def listar_rankings(self) -> list:
        query = "SELECT name, time FROM player ORDER BY time DESC, id ASC LIMIT 10"
        self._cursor.execute(query)
        return self._cursor.fetchall()
