import tkinter as tk
import tkinter.ttk as ttk
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
    except requests.exceptions.RequestException:
        show_error("Ошибка при получении животных")

def show_animal_details():
    try:
        selected_animal = animal_listbox.get(animal_listbox.curselection())
        response = requests.get(f"http://127.0.0.1:5001/animals/{selected_animal}")
        response.raise_for_status()
        animal_details = json.loads(response.text)
        
        details_text.delete("1.0", tk.END) 
        
        if isinstance(animal_details, list) and len(animal_details) > 0:
            # если конечности существуют
            unique_appendages = set()
            animal_name = animal_details[0]['animal_name']
            
            for detail in animal_details:
                appendage_type = detail['appendage_type']
                if appendage_type is not None:
                    unique_appendages.add((appendage_type, detail['appendage_count']))
            
            details_text.insert(tk.END, f"Животное: {animal_name}\n")
            
            if unique_appendages:
                for appendage_type, count in unique_appendages:
                    details_text.insert(tk.END, f"Тип конечности: {appendage_type}\n")
                    details_text.insert(tk.END, f"Количество: {count}\n\n")
            else:
                details_text.insert(tk.END, "Нет конечностей.\n")
        else:
            details_text.insert(tk.END, "Детали не найдены.")
    
    except requests.exceptions.RequestException:
        show_error("Ошибка при получении деталей")
    except (IndexError, json.JSONDecodeError):
        show_error("Пожалуйста, выберите животное.")

def show_error(message):
    details_text.delete("1.0", tk.END)
    details_text.insert(tk.END, message)

root = tk.Tk()
root.title("База данных животных")
root.style = ttk.Style()
root.style.theme_use('clam') 

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))

get_button = ttk.Button(main_frame, text="Получить животных", command=get_animals)
get_button.grid(row=0, column=0, pady=5)

animal_listbox = tk.Listbox(main_frame, width=30)
animal_listbox.grid(row=1, column=0, pady=5)

details_frame = ttk.LabelFrame(main_frame, text="Детали", padding="10")
details_frame.grid(row=0, column=1, rowspan=2, padx=10, sticky=(tk.N, tk.S, tk.E, tk.W))

details_text = tk.Text(details_frame, wrap=tk.WORD, height=10, width=40)
details_text.pack()

# показ деталей выбранного животного
show_details_button = ttk.Button(main_frame, text="Показать детали", command=show_animal_details)
show_details_button.grid(row=2, column=0, pady=5)

root.mainloop()