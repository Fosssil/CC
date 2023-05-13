import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk
import re


class RealTimeCurrencyConverter:
    def __init__(self, url):
        self.data = requests.get(url).json()
        self.currencies = self.data["rates"]

    def convert(self, from_currency, to_currency, amount):
        initial_amount = amount
        if from_currency != "USD":
            amount = amount / self.currencies[from_currency]

        # limiting the precision to 4 decimal places
        amount = round(amount * self.currencies[to_currency], 4)
        return amount


class App(tk.Tk):
    def __init__(self, converter):
        tk.Tk.__init__(self)
        self.title = "Currency Converter"
        self.currency_converter = converter

        self.geometry("1000x400")
        # self.configure(bg="#F22546")

        # Label
        self.intro_label = Label(
            self,
            text="Welcome to Real Time Currency Convertor",
            fg="blue",
            relief=tk.RAISED,
            justify=tk.CENTER,
            borderwidth=3,
        )
        self.intro_label.config(font=("Manrope", 35, "bold"), padx=10, justify=CENTER)

        self.name_label = Label(
            self,
            text=f"Made by: Vikash (20BCA1508), Prabhat Singh (20BCA1552), Himanshi (20BCA1423)",
            fg="green",
            relief=tk.RAISED,
            justify=tk.CENTER,
            borderwidth=2,
        )
        self.name_label.config(
            font=("lucida", "12", "bold"), justify=CENTER, padx=7, pady=7
        )

        self.date_label = Label(
            self,
            text=f"1 Indian Rupee equals = {self.currency_converter.convert('INR','USD',1)} USD \n Last Updated : {self.currency_converter.data['time_last_update_utc'][:-15]}",
            relief=tk.GROOVE,
            borderwidth=2,
        )
        self.date_label.config(font="15", padx=5, pady=5)

        self.intro_label.place(x=40, y=10)
        self.name_label.place(x=200, y=80)
        self.date_label.place(x=400, y=130)

        # Entry box
        valid = (self.register(self.restrictNumberOnly), "%d", "%P")
        self.amount_field = Entry(
            self,
            bd=3,
            relief=tk.RIDGE,
            justify=tk.CENTER,
            validate="key",
            validatecommand=valid,
            width=18,
            font="20",
        )

        self.converted_amount_field_label = Label(
            self,
            text="",
            fg="black",
            bg="white",
            relief=tk.RIDGE,
            justify=tk.CENTER,
            width=18,
            borderwidth=3,
            font="20",
        )

        # dropdown
        self.from_currency_variable = StringVar(self)
        self.from_currency_variable.set("INR")  # default value
        self.to_currency_variable = StringVar(self)
        self.to_currency_variable.set("USD")  # default value

        font = ("Manrope", 12, "bold")
        self.option_add("*TCombobox*Listbox.font", font)
        self.from_currency_dropdown = ttk.Combobox(
            self,
            textvariable=self.from_currency_variable,
            values=list(self.currency_converter.currencies.keys()),
            font=font,
            state="readonly",
            width=16,
            justify=tk.CENTER,
        )

        self.to_currency_dropdown = ttk.Combobox(
            self,
            textvariable=self.to_currency_variable,
            values=list(self.currency_converter.currencies.keys()),
            font=font,
            state="readonly",
            width=16,
            justify=tk.CENTER,
        )

        # placing
        self.from_currency_dropdown.place(x=260, y=205)
        self.amount_field.place(x=260, y=240)
        self.to_currency_dropdown.place(x=620, y=205)
        self.converted_amount_field_label.place(x=620, y=240)

        # Convert button
        self.convert_button = Button(
            self, text="Convert", fg="black", command=self.perform
        )
        self.convert_button.config(font=("Manrope", 15, "bold"), padx=5, pady=5)
        self.convert_button.place(x=490, y=215)

    def perform(self):
        amount = float(self.amount_field.get())
        from_curr = self.from_currency_variable.get()
        to_curr = self.to_currency_variable.get()

        converted_amount = self.currency_converter.convert(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        self.converted_amount_field_label.config(text=str(converted_amount))

    def restrictNumberOnly(self, action, string):
        regex = re.compile(r"[0-9,]*?(\.)?[0-9,]*$")
        result = regex.match(string)
        return string == "" or (string.count(".") <= 1 and result is not None)


if __name__ == "__main__":
    url = "https://open.er-api.com/v6/latest/USD"
    converter = RealTimeCurrencyConverter(url)
    App(converter)
    mainloop()
