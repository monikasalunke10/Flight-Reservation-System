import tkinter as tk
from tkinter import ttk, messagebox
import random
import string

# Flight data
flights = [
    {"flight_no": "AI101", "airline": "Air India", "source": "Pune", "destination": "Delhi", "price": 4500},
    {"flight_no": "6E202", "airline": "IndiGo", "source": "Pune", "destination": "Delhi", "price": 3800},
    {"flight_no": "QP303", "airline": "Akasa Air", "source": "Mumbai", "destination": "Bengaluru", "price": 5200},
    {"flight_no": "AI404", "airline": "Air India", "source": "Pune", "destination": "Goa", "price": 3200},
    {"flight_no": "6E505", "airline": "IndiGo", "source": "Mumbai", "destination": "Delhi", "price": 4100},
    {"flight_no": "AI606", "airline": "Air India", "source": "Delhi", "destination": "Mumbai", "price": 4700},
    {"flight_no": "QP707", "airline": "Akasa Air", "source": "Pune", "destination": "Bengaluru", "price": 5000},
    {"flight_no": "6E808", "airline": "IndiGo", "source": "Bengaluru", "destination": "Delhi", "price": 4300},
    {"flight_no": "AI909", "airline": "Air India", "source": "Mumbai", "destination": "Goa", "price": 3600},
    {"flight_no": "6E110", "airline": "IndiGo", "source": "Pune", "destination": "Hyderabad", "price": 3500},
    {"flight_no": "QP211", "airline": "Akasa Air", "source": "Delhi", "destination": "Bengaluru", "price": 4900},
    {"flight_no": "AI312", "airline": "Air India", "source": "Hyderabad", "destination": "Mumbai", "price": 4000},
]

bookings = []


def linear_search(data, flight_number):
    for flight in data:
        if flight["flight_no"].lower() == flight_number.strip().lower():
            return flight
    return None


def bubble_sort(data, key, descending=False):
    result = data[:]
    n = len(result)

    for i in range(n - 1):
        swapped = False
        for j in range(n - i - 1):
            left = result[j][key]
            right = result[j + 1][key]

            if (left < right and descending) or (
                left > right and not descending
            ):
                result[j], result[j + 1] = result[j + 1], result[j]
                swapped = True

        if not swapped:
            break

    return result


BG = "#eef3f9"
NAVY = "#102a43"
BLUE = "#1976d2"
WHITE = "#ffffff"
TEXT = "#243b53"
MUTED = "#627d98"


class FlightReservationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SkyBook | Flight Reservation System")
        self.root.geometry("1120x760")
        self.root.minsize(980, 680)
        self.root.configure(bg=BG)

        self.selected_flight = None
        self.filtered_flights = flights[:]

        self.setup_styles()
        self.build_ui()
        self.refresh_flights()

    def setup_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "Treeview",
            font=("Segoe UI", 10),
            rowheight=30,
            background=WHITE,
            fieldbackground=WHITE,
            foreground=TEXT
        )

        style.configure(
            "Treeview.Heading",
            font=("Segoe UI", 10, "bold"),
            background="#d9e8f7",
            foreground=NAVY,
            padding=8
        )

        style.map(
            "Treeview",
            background=[("selected", "#c8e2ff")],
            foreground=[("selected", NAVY)]
        )

        style.configure("TCombobox", padding=5)

    def build_ui(self):
        header = tk.Frame(self.root, bg=NAVY, height=94)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="✈  SKYBOOK",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w", padx=25, pady=(14, 0))

        tk.Label(
            header,
            text="FLIGHT RESERVATION SYSTEM ",
            bg=NAVY,
            fg="#c6dcf2",
            font=("Segoe UI", 10)
        ).pack(anchor="w", padx=29)

        main = tk.Frame(self.root, bg=BG, padx=20, pady=15)
        main.pack(fill="both", expand=True)

        filter_card = tk.Frame(
            main,
            bg=WHITE,
            padx=14,
            pady=12,
            highlightbackground="#d7e2ee",
            highlightthickness=1
        )
        filter_card.pack(fill="x")

        tk.Label(
            filter_card,
            text="Find your flight",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).grid(row=0, column=0, columnspan=6,
               sticky="w", pady=(0, 9))

        tk.Label(
            filter_card, text="Flight No.",
            bg=WHITE, fg=MUTED
        ).grid(row=1, column=0, sticky="w")

        self.search_var = tk.StringVar()

        tk.Entry(
            filter_card,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
            width=16
        ).grid(row=2, column=0, padx=(0, 10), sticky="ew")

        tk.Label(
            filter_card, text="From",
            bg=WHITE, fg=MUTED
        ).grid(row=1, column=1, sticky="w")

        self.from_var = tk.StringVar(value="All")
        self.from_box = ttk.Combobox(
            filter_card,
            textvariable=self.from_var,
            state="readonly",
            width=13
        )
        self.from_box.grid(row=2, column=1, padx=(0, 10), sticky="ew")

        tk.Label(
            filter_card, text="To",
            bg=WHITE, fg=MUTED
        ).grid(row=1, column=2, sticky="w")

        self.to_var = tk.StringVar(value="All")
        self.to_box = ttk.Combobox(
            filter_card,
            textvariable=self.to_var,
            state="readonly",
            width=13
        )
        self.to_box.grid(row=2, column=2, padx=(0, 10), sticky="ew")

        tk.Label(
            filter_card, text="Airline",
            bg=WHITE, fg=MUTED
        ).grid(row=1, column=3, sticky="w")

        self.airline_var = tk.StringVar(value="All")
        self.airline_box = ttk.Combobox(
            filter_card,
            textvariable=self.airline_var,
            state="readonly",
            width=13
        )
        self.airline_box.grid(row=2, column=3, padx=(0, 10), sticky="ew")

        tk.Label(
            filter_card, text="Sort by",
            bg=WHITE, fg=MUTED
        ).grid(row=1, column=4, sticky="w")

        self.sort_var = tk.StringVar(
            value="Price: Low to High"
        )

        self.sort_box = ttk.Combobox(
            filter_card,
            textvariable=self.sort_var,
            state="readonly",
            values=[
                "Price: Low to High",
                "Price: High to Low",
                "Flight Number",
                "Airline"
            ],
            width=19
        )
        self.sort_box.grid(row=2, column=4, padx=(0, 10), sticky="ew")

        button_area = tk.Frame(filter_card, bg=WHITE)
        button_area.grid(row=2, column=5, sticky="e")

        tk.Button(
            button_area,
            text="Search / Apply",
            command=self.refresh_flights,
            bg=BLUE,
            fg=WHITE,
            activebackground="#125da8",
            activeforeground=WHITE,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="left", padx=(0, 6))

        tk.Button(
            button_area,
            text="Reset",
            command=self.reset_filters,
            bg="#e8eef5",
            fg=NAVY,
            relief="flat",
            padx=12,
            pady=7,
            cursor="hand2"
        ).pack(side="left")

        for col in range(5):
            filter_card.grid_columnconfigure(col, weight=1)

        # Available flights table
        table_card = tk.Frame(
            main,
            bg=WHITE,
            padx=14,
            pady=12,
            highlightbackground="#d7e2ee",
            highlightthickness=1
        )
        table_card.pack(fill="both", expand=True, pady=(14, 12))

        title_row = tk.Frame(table_card, bg=WHITE)
        title_row.pack(fill="x", pady=(0, 9))

        tk.Label(
            title_row,
            text="Available Flights",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 14, "bold")
        ).pack(side="left")

        self.count_label = tk.Label(
            title_row,
            text="",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        )
        self.count_label.pack(side="right")

        columns = (
            "flight_no", "airline", "source",
            "destination", "price"
        )

        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "flight_no": "FLIGHT NO.",
            "airline": "AIRLINE",
            "source": "FROM",
            "destination": "TO",
            "price": "FARE (₹)"
        }

        widths = {
            "flight_no": 130,
            "airline": 190,
            "source": 170,
            "destination": 170,
            "price": 130
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind(
            "<<TreeviewSelect>>",
            self.on_flight_select
        )

        # Passenger details section
        passenger_card = tk.Frame(
            main,
            bg=WHITE,
            padx=14,
            pady=12,
            highlightbackground="#d7e2ee",
            highlightthickness=1
        )
        passenger_card.pack(fill="x")

        tk.Label(
            passenger_card,
            text="Passenger Details & Booking",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 13, "bold")
        ).grid(
            row=0, column=0, columnspan=5,
            sticky="w", pady=(0, 9)
        )

        tk.Label(
            passenger_card,
            text="Passenger Name *",
            bg=WHITE,
            fg=MUTED
        ).grid(row=1, column=0, sticky="w")

        self.name_var = tk.StringVar()

        tk.Entry(
            passenger_card,
            textvariable=self.name_var,
            width=24,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        ).grid(
            row=2, column=0,
            padx=(0, 15), sticky="ew"
        )

        tk.Label(
            passenger_card,
            text="Age *",
            bg=WHITE,
            fg=MUTED
        ).grid(row=1, column=1, sticky="w")

        self.age_var = tk.StringVar()

        tk.Entry(
            passenger_card,
            textvariable=self.age_var,
            width=10,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        ).grid(
            row=2, column=1,
            padx=(0, 15), sticky="ew"
        )

        tk.Label(
            passenger_card,
            text="Phone (optional)",
            bg=WHITE,
            fg=MUTED
        ).grid(row=1, column=2, sticky="w")

        self.phone_var = tk.StringVar()

        tk.Entry(
            passenger_card,
            textvariable=self.phone_var,
            width=20,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1
        ).grid(
            row=2, column=2,
            padx=(0, 15), sticky="ew"
        )

        self.selected_label = tk.Label(
            passenger_card,
            text="Select a flight from the table",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        )

        self.selected_label.grid(
            row=2, column=3,
            sticky="w", padx=(0, 10)
        )

        tk.Button(
            passenger_card,
            text="✈  Book Selected Flight",
            command=self.book_ticket,
            bg="#16805d",
            fg=WHITE,
            activebackground="#11684c",
            activeforeground=WHITE,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            padx=17,
            pady=9,
            cursor="hand2"
        ).grid(row=2, column=4, sticky="e")

        for col in range(4):
            passenger_card.grid_columnconfigure(col, weight=1)

        tk.Label(
            main,
            text=(
                "Academic demonstration only • "
                "Sample flight data • No real booking or payment"
            ),
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="center", pady=(8, 0))

        # Fill dropdown options
        locations = sorted(
            {f["source"] for f in flights}
            | {f["destination"] for f in flights}
        )

        self.from_box["values"] = ["All"] + locations
        self.to_box["values"] = ["All"] + locations

        self.airline_box["values"] = (
            ["All"]
            + sorted({f["airline"] for f in flights})
        )

    def refresh_flights(self):
        data = flights[:]
        query = self.search_var.get().strip().lower()

        if query:
            data = [
                f for f in data
                if query in f["flight_no"].lower()
            ]

        if self.from_var.get() != "All":
            data = [
                f for f in data
                if f["source"] == self.from_var.get()
            ]

        if self.to_var.get() != "All":
            data = [
                f for f in data
                if f["destination"] == self.to_var.get()
            ]

        if self.airline_var.get() != "All":
            data = [
                f for f in data
                if f["airline"] == self.airline_var.get()
            ]

        sort_choice = self.sort_var.get()

        if sort_choice == "Price: Low to High":
            data = bubble_sort(data, "price")

        elif sort_choice == "Price: High to Low":
            data = bubble_sort(
                data, "price", descending=True
            )

        elif sort_choice == "Flight Number":
            data = bubble_sort(data, "flight_no")

        elif sort_choice == "Airline":
            data = bubble_sort(data, "airline")

        self.filtered_flights = data

        for item in self.tree.get_children():
            self.tree.delete(item)

        for flight in data:
            self.tree.insert(
                "",
                "end",
                values=(
                    flight["flight_no"],
                    flight["airline"],
                    flight["source"],
                    flight["destination"],
                    f'{flight["price"]:,}'
                )
            )

        self.count_label.config(
            text=f"{len(data)} flight(s) found"
        )

        self.selected_flight = None

        self.selected_label.config(
            text="Select a flight from the table",
            fg=MUTED
        )

    def reset_filters(self):
        self.search_var.set("")
        self.from_var.set("All")
        self.to_var.set("All")
        self.airline_var.set("All")

        self.sort_var.set("Price: Low to High")
        self.refresh_flights()

    def on_flight_select(self, event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")

        self.selected_flight = linear_search(
            flights, values[0]
        )

        if self.selected_flight:
            f = self.selected_flight
            self.selected_label.config(
                text=f'Selected: {f["flight_no"]} • ₹{f["price"]:,}',
                fg=BLUE
            )

    def book_ticket(self):
        if not self.selected_flight:
            messagebox.showwarning(
                "Select Flight",
                "Please select a flight from the table first."
            )
            return

        name = self.name_var.get().strip()
        age_text = self.age_var.get().strip()
        phone = self.phone_var.get().strip()

        if not name:
            messagebox.showerror(
                "Missing Details",
                "Please enter the passenger name."
            )
            return

        try:
            age = int(age_text)
            if not 1 <= age <= 120:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Age",
                "Please enter an age between 1 and 120."
            )
            return

        if phone and (
            not phone.isdigit() or not 7 <= len(phone) <= 15
        ):
            messagebox.showerror(
                "Invalid Phone",
                "Phone must contain 7 to 15 digits."
            )
            return

        booking_id = "SKY" + "".join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=6
            )
        )

        flight = self.selected_flight

        bookings.append({
            "booking_id": booking_id,
            "passenger": name,
            "age": age,
            "phone": phone,
            "flight": flight["flight_no"],
            "fare": flight["price"]
        })

        messagebox.showinfo(
            "Booking Confirmed",
            f"BOOKING CONFIRMED \n\n"
            f"Booking ID: {booking_id}\n"
            f"Passenger: {name}\n"
            f"Age: {age}\n"
            f"Flight: {flight['flight_no']} - {flight['airline']}\n"
            f"Route: {flight['source']} to {flight['destination']}\n"
            f"Fare: ₹{flight['price']:,}\n\n"
            "This is an academic demo. "
            "No real ticket or payment was created."
        )


if __name__ == "__main__":
    root = tk.Tk()
    app = FlightReservationApp(root)
    root.mainloop() 