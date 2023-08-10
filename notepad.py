# Import necessary libraries
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font
from tkinter import font as tkFont
from PIL import Image, ImageTk

# Define the Notepad class
class Notepad:
    # Initialize GUI components
    def __init__(self, root):
        # Main window
        self.root = root
        # Text area in the window where users will type
        self.text_area = tk.Text(self.root)
        self.text_area.pack(expand=True, fill='both')
        self.text_area.tag_config("bold", font=(None, 12, "bold"))

        # Font for text area with initial size
        self.text_font = font.Font(size=12)
        self.text_area.configure(font=self.text_font)

        self.saved = True
        self.text_area.bind("<<Modified>>", self.set_modified)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Bind mousewheel event to zoom function
        # self.text_area.bind("<MouseWheel>", self.zoom)

        # Key binding for bullet point
        self.root.bind('<Control-l>', self.insert_bullet)

        # Font for bold text
        self.bold_font = font.Font(self.text_area, self.text_area.cget("font"))
        self.bold_font.configure(weight="bold")

        # Key binding for bold
        self.root.bind('<Control-b>', self.toggle_bold)

        # Key binding for checkbox
        self.root.bind('<Control-s>', self.toggle_checkbox)

        # Key binding for new page
        self.root.bind('<Control-n>', self.new_file)

        # Canvas overlay for image
        # self.canvas = tk.Canvas(self.text_area, bd=0, highlightthickness=0)
        # self.canvas.pack(fill='both', expand=True)
        # self.canvas.place(relheight=1, relwidth=1)

        # Main menu bar
        self.menu = tk.Menu(self.root)
        # File submenu in the main menu bar
        self.file_menu = tk.Menu(self.menu, tearoff=0)

        # Edit submenu in the main menu bar
        self.edit_menu = tk.Menu(self.menu, tearoff=0)

        #Store images in a list to prevent garbage collection
        self.images = []

        # Store canvas images in a list for resizing
        # self.canvas_images = []

        # Add new submenu
        # self.xxxxx_menu = tk.Menu(self.menu, tearoff=0)

        # Call method to create widgets
        self.create_widgets()


    # Create and configure widgets
    def create_widgets(self):
        # Add the main menu to the root window
        self.root.config(menu=self.menu)

        # Add the 'File' submenu to the main menu
        self.menu.add_cascade(label="File", menu=self.file_menu)
        # Add the 'Edit' command to the main menu
        self.menu.add_cascade(label="Edit", menu=self.edit_menu)

        # Add commands to the 'File' menu
        self.file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        
        ## Add commands to the 'Edit' menu
        # Add images feature
        self.edit_menu.add_command(label="Insert Image", command=self.insert_image)
        # Edit font size
        self.edit_menu.add_command(label="Font Size", command=self.set_font_size)
        # Add a separator in the menu
        self.edit_menu.add_separator()
        # Add bullet list option
        self.edit_menu.add_command(label="Bullet", command=self.insert_bullet, accelerator="Ctrl+L")
        # Add bold feature
        self.edit_menu.add_command(label="Toggle Bold", command=self.toggle_bold, accelerator="Ctrl+B")
        # Add toggle checkbox feature
        self.edit_menu.add_command(label="Toggle Checkbox", command=self.toggle_checkbox, accelerator="Ctrl+S")


        # Allow the text area to fill the window
        self.text_area.pack(expand=True, fill='both')

#--------------------------------------------------------------------------------------------------------------------------------

    # Insert image in the notepad
    def insert_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])
        if file_path:
            image = Image.open(file_path)
            # Ask for the desired image size
            width = simpledialog.askinteger("Width", "Enter image width")
            height = simpledialog.askinteger("Height", "Enter image height")
            # Resize the image
            image = image.resize((width, height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            # Append the image object to the images list
            self.images.append(photo)
            self.text_area.image_create('insert', image=photo)

    # Set the modified flag when the text is changed
    def set_modified(self, event=None):
        self.saved = False
        self.text_area.edit_modified(False)  # Reset the modified flag in the Text widget

    def on_closing(self):
        if not self.saved:
            if messagebox.askyesno("Save changes?", "You have unsaved changes. Do you want to save before exiting?"):
                self.save_file()
        self.root.destroy()

    def new_file(self, event=None):
        if not self.saved:
            if messagebox.askyesno("Save changes?", "Would you like to save your changes?"):
                self.save_file()

        self.text_area.delete(1.0, 'end')
        self.saved = True
        
    # # Mouse drag event
    # def on_drag(self, event):
    #     # Get the image ID and image object from the last inserted image
    #     image_id, photo, image = self.canvas_images[-1]
    # 
    #     dx = event.x - self.last_x
    #     dy = event.y - self.last_y
    # 
    #     new_width = image.width + dx
    #     new_height = image.height + dy
    # 
    #     if new_width > 0 and new_height > 0:
    #         image = image.resize((new_width, new_height))
    #         photo = ImageTk.PhotoImage(image)
    # 
    #         self.images.append(photo)
    #         self.canvas_images[-1] = (image_id, photo, image)
    # 
    #         self.canvas.itemconfig(image_id, image=photo)
    # 
    #     self.last_x = event.x
    #     self.last_y = event.y

    # Insert Bullet points
    def insert_bullet(self, event=None):
        # Get the current line
        current_line = self.text_area.index('insert').split('.')[0]
        # Insert the bullet at the start of the current line
        self.text_area.insert(f'{current_line}.0', '\u2022 ')
    
    # Checkbox
    def toggle_checkbox(self, event=None):
        '''Function to toggle a checkbox at the current cursor position'''
        # Get the current line
        line = self.text_area.get("insert linestart", "insert lineend").strip()

        # Check if the current line already has a checkbox
        if line.startswith("✔") or line.startswith("❏"):
            # If the line already has a checkbox, toggle it
            if line.startswith("✔"):
                self.text_area.delete("insert linestart", "insert linestart + 2c")
                self.text_area.insert("insert linestart", "❏ ")
            else:
                self.text_area.delete("insert linestart", "insert linestart + 2c")
                self.text_area.insert("insert linestart", "✔ ")
        else:
            # If the line doesn't have a checkbox, add one
            self.text_area.insert("insert linestart", "❏ ")


       


    # Method to open a file and load its content to the text area
    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
        if file_path:
            self.root.title(f'Notepad - {file_path}')
            self.text_area.delete(1.0, 'end')
            with open(file_path, 'r') as file:
                self.text_area.insert('insert', file.read())

    # Method to save the current content of the text area to a file
    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, 'end'))
                self.root.title(f'Notepad - {file_path}')
            except Exception as e:
                messagebox.showerror("Save error", str(e))

    # Method to save the current content of the text area to a new file
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("All Files", "*.*"), ("Text Files", "*.txt"), ("HTML Files", "*.html")])
        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(self.text_area.get(1.0, 'end'))
                self.root.title(f'Notepad - {file_path}')
            except Exception as e:
                messagebox.showerror("Save error", str(e))
    
    def set_font_size(self):
        size = simpledialog.askinteger("Set Font Size", "Enter font size", initialvalue=self.text_font.cget("size"))
        if size is not None:  # If the user didn't cancel the dialog
            self.text_font.configure(size=size)
            # Update the bold font to match the new size
            self.text_area.tag_config("bold", font=(None, size, "bold"))

    # Bold the letters
    def toggle_bold(self, event=None):
     selected_text = self.text_area.tag_ranges("sel")
     if selected_text:
         # Check if the selected text is already bold
         if "bold" in self.text_area.tag_names(selected_text[0]):
             self.text_area.tag_remove("bold", "sel.first", "sel.last")
         else:
             self.text_area.tag_add("bold", "sel.first", "sel.last")
         return "break"

# Create an instance of the Notepad class and start the application
if __name__ == "__main__":
    root = tk.Tk()
    root.title('Notepad')
    root.geometry('600x400')
    Notepad(root)
    root.mainloop()
