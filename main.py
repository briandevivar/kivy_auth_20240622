from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDModalDatePicker

from datetime import datetime
from faker import Faker
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

from db import auth_tbl, users_tbl
from models import AuthModel, UsersModel

faker = Faker()


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Teal"
        return Builder.load_file("main.kv")

    def show_gender_menu(self, tf, focus):
        if not focus:
            return

        menu_items = [
            {
                "text": "Male",
                "on_release": lambda x="Male": self.gender_menu_callback(x)
            },
            {
                "text": "Female",
                "on_release": lambda x="Female": self.gender_menu_callback(x)
            },
        ]
        MDDropdownMenu(caller=tf, items=menu_items).open()

    def gender_menu_callback(self, selected_gender):
        self.root.get_screen("register_screen").ids.gender.text = selected_gender

    def show_date_picker(self, focus):
        if not focus:
            return

        dd = MDModalDatePicker()
        dd.bind(on_ok=self.on_btn_ok, on_cancel=self.on_btn_cancel)
        dd.open()

    def on_btn_ok(self, instance):
        dt = instance.get_date()[0].strftime("%B %d, %Y")
        self.root.get_screen("register_screen").ids.birthday.text = dt
        instance.dismiss()

    def on_btn_cancel(self, instance):
        instance.dismiss()

    def login_user(self):
        message = ""

        username = self.root.get_screen("login_screen").ids.username
        password = self.root.get_screen("login_screen").ids.password

        if username.text != "" and password.text != "":
            login_details = auth_tbl.login(username.text, password.text)

            if login_details is not None:
                auth: AuthModel = AuthModel(*login_details)

                username.text = ""
                password.text = ""

                user_info: UsersModel = UsersModel(*users_tbl.select_by_id(auth.user_id))

                if user_info:
                    self.root.get_screen("home_screen").ids.full_name_info.text = user_info.full_name
                    self.root.get_screen("home_screen").ids.address_info.text = user_info.address
                    self.root.get_screen("home_screen").ids.birthday_info.text = user_info.birthday
                    self.root.get_screen("home_screen").ids.gender_info.text = user_info.gender

                self.root.current = "home_screen"
            else:
                message = "User does not exist."
        else:
            message = "Username and/or password cannot be empty."

        if message != "":
            MDSnackbar(
                MDSnackbarText(
                    text=message,
                ),
                orientation="horizontal",
            ).open()

    def register_user(self):
        full_name = self.root.get_screen("register_screen").ids.full_name
        address = self.root.get_screen("register_screen").ids.address
        birthday = self.root.get_screen("register_screen").ids.birthday
        gender = self.root.get_screen("register_screen").ids.gender

        if full_name.text != "" and address.text != "" and birthday.text != "" and gender.text != "":
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            inserted_id = users_tbl.insert_info(
                full_name.text,
                address.text,
                birthday.text,
                gender.text,
                created_at,
                updated_at
            )

            full_name.text = ""
            address.text = ""
            birthday.text = ""
            gender.text = ""

            if inserted_id > 0:
                username = f"{faker.color_name()}@{faker.language_name()}"
                password = faker.password(
                    length=10,
                    special_chars=True,
                    digits=True,
                    upper_case=True,
                    lower_case=True
                )
                last_inserted_id = auth_tbl.insert_auth(username, password, inserted_id, created_at, updated_at)

                print(last_inserted_id)

                self.root.current = "home_screen"
            else:
                self.root.current = "login_screen"


if __name__ == '__main__':
    MainApp().run()
