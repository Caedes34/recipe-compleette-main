import requests 
import webbrowser
from io import BytesIO
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, Toplevel, Scrollbar, Frame

# Constants for recipe image dimensions
RECIPE_IMAGE_WIDTH = 200
RECIPE_IMAGE_HEIGHT = 200
image_url = "" 
canvas_width = 747
center_x = canvas_width / 2

class RecipeApp:
    def __init__(self, recipe_app_key):
        self.recipe_app_key = recipe_app_key

        # Main Window
        self.main_window = Tk()
        self.main_window.geometry("747x504")
        self.main_window.configure(bg="#A46D6D")
        
        self.canvas = Canvas(
            self.main_window,
            bg="#A46D6D",
            height=504,
            width=747,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Search text label
        self.canvas.create_text(
            center_x, 
            20.0,
            anchor="center",
            text="Whats Cookin?",
            fill="#CC9318",
            font=("Montserrat Bold", 36)
        )

        # Search entry background and entry field
        self.button_image_1 = PhotoImage(file=relative_to_assets("entry_1.png"))
        self.search_entry = Entry(self.main_window, bd=0, bg="#D9D9D9", fg="#000716", highlightthickness=0)
        self.search_entry.place(x=123.0, y=81.0, width=502.0, height=38.0)


        # Search button
        self.button_image_1 = PhotoImage(file=relative_to_assets("button_7.png"))
        self.button_image_1 = self.button_image_1.subsample(3, 3) 
        self.search_button = Button(
            self.main_window,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=self.__run_search_query,
            relief="flat"
        )
        self.search_button.place(x=584.0, y=81.0, width=42.0, height=38.)
        self.search_entry.bind("<Return>", self.__on_enter_pressed)

        

        def load_image(file_path, size=(278, 92)): 
            img = Image.open(file_path)
            img = img.resize(size)  
            return ImageTk.PhotoImage(img)

        button_image_1 = load_image(relative_to_assets("button_1.png"))
        button_1 = Button(
            self.main_window,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat",
            bg="#A46D6D",
            bd=0,
            padx=0,
            pady=0
        )
        button_1.image = button_image_1
        button_1.place(x=47.0, y=132.0, width=278.0, height=92.0)

        button_image_2 = load_image(relative_to_assets("button_2.png"))
        button_2 = Button(
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat",
            bg="#A46D6D", 
            activebackground="#A46D6D",  
            bd=0,  
            padx=0, 
            pady=0   
        )
        button_2.image = button_image_2
        button_2.place(
            x=47.0,
            y=240.0,
            width=278.0,  
            height=92.0  
        )

        button_image_3 = load_image(relative_to_assets("button_3.png"))
        button_3 = Button(
            image=button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat",
            bg="#A46D6D",  
            activebackground="#A46D6D",  
            bd=0,  
            padx=0,  
            pady=0  
        )
        button_3.image = button_image_3
        button_3.place(
            x=47.0,
            y=359.0,
            width=278.0,  
            height=92.0  
        )

        button_image_4 = load_image(relative_to_assets("button_4.png"))

        button_4 = Button(
            image=button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat",
            bg="#A46D6D",  
            activebackground="#A46D6D",
            bd=0,  
            padx=0,  
            pady=0   
        )
        button_4.image = button_image_4
        button_4.place(
            x=395.0,
            y=132.0,
            width=278.0,  
            height=92.0  
        )

        button_image_5 =  load_image(relative_to_assets("button_5.png"))
        button_5 = Button(
            image=button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat",
            bg="#A46D6D",  
            activebackground="#A46D6D",  
            bd=0, 
            padx=0,  
            pady=0   
        )
        button_5.image = button_image_5
        button_5.place(
            x=395.0,
            y=248.0,
            width=278.0,  
            height=92.0  
        )

        button_image_6 =  load_image(relative_to_assets("button_6.png"))
        button_6 = Button(
            image=button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat",
            bg="#A46D6D",  
            activebackground="#A46D6D",  
            bd=0,  
            padx=0,  
            pady=0   
        )
        button_6.image = button_image_6
        button_6.place(
            x=395.0,
            y=355.0,
            width=278.0,  
            height=92.0  
        )

    #BACK END STUFFS
    def __on_enter_pressed(self, event):
        self.__run_search_query()
     

    def __run_search_query(self):
        query = self.search_entry.get()
        recipe = self.__get_recipe(query)

        # Open results in a new window
        if recipe:
            self.__open_results_window(recipe)
        else:
            self.__open_results_window(None, message="No Recipe found for search criteria")

    def __open_results_window(self, recipe, message=""):
        # Create a new result window
        result_window = Toplevel(self.main_window)
        result_window.geometry("1441x800")
        result_window.configure(bg="#3E2929")

        # Create a frame and canvas for scrolling
        frame = Frame(result_window)
        frame.pack(fill="both", expand=True)

        canvas = Canvas(frame, bg="#3E2929", bd=0, highlightthickness=0, relief="ridge")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the recipe content
        content_frame = Frame(canvas, bg="#3E2929")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

       
        if recipe:
            recipe_image = recipe['image']
            recipe_url = recipe.get('sourceUrl', "")

            # Display recipe image
            self.__show_image(content_frame, recipe_image)

            # Display ingredients and recipe details
            self.__get_ingredients(content_frame, recipe)
            
            # Recipe link button
            def __open_link():
                if recipe_url:
                    webbrowser.open(recipe_url)
            recipe_button = Button(content_frame, text="Recipe Link", highlightbackground="#ea86b6", command=__open_link)
            recipe_button.grid(column=1, row=7, pady=10)
        else:
            # Display message if no recipe is found

            no_recipe_label = Label(content_frame, text=message, bg="#3E2929", fg="white")
            no_recipe_label.grid(column=1, row=4, pady=10)


            
            placeholder_image_url = "https://www.creta-gel.com/page-404.html"  
            self.__show_image(content_frame, placeholder_image_url)

        
        content_frame.update_idletasks()  
        canvas.config(scrollregion=canvas.bbox("all"))
     # Handle the enter key event
    def __on_enter_pressed(self, event):
        self.__run_search_query()

    # Handle search query and display results
    def __run_search_query(self):
        query = self.search_entry.get()
        recipes = self.__get_recipes(query)

        # Show results in a new window
        if recipes:
            self.__open_results_window(recipes)
        else:
            self.__open_results_window([], message="No recipes found for your search.")

    # Open the results window with a list of recipes
    def __open_results_window(self, recipes, message=""):
        result_window = Toplevel(self.main_window)
        result_window.geometry("1441x800")
        result_window.configure(bg="#3E2929")

        frame = Frame(result_window)
        frame.pack(fill="both", expand=True)

        canvas = Canvas(frame, bg="#3E2929", bd=0, highlightthickness=0, relief="ridge")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.config(yscrollcommand=scrollbar.set)

        content_frame = Frame(canvas, bg="#3E2929")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        if recipes:
            # Display a list of recipes
            for index, recipe in enumerate(recipes):
                self.__create_recipe_button(content_frame, recipe, index)
        else:
            no_recipe_label = Label(content_frame, text=message, bg="#3E2929", fg="white")
            no_recipe_label.grid(column=1, row=4, pady=10)

        content_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    # Create a button for each recipe in the list
    def __create_recipe_button(self, frame, recipe, index):
        button = Button(frame, text=recipe['title'], command=lambda r=recipe: self.__open_recipe_details(r))
        button.grid(column=1, row=index, pady=5)

    # Open the recipe details when a recipe is selected
    def __open_recipe_details(self, recipe):
        recipe_window = Toplevel(self.main_window)
        recipe_window.geometry("1441x800")
        recipe_window.configure(bg="#3E2929")

        content_frame = Frame(recipe_window, bg="#3E2929")
        content_frame.pack(fill="both", expand=True)

        self.__show_image(content_frame, recipe['image'])

        self.__get_ingredients(content_frame, recipe)

        # Recipe link button
        def __open_link():
            webbrowser.open(recipe.get('sourceUrl', ''))
        recipe_button = Button(content_frame, text="Recipe Link", highlightbackground="#ea86b6", command=__open_link)
        recipe_button.grid(column=1, row=7, pady=10)

    # Get multiple recipes based on query
    def __get_recipes(self, query):
        url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={self.recipe_app_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data.get('results', [])
        return []

    def __show_image(self, frame, image_url):
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT))
        image = ImageTk.PhotoImage(img)

        holder = Label(frame, image=image)
        holder.photo = image
        holder.grid(column=1, row=6, pady=10)

    def __get_ingredients(self, frame, recipe):
        ingredients_text = Text(frame, height=15, width=50, bg="#ffdada")
        ingredients_text.grid(column=1, row=4, pady=10)
        ingredients_text.delete("1.0", "end")

        ingredients_text.insert("end", "\n" + recipe['title'] + "\n")
        ingredients_text.insert("end", f"\nServings: {recipe['servings']}\n")
        ingredients_text.insert("end", f"\nReady in: {recipe['readyInMinutes']} minutes\n")

        if 'extendedIngredients' in recipe:
            for ingredient in recipe['extendedIngredients']:
                ingredients_text.insert("end", "\n- " + ingredient['original'])    

    def __get_recipe(self, query):
        url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={self.recipe_app_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                recipe_id = data['results'][0]['id']
                return self.__get_recipe_details(recipe_id)
        return None

    def __get_recipe_details(self, recipe_id):
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={self.recipe_app_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        return None

    def __show_image(self, frame, image_url):
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT))
        image = ImageTk.PhotoImage(img)

        holder = Label(frame, image=image)
        holder.photo = image  
        holder.grid(column=1, row=6, pady=10)
        

    def __get_ingredients(self, frame, recipe):
        ingredients_text = Text(frame, height=15, width=50, bg="#ffdada")
        ingredients_text.grid(column=1, row=4, pady=10)
        ingredients_text.delete("1.0", "end")

        # Display recipe details and ingredients
        ingredients_text.insert("end", "\n" + recipe['title'] + "\n")
        ingredients_text.insert("end", f"\nServings: {recipe['servings']}\n")
        ingredients_text.insert("end", f"\nReady in: {recipe['readyInMinutes']} minutes\n")

        if 'extendedIngredients' in recipe:
            for ingredient in recipe['extendedIngredients']:
                ingredients_text.insert("end", "\n- " + ingredient['original'])

    def run_app(self):
        self.main_window.resizable(False, False)
        self.main_window.mainloop()

# Helper function to manage asset paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Admin\Downloads\recipe-compleette-main\recipe-compleette-main\build\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Main execution
if __name__ == "__main__":
    recipe_app_key = "8b4d854f3bb446afa28109f20019f126"  
    recipe_app = RecipeApp(recipe_app_key)
    recipe_app.run_app()
