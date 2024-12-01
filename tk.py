import tkinter as tk
import tkinter.ttk as ttk  # для стилизации
import requests
import json

def get_animals():
    try:
        response = requests.get("http://127.0.0.1:5001/animals")       
        response.raise_for_status()
        animals = json.loads(response.text)
        animal_listbox.delete(0, tk.END)
        for animal in animals:
            animal_listbox.insert(tk.END, animal['name'])
    except requests.exceptions.RequestException as e:
        show_error(f"Error fetching animals: {e}")

def show_animal_details():
    try:
        selected_animal = animal_listbox.get(animal_listbox.curselection())
        response = requests.get(f"http://127.0.0.1:5000/animals/{selected_animal}")
        response.raise_for_status()
        animal_details = json.loads(response.text)
        details_text.delete("1.0", tk.END)  # Очистка текстового поля
        details_text.insert(tk.END, json.dumps(animal_details, indent=2))
    except requests.exceptions.RequestException as e:
        show_error(f"Error fetching details: {e}")
    except (IndexError, json.JSONDecodeError):
        show_error("Please select an animal.")

def show_error(message):
    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, message)


root = tk.Tk()
root.title("Animals Database")
root.style = ttk.Style()
root.style.theme_use('clam') # или другой стиль, если доступен


main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

get_button = ttk.Button(main_frame, text="Get Animals", command=get_animals)
get_button.grid(row=0, column=0, pady=5)

animal_listbox = tk.Listbox(main_frame, width=30)
animal_listbox.grid(row=1, column=0, pady=5)

details_frame = ttk.LabelFrame(main_frame, text="Details", padding="10")
details_frame.grid(row=0, column=1, rowspan=2, padx=10, sticky=(tk.N, tk.S, tk.E, tk.W))

details_text = tk.Text(details_frame, wrap=tk.WORD, height=10, width=40)
details_text.pack()

show_details_button = ttk.Button(main_frame, text="Show Details", command=show_animal_details)
show_details_button.grid(row=2, column=0, pady=5)

root.mainloop()