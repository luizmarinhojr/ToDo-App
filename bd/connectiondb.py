import sqlite3


class DataBase:
    def __init__(self):
        self.dbExecute('CREATE TABLE IF NOT EXISTS tasks("task" TEXT NOT NULL UNIQUE, "status" TEXT NOT NULL)')


    def dbExecute(self, query, params=[]):
        with sqlite3.connect('bd/database.sqlite') as con:
            cur = con.cursor()
            cur.execute(query, params)
            con.commit()
            return cur.fetchall()
    

    def addTasks(self, name, value):
        self.dbExecute('INSERT INTO tasks("task", "status") VALUES(?, ?)', params=[name, value])
        print('Adicionado ao Banco de Dados - Ok')
    
    def updateTasks(self, value, task):
        self.dbExecute('UPDATE "tasks" SET "status" = ? WHERE "task" = ?', params=[value, task])
        print('Atualizado com sucesso')
    

    def searchItens(self, query):
        tasks = self.dbExecute(query)
        return tasks
