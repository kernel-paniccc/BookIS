import flet as ft
from flet import Theme
from Web_app.style_element import snack_bar_success, snack_bar_error, Book_bar, del_bar
from app.database.models import User, Book, async_session
from sqlalchemy import select, delete

import asyncio
async def main(page: ft.Page):
    # init

    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }

    page.title = 'BookIs'
    page.theme = Theme(color_scheme_seed='cyan', font_family='RobotoSlab')
    page.update()
    page.vertical_alignment = ft.MainAxisAlignment.CENTER


    #snack_bar
    page.overlay.append(snack_bar_success)
    page.overlay.append(snack_bar_error)
    page.overlay.append(Book_bar)
    page.overlay.append(del_bar)


    # func
    async def validate(e):
        reg_btn.disabled = not (usr_pass.value and usr_tg_id.value)
        page.update()

    async def singIn_func(e):
        async with async_session() as session:
            user = await session.scalar(select(User).where(User.tg_id == usr_tg_id.value))
            if user and user.password == usr_pass.value:
                usr_tg_id.value = ''
                usr_pass.value = ''
                page.user = user
                page.open(snack_bar_success)
                if len(page.navigation_bar.destinations) < 2:
                    page.navigation_bar.destinations.append(
                        ft.NavigationBarDestination(icon=ft.icons.BOOKMARK_ADD, label='Добавить книгу')
                    )
                    page.navigation_bar.destinations.append(
                        ft.NavigationBarDestination(icon=ft.icons.BOOKMARKS, label='Мои книги')
                    )
                    page.navigation_bar.destinations.append(
                    ft.NavigationBarDestination(icon=ft.icons.DELETE, label='Удалить')
                    )
                page.update()

            elif usr_tg_id != None or usr_pass != None:
                usr_tg_id.value = ''
                usr_pass.value = ''
                page.open(snack_bar_error)
                if len(page.navigation_bar.destinations) > 1:
                    page.navigation_bar.destinations.pop(1)
                    page.navigation_bar.destinations.pop(1)
                    page.navigation_bar.destinations.pop(1)
                page.user = None
                page.update()

    async def navigation(e):
        index = page.navigation_bar.selected_index
        page.clean()

        match index:
            case 0: page.add(page_register)
            case 1: page.add(page_add_book)
            case 2: await load_book(), page.add(page_my_book), page.update()
            case 3: page.add(page_delited)

    async def load_book():
        book_container.controls.clear()
        headers = [
            ft.DataColumn(ft.Text("Автор")),
            ft.DataColumn(ft.Text("Название")),
            ft.DataColumn(ft.Text("Жанр")),
        ]
        table = ft.DataTable(
            columns=headers,
            rows=[],
            border_radius=5
        )
        async with async_session() as session:
            books = await session.execute(select(Book).where(Book.user_id == page.user.tg_id))
            book_list = books.scalars().all()

            for book in book_list:
                row = ft.DataRow(cells=[
                    ft.DataCell(ft.Text(book.autor)),
                    ft.DataCell(ft.Text(book.name)),
                    ft.DataCell(ft.Text(book.genre)),
                ])
                table.rows.append(row)
        book_container.controls.append(table)
        page.update()



    async def add_book(e):
        if book_name.value != "" or book_autor.value != '' or book_genre.value != '':
            async with async_session() as session:
                session.add(Book(autor=book_autor.value, name=book_name.value, genre=book_genre.value, user_id=page.user.tg_id))
                await session.commit()
            page.open(Book_bar)
            book_name.value = ''
            book_genre.value = ''
            book_autor.value = ''

        else: page.open(snack_bar_error)
        page.update()

    async def delet_book(e):
        if book_name.value != "" or book_autor.value != '':
            async with async_session() as session:
                books = await session.scalar(select(Book).where(
                    Book.user_id == page.user.tg_id,
                    Book.autor == book_autor.value,
                    Book.name == book_name.value
                ))
                if books != None:
                    stmt = delete(Book).where(
                        Book.user_id == page.user.tg_id,
                        Book.autor == book_autor.value,
                        Book.name == book_name.value
                    )
                    await session.execute(stmt)
                    await session.commit()
                    page.open(del_bar)
            book_name.value = ''
            book_autor.value = ''

        else: page.open(snack_bar_error)
        page.update()

    usr_tg_id = ft.TextField(label='Telegram ID', on_change=validate, width=300)
    usr_pass = ft.TextField(label='Пароль', password=True, on_change=validate, width=300)
    reg_btn = ft.OutlinedButton(text='Войти', on_click=singIn_func, disabled=True)

    book_autor = ft.TextField(label='Автор', width=300)
    book_name = ft.TextField(label='Название', width=300)
    book_genre = ft.TextField(label='Жанр', width=300)
    add_book_btn = ft.OutlinedButton(text='Добавить книгу', on_click=add_book)
    del_btn = ft.OutlinedButton(text='Удалить', on_click=delet_book)
    book_container = ft.Column(spacing=10)


    #value
    page_register=ft.Container(
            content=ft.Column(
                [
                    ft.Text('Вход', size=50, color=ft.colors.CYAN_400),
                    usr_tg_id,
                    usr_pass,
                    reg_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            padding=20,
            border_radius=10,
            alignment=ft.alignment.center
        )

    page_add_book = ft.Container(
        content=ft.Column(
            [
                ft.Text('Добавить книгу', size=50, color=ft.colors.CYAN_400),
                book_autor,
                book_name,
                book_genre,
                add_book_btn
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            spacing=20
        ),
        padding=20,
        border_radius=10,
        alignment=ft.alignment.center
    )

    page_my_book = ft.Container(
        content=ft.Column(
            [
                ft.Text('Мои книги', size=50, color=ft.colors.CYAN_400),
                book_container
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        padding=20,
        border_radius=10,
        alignment=ft.alignment.center
    )


    page_delited=ft.Container(
            content=ft.Column(
                [
                    ft.Text('Удалить книгу', size=50, color=ft.colors.CYAN_400),
                    book_autor,
                    book_name,
                    del_btn
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=20
            ),
            padding=20,
            border_radius=10,
            alignment=ft.alignment.center
        )




    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.icons.LOGIN, label='Вход')
        ],
        on_change=navigation
    )

    #render page
    page.add(
        page_register
    )


if __name__ == '__main__':
    ft.app(target=main, view=None, port=8080)