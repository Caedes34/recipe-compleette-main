import requests
import webbrowser
from io import BytesIO
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, Toplevel, Scrollbar, Frame

# Constants for recipe image dimensions
RECIPE_IMAGE_WIDTH = 100  # Thumbnail size
RECIPE_IMAGE_HEIGHT = 100
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
        self.search_button.place(x=584.0, y=81.0, width=42.0, height=38.0)
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
    
    
    
    # BACK END STUFF
    def __on_enter_pressed(self, event):
        self.__run_search_query()
     
    def __run_search_query(self):
        query = self.search_entry.get()
        recipes = self.__search_recipes(query)

        # Open results in a new window
        if recipes:
            self.__open_results_window(recipes)
        else:
            self.__open_results_window(None, message="No recipes found for your search.")

    def __open_results_window(self, recipes, message=""):
        # Create a new result window
        result_window = Toplevel(self.main_window)
        result_window.geometry("1441x800")
        result_window.configure(bg="#3E2929")

        # Create a frame and canvas for scrolling
        frame = Frame(result_window)
        frame.pack(fill="both", expand=True)

        canvas = Canvas(frame, bg="#3E2929", bd=0, highlightthickness=0, relief="ridge")
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview, 
                      bg="#555555",  # Color of the scrollbar itself
                      troughcolor="#888888",  # Color of the trough (area the slider moves in)
                      width=15)  # Increase the width to make the scrollbar more prominent
        scrollbar.pack(side="left", fill="y")


        canvas.config(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the recipe content
        content_frame = Frame(canvas, bg="#3E2929")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        def go_back():
            result_window.destroy()  # Close the results window and return to main search screen

        back_button = Button(content_frame, text="Back", command=go_back, bg="#f0ad4e", fg="white", relief="flat")
        back_button.grid(column=0, row=0, padx=20, pady=20)

        if recipes:
            row = 1
            for recipe in recipes:
                # Create a frame for each recipe to hold the image and title, and center the contents
                recipe_frame = Frame(content_frame, bg="#3E2929")
                recipe_frame.grid(row=row, column=0, padx=20, pady=10, sticky="nsew")

                # Centering the image and title within the recipe frame
                self.__show_recipe_thumbnail(recipe_frame, recipe['image'])
                
                # Create a button for the recipe title and center it
                recipe_button = Button(recipe_frame, text=recipe['title'], bg="#ffdada", relief="flat", command=lambda r=recipe: self.__open_recipe_details(r))
                recipe_button.pack(side="top", padx=10, pady=10, anchor="center")

                row += 1
        else:
            no_recipe_label = Label(content_frame, text=message, bg="#3E2929", fg="white")
            no_recipe_label.grid(column=0, row=1, pady=10)

        content_frame.update_idletasks()  
        canvas.config(scrollregion=canvas.bbox("all"))
        
    # Bind mouse wheel scrolling
        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        # Windows
        result_window.bind_all("<MouseWheel>", on_mouse_wheel)          

    def __open_recipe_details(self, recipe):
        # Retrieve full recipe details including ingredients
        full_recipe = self.__get_recipe_details(recipe['id'])

        if full_recipe:
            # Create a new window to show recipe details
            recipe_window = Toplevel(self.main_window)
            recipe_window.geometry("1441x800")
            recipe_window.configure(bg="#3E2929")

            content_frame = Frame(recipe_window, bg="#3E2929")
            content_frame.pack(fill="both", expand=True)

            # Show image
            self.__show_image(content_frame, full_recipe['image'])

            # Show ingredients and details
            self.__get_ingredients(content_frame, full_recipe)

            # Show the recipe source link button
            def __open_link():
                webbrowser.open(full_recipe.get('sourceUrl', ''))

            recipe_button = Button(content_frame, text="Recipe Link", highlightbackground="#ea86b6", command=__open_link)
            recipe_button.grid(row=3, column=0, pady=10)  # Use grid for positioning
        else:
            print("Failed to retrieve full recipe details.")

    def __search_recipes(self, query):
        url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&apiKey={self.recipe_app_key}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                # Return simplified recipe info (id, title, and image)
                recipes = [
                    {
                        'id': recipe['id'],
                        'title': recipe['title'],
                        'image': recipe['image']
                    }
                    for recipe in data['results']
                ]
                return recipes
        return []

    def __get_recipe_details(self, recipe_id):
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?apiKey={self.recipe_app_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        return None

    def __get_ingredients(self, frame, recipe):
        ingredients_text = Text(frame, height=15, width=50, bg="#ffdada")
        ingredients_text.grid(column=0, row=1, pady=10, padx=20) 
        ingredients_text.delete("1.0", "end")

        # Display recipe details and ingredients
        ingredients_text.insert("end", "\n" + recipe['title'] + "\n")
        ingredients_text.insert("end", f"\nServings: {recipe['servings']}\n")
        ingredients_text.insert("end", f"\nReady in: {recipe['readyInMinutes']} minutes\n")

        if 'extendedIngredients' in recipe:
            for ingredient in recipe['extendedIngredients']:
                ingredients_text.insert("end", "\n- " + ingredient['original'])

    def __show_image(self, frame, image_url):
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT))
        image = ImageTk.PhotoImage(img)

        holder = Label(frame, image=image)
        holder.photo = image  # Keep a reference to the image
        holder.grid(row=0, column=0, pady=10, padx=14)  # Use grid for proper positioning


    def __show_recipe_thumbnail(self, frame, image_url):
        # Load and resize the image to create a thumbnail
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((RECIPE_IMAGE_WIDTH, RECIPE_IMAGE_HEIGHT))  # Resize for thumbnail display
        image = ImageTk.PhotoImage(img)

        # Display the image as a thumbnail, centered in the frame
        label = Label(frame, image=image)
        label.photo = image  # Keep a reference to the image to avoid garbage collection
        label.pack(side="top", pady=10, anchor="center")

    def run_app(self):
        self.main_window.resizable(False, False)
        self.main_window.mainloop()

# Helper function to manage asset paths
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\angel\Downloads\recipe-compleette-main-main\recipe-compleette-main\build\assets\frame0")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Main execution
if __name__ == "__main__":
    recipe_app_key = "8b4d854f3bb446afa28109f20019f126"  
    recipe_app = RecipeApp(recipe_app_key)
    recipe_app.run_app()
