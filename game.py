import tkinter as tk
import random

class LifeSimulation:
    def __init__(self, root):
        self.root = root
        self.root.title("Life")

        self.grid = tk.Frame(root)
        self.grid.grid(row=2, column=0, padx=10, pady=10)

        self.log = tk.Listbox(root, width=40, height=10)
        self.log.grid(row=2, column=1, padx=10, pady=10)

        self.population_label = tk.Label(root, text="Population:")
        self.population_label.grid(row=3, column=0, sticky='w', padx=10)

        self.days_label = tk.Label(root, text="Days:")
        self.days_label.grid(row=3, column=0, sticky='e', padx=10)

        self.population_var = tk.StringVar()
        self.population_label_value = tk.Label(root, textvariable=self.population_var)
        self.population_label_value.grid(row=3, column=0, sticky='w', padx=95)

        self.days_var = tk.StringVar()
        self.days_label_value = tk.Label(root, textvariable=self.days_var)
        self.days_label_value.grid(row=3, column=0, sticky='e', padx=95)

        self.feed_button = tk.Button(root, text="Feed", command=self.feed)
        self.feed_button.grid(row=4, column=0, padx=10, pady=10)

        self.size = 12 * 9
        self.cells = [None] * self.size
        self.generation = 0

        self.init_grid()
        self.init_cells()

    def init_grid(self):
        for i in range(self.size):
            li = tk.Label(self.grid, text=i, relief='solid', width=3, height=1, bg='green')
            li.grid(row=i // 12, column=i % 12, padx=1, pady=1)
            self.cells[i] = li

    def init_cells(self):
        random_cells = self.pick6random_cells()
        for index in random_cells:
            self.cells[index].configure(bg='red')

    def get_neighbors(self, index):
        neighbors = []
        row = index // 12
        col = index % 12
        top = row - 1
        bottom = row + 1
        left = col - 1
        right = col + 1

        if top >= 0:
            neighbors.append(top * 12 + col)
        if bottom < 9:
            neighbors.append(bottom * 12 + col)
        if left >= 0:
            neighbors.append(row * 12 + left)
        if right < 12:
            neighbors.append(row * 12 + right)
        if top >= 0 and left >= 0:
            neighbors.append(top * 12 + left)
        if top >= 0 and right < 12:
            neighbors.append(top * 12 + right)
        if bottom < 9 and left >= 0:
            neighbors.append(bottom * 12 + left)
        if bottom < 9 and right < 12:
            neighbors.append(bottom * 12 + right)

        return neighbors

    def pick6random_cells(self):
        return random.sample(range(self.size), 6)

    def feed(self):
        for index, cell in enumerate(self.cells):
            if cell['bg'] == 'red':
                live_neighbors = self.get_live_neighbors(index)
                food_neighbors = [i for i in self.get_neighbors(index) if self.cells[i]['bg'] == 'green']

                if food_neighbors:
                    random_index = random.choice(food_neighbors)
                    self.cells[random_index].configure(bg='red')
                    self.cells[index].configure(bg='green')
                    self.update_log(f"Cell {index} ate cell {random_index}.")

                elif not live_neighbors:
                    self.cells[index].configure(bg='green')
                    self.update_log(f"Cell {index} died of hunger.")

        self.reproduce()
        self.update()

    def get_live_neighbors(self, index):
        neighbors = self.get_neighbors(index)
        return [i for i in neighbors if self.cells[i]['bg'] == 'red']

    def reproduce(self):
        for index, cell in enumerate(self.cells):
            if cell['bg'] == 'red':
                live_neighbors = self.get_live_neighbors(index)
                if live_neighbors:
                    random_index = random.choice(live_neighbors)
                    self.cells[random_index].configure(bg='red')
                    self.update_log(f"Cells {index} gave birth to {random_index}.")

    def update(self):
        live_cells = sum(1 for cell in self.cells if cell['bg'] == 'red')
        population = tk.StringVar(value=live_cells)
        self.population_var.set(population)

        days = tk.StringVar(value=self.generation + 1)
        self.days_var.set(days)
        self.generation += 1

        if live_cells == 0:
            self.update_log(f"All cells died after {days.get()} days.")
            self.feed_button.configure(state='disabled')

    def update_log(self, message):
        self.log.insert(tk.END, message)
        self.log.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    life_simulation = LifeSimulation(root)
    root.mainloop()
