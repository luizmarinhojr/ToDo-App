import flet as ft
import os
from bd.connectiondb import DataBase


class apk:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'ToDo App'
        self.page.window_width = 400
        self.page.window_height = 600
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.color = {'primary': '#278C39','secundary': '#4C9B53','black': '#000000','white': '#ffffff'}
        self.usuario = os.getlogin()
        self.Database = DataBase()
        self.main()


    def main(self):
        # --------------------ELEMENTOS----------------------
        user_name = ft.Text(
            value = f'Hi, {self.usuario} 😃',
            size = 20
        )

        descricao = ft.Text(
            value = 'Look or add new tasks',
            max_lines = 2,
            text_align = ft.TextAlign.CENTER,
            overflow = "ellipsis",
            size = 13
        )
        
        self.input_task = ft.TextField(
            value = '',
            hint_text = 'Type your task',
            expand = True
        )

        # --------------------CONTAINERS---------------------
        container_apresentation = ft.Container(
            content = ft.Column([
                user_name, descricao
                ],
                horizontal_alignment = ft.CrossAxisAlignment.CENTER
            ),
            alignment = ft.alignment.center,
            padding = 20
        )

        container_input = ft.Container(
            content = ft.Row([
                self.input_task,
                ft.FloatingActionButton(
                    icon = ft.icons.ADD,
                    bgcolor = self.color['primary'],
                    on_click = self.addInDB
                )
            ]),
            padding = 10
        )

        self.page.add(container_apresentation, container_input, self.insertTabs(), self.insertCheckbox())


    def insertTabs(self):
        self.tabs = ft.Tabs(
            tabs = [ft.Tab(text = 'All', adaptive = True),
                ft.Tab(text = 'Active', adaptive = True),
                ft.Tab(text = 'Completed', adaptive = True)
            ],
            on_change = self.updateLists,
            selected_index = 0,
            indicator_color = self.color['primary'],
            label_color = self.color['primary'],
            expand = True
            )
        return ft.Container(
            content = self.tabs
        )

    def insertCheckbox(self, query='SELECT * FROM "tasks"'):
        self.data = self.Database.searchItens(query)
        return ft.Container(
            ft.Column([
                ft.Checkbox(label = item[0], value = True if item[1]=='complete' else False, active_color = self.color['primary'], on_change=self.updateInDB) for item in self.data
                ],
                height=self.page.window_height*0.5,
                scroll=ft.ScrollMode.AUTO
            ),
            padding = 10
        )
    

    def updateLists(self, e=''):
        self.page.controls.pop()
        if self.tabs.selected_index == 0:
            self.page.add(self.insertCheckbox())
        
        if self.tabs.selected_index == 1:
            self.page.add(self.insertCheckbox('SELECT * FROM "tasks" WHERE "status" = "incomplete"'))
        
        if self.tabs.selected_index == 2:
            self.page.add(self.insertCheckbox('SELECT * FROM "tasks" WHERE "status" = "complete"'))


    def addInDB(self, e):
        self.Database.addTasks(self.input_task.value, 'incomplete')
        self.input_task.value = ''
        self.page.controls.pop()
        self.page.add(self.insertCheckbox())


    def updateInDB(self, e):
        value = 'complete' if e.control.value == True else 'incomplete'
        self.Database.updateTasks(value, e.control.label)
        self.updateLists()


if __name__ == "__main__":
    ft.app(target=apk)
