import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from image_processor import ImageProcessor
from game_logic import GameLogic

# Main game window class
class GameUI(tk.Tk):
    # BG color and bullet points to be used later
    BG = "#f6f6f6"
    bullet = "\u2022"
    def __init__(self):
        super().__init__()
        # Setting up the window
        self.title("Spot the Differences!")
        self.configure(bg=self.BG)
        self.geometry("1200x800")

        # Widget variables
        self.headerframe = None
        self.load_btn = None
        self.reveal_btn = None
        self.new_btn = None
        self.title_label = None

        # Separating different sections
        self.setup_root_grid()
        self.setup_header()
        self.setup_image_space()
        self.setup_footer()

        # Objects from classes
        self.ip = ImageProcessor(self.copy_img_label, self.ori_img_label)
        self.logic = GameLogic()


        self.set_reveal_btn(False)
        self.load_default_image()

    # Row and column configuration
    def setup_root_grid(self):
        self.columnconfigure(0, weight=1)
        # Header
        self.rowconfigure(0, weight=0)
        # Images
        self.rowconfigure(1, weight=1)
        # Footer
        self.rowconfigure(2, weight=0)

    # Creating the top header section
    def setup_header(self):
        self.headerframe = tk.Frame(self, bg=self.BG, pady=10)

        self.headerframe.columnconfigure(0, weight=1)
        self.headerframe.columnconfigure(1, weight=8)
        self.headerframe.columnconfigure(2, weight=1)

        self.headerframe.grid(row=0, column=0, sticky="ew")

        # Header Buttons
        self.load_btn = tk.Button(
            self.headerframe,
            text="Load Image",
            font=("Open Sans", 16),
            borderwidth=0,
            highlightthickness=0,
            command=self.load_image
        )
        self.load_btn.grid(row=0, column=0)

        self.reveal_btn = tk.Button(
            self.headerframe,
            text="Reveal Differences",
            font=("Open Sans", 16),
            borderwidth=0,
            highlightthickness=0, command=self.reveal_differences)
        self.reveal_btn.grid(row=0, column=2)

        # Title of the Game
        self.title_label = tk.Label(self.headerframe,
                               text="Spot the Difference!",
                               font=("Arial", 22, "bold",),
                               bg=self.BG, fg="black")
        self.title_label.grid(row=0, column=1)

    # The section for containing the images
    def setup_image_space(self):
        self.image_frame = tk.Frame(self, bg=self.BG, padx=10, pady=10)

        self.image_frame.columnconfigure(0, weight=1)
        self.image_frame.columnconfigure(1, weight=1)

        self.image_frame.grid(row=1, column=0, sticky="nsew")

        self.setup_original_image()
        self.setup_duplicate_image()

    def setup_original_image(self):
        self.ori_frame = tk.Frame(self.image_frame, bg=self.BG, padx=20, pady=10, bd=1, relief="solid")
        self.ori_frame.grid(row=0, column=0, sticky="n")

        self.ori_img_text = tk.Label(self.ori_frame,
                                text="Original Image",
                                font=("Arial", 14),
                                bg=self.BG,
                                fg="#656364",
                                pady=10)
        self.ori_img_text.grid(row=0, column=0)

        self.ori_img = Image.open("Images/placeholder_image.png").resize((500, 500))
        self.ori_img = ImageTk.PhotoImage(self.ori_img)

        self.ori_img_label = tk.Label(self.ori_frame, image=self.ori_img)
        self.ori_img_label.grid(row=1, column=0)


    def setup_duplicate_image(self):
        self.copy_frame = tk.Frame(self.image_frame, bg=self.BG, padx=15, pady=10, bd=1, relief="solid")
        self.copy_frame.grid(row=0, column=1, padx=10, sticky="n")

        self.copy_img_text = tk.Label(self.copy_frame,
                                 text="Altered Image (Click on the Differences!)",
                                 font=("Arial", 14),
                                 bg=self.BG,
                                 fg="#656364",
                                 pady=10)
        self.copy_img_text.grid(row=0, column=0)

        self.copy_img = Image.open("Images/placeholder_image.png").resize((500, 500))
        self.copy_img = ImageTk.PhotoImage(self.copy_img)

        self.copy_img_label = tk.Label(self.copy_frame, image=self.copy_img)
        self.copy_img_label.grid(row=1, column=0)
        self.copy_img_label.bind("<Button-1>", self.on_click)

    # Setting up the footer section
    def setup_footer(self):
        self.footer_frame = tk.Frame(self, bg=self.BG, padx=10, pady=10)

        self.footer_frame.columnconfigure(0, weight=1)
        self.footer_frame.columnconfigure(1, weight=1)
        self.footer_frame.columnconfigure(2, weight=1)

        self.footer_frame.grid(row=2, column=0, sticky="ew")

        self.counts()
        self.setup_instructions()
        self.setup_status()

