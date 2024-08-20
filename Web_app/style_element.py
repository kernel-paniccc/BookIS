import flet as ft

snack_bar_success = ft.SnackBar(
    ft.Row(
        [ft.Text("Вы успешно авторизованны", color=ft.colors.GREEN_500, size=20)],
        alignment=ft.MainAxisAlignment.CENTER
    ),
    bgcolor=ft.colors.GREY_900,
)

snack_bar_error = ft.SnackBar(
    ft.Row(
        [ft.Text("Некорректные данные", color=ft.colors.RED_500, size=20)],
        alignment=ft.MainAxisAlignment.CENTER
    ),
    bgcolor=ft.colors.GREY_900,
)

Book_bar = ft.SnackBar(
    ft.Row(
        [ft.Text("Книга успешно добавленна", color=ft.colors.GREEN_500, size=20)],
        alignment=ft.MainAxisAlignment.CENTER
    ),
    bgcolor=ft.colors.GREY_900,
)

del_bar = ft.SnackBar(
    ft.Row(
        [ft.Text("Книга успешно удалена", color=ft.colors.GREEN_500, size=20)],
        alignment=ft.MainAxisAlignment.CENTER
    ),
    bgcolor=ft.colors.GREY_900,
)
