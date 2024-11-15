import requests
import webbrowser
from io import BytesIO
from PIL import Image, ImageTk
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Label, Toplevel, Scrollbar, Frame
import re
# Constants for recipe image dimensions
RECIPE_IMAGE_WIDTH = 200  # Thumbnail size
RECIPE_IMAGE_HEIGHT = 200  # Thumbnail size
custom_width = 400  # For example, 400 pixels wide
custom_height = 300 #For example, 300 pixels high
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
                command=lambda:  self.__search_and_display_results("Soup"),
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
                command=lambda: self.__search_and_display_results("Desserts"),
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
                command=lambda: self.__search_and_display_results("Main Course"),
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
                command=lambda:  self.__search_and_display_results("BreakFast"),
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
                command=lambda: self.__search_and_display_results("Drinks"),
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
                command=lambda: self.__search_and_display_results("Snacks"),
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
    
    
    
    # BACK END STUFF!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
        result_window.geometry("747x504")
        result_window.configure(bg="#FCF9F5")  # Consistent background color

        # Create a Frame to hold the canvas and scrollbar
        frame = Frame(result_window)
        frame.pack(fill="both", expand=True)

        # Create a canvas widget with a vertical scrollbar
        canvas = Canvas(
            frame,
            bg="#FCF9F5",
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )

        scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Create a frame inside the canvas to hold the recipe content
        content_frame = Frame(canvas, bg="#FCF9F5")
        canvas.create_window((0, 0), window=content_frame, anchor="nw")

        # Add message if no recipes are found
        if not recipes:
            no_recipe_label = Label(content_frame, text=message, bg="#FCF9F5", fg="#1F1D1B", font=("SpaceGrotesk Medium", 18))
            no_recipe_label.grid(column=0, row=0, pady=50, padx=20)

        # Add recipe buttons if there are any
        else:
            row = 1
            for recipe in recipes:
                # Create a frame for each recipe to hold the image and title
                recipe_frame = Frame(content_frame, bg="#FCF9F5")
                recipe_frame.grid(row=row, column=0, padx=20, pady=10, sticky="nsew")

                # Show the recipe image as a thumbnail
                self.__show_recipe_thumbnail(recipe_frame, recipe['image'])

                # Create a button for the recipe title
                recipe_button = Button(
                    recipe_frame,
                    text=recipe['title'],
                    bg="#FFDADA",  # Background color for the button
                    fg="#1F1D1B",  # Text color
                    relief="flat",
                    font=("SpaceGrotesk Medium", 16),
                    command=lambda r=recipe: self.__open_recipe_details(r)  # Open recipe details when clicked
                )
                recipe_button.pack(side="top", padx=10, pady=10, anchor="center")

                row += 1
            # ---- Back Button Code ----
            back_button = Button(content_frame, text="Back", highlightbackground="#ea86b6", command=result_window.destroy)
            back_button.place(x=10, y=10)         

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
            recipe_window.geometry("1703x1580")
            recipe_window.configure(bg="#FDFAF5")

            content_frame = Frame(recipe_window, bg="#FDFAF5")
            content_frame.pack(fill="both", expand=False)

            # Show image
            self.__show_image(content_frame, full_recipe['image'])

            # Show ingredients and details in a single text field
            self.__show_recipe_details(content_frame, full_recipe)

            # Show the recipe source link button
            def __open_link():
                webbrowser.open(full_recipe.get('sourceUrl', ''))

            recipe_button = Button(content_frame, text="Recipe Link", highlightbackground="#ea86b6", command=__open_link)
            recipe_button.grid(row=3, column=0, pady=10)  # Use grid for positioning
        else:
            print("Failed to retrieve full recipe details.")
        # Retrieves simplified recipe info (id, title, and image)
    def __search_recipes(self, query):# MODIFY API CALL RESULTS
        url = f"https://api.spoonacular.com/recipes/complexSearch?query={query}&number=1&apiKey={self.recipe_app_key}"
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
    
    # Retrieves full recipe details including ingredients
    def __get_recipe_details(self, recipe_id):
        url = f"https://api.spoonacular.com/recipes/{recipe_id}/information?includeNutrition=true&apiKey={self.recipe_app_key}"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        return None
    
    #shows ingredients and details
    def __show_recipe_details(self, frame, recipe):
        
        title_label = Label(frame, text=recipe['title'], font=("Helvetica", 18, "bold"), bg="#FDFAF5")
        title_label.grid(row=0, column=0, columnspan=3, pady=10, sticky="n")  # Columnspan makes it center aligned
        # Create a single Text widget to display all details
        recipe_details_text = Text(frame, height=30, width=50, bg="#FDFAF5", wrap="word")
        recipe_details_text.grid(column=10, row=0, pady=10, padx=12)  # Adjust positioning as needed
        recipe_details_text.delete("1.0", "end")  # Clear any previous content

        # Display recipe details and ingredients directly in the Text widget
        recipe_details_text.insert("end", f"\n🍽️ Servings: {recipe['servings']}\n")
        recipe_details_text.insert("end", f"\n⏲️ Prep time: {recipe['readyInMinutes']} minutes\n")
        recipe_details_text.insert("end", f"\n🍳 Cook time: {recipe['cookingMinutes']} minutes\n")

        if 'extendedIngredients' in recipe:
            recipe_details_text.insert("end", "\n Ingredients: \n")
            for ingredient in recipe['extendedIngredients']:
                recipe_details_text.insert("end", f"\n {ingredient['original']}\n")

         # Create a separate Text widget for instructions
            instructions_text = Text(frame, height=15, width=50, bg="#FDFAF5", wrap="word")
            instructions_text.place(x=800, y=12)  # Position below recipe details
            instructions_text.delete("1.0", "end")  # Clear any previous content

        # Display instructions if available
        if 'instructions' in recipe:
            instructions_text.insert("end", "\n Instructions: \n")
            instructions_text.insert("end", f"\n {recipe['instructions']} minutes \n")
        else: 
            instructions_text.insert("end", "\n No instructions available.\n")
                
    #shows image
    
    def __show_image(self, frame, image_url):
        # Fetch the image from the URL
        response = requests.get(image_url)
        
        # Open and resize the image
        img = Image.open(BytesIO(response.content))
        img = img.resize((RECIPE_IMAGE_HEIGHT, RECIPE_IMAGE_WIDTH))  # Resize image (adjust the size as needed)
        
        # Convert the image to a format Tkinter can use
        image = ImageTk.PhotoImage(img)

        # Create a label to hold the image
        holder = Label(frame, image=image)
        holder.photo = image  # Keep a reference to the image to avoid garbage collection
        
        # Position the image above the text (row=0)
        holder.grid(row=0, column=0, pady=20, padx=20)  # Adjust positioning as needed
        #shows recipe thumbnail

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
    def __search_and_display_results(self, query):
        # Retrieve simplified recipe info (id, title, and image)
        recipes = self.__search_recipes(query)

        # Open results in a new window
        if recipes:
            self.__open_results_window(recipes)
        else:
            self.__open_results_window(None, message="No recipes found for your search.")    

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

