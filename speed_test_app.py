import speedtest
import tkinter as tk
from tkinter import ttk  
from PIL import Image, ImageTk
import threading

class InternetSpeedTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Internet Speed Test")

        
        icon_image = tk.PhotoImage(file="your_icon.png")  
        self.root.iconphoto(True, icon_image)

        
        self.root.geometry("500x500")  
        self.root.resizable(False, False)  

        
        self.font_large = ("Helvetica", 16)  
        self.font_medium = ("Helvetica", 14, "bold")  
        self.font_title = ("Helvetica", 20, "bold")  

        
        self.root.tk_setPalette(background='#001632', foreground='#34ffea')  

        
        self.setup_icons()

        
        self.title_label = tk.Label(root, text="Internet Speed Test", font=self.font_title, bg='#001632', fg='#34ffea')  
        self.title_label.pack(pady=(10, 20)) 

        self.logo_image = Image.open("logo.png").resize((100, 100))  
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        self.logo_label = tk.Label(root, image=self.logo_image, bg='#001632')
        self.logo_label.pack()

       
        self.download_frame = tk.Frame(root, bg='#001632')
        self.download_frame.pack(pady=10)

        self.download_icon = tk.Label(self.download_frame, image=self.download_icon_image, bg='#001632', fg='#34ffea')
        self.download_icon.grid(row=0, column=0, padx=10)

        self.download_title = tk.Label(self.download_frame, text="Download Speed:", font=self.font_medium, bg='#001632', fg='#34ffea')
        self.download_title.grid(row=0, column=1)

        self.download_speed = tk.Label(self.download_frame, text="", font=self.font_large, bg='#001632', fg='green')
        self.download_speed.grid(row=0, column=2)

        self.download_result = tk.Label(self.download_frame, text="", font=self.font_medium, bg='#001632', fg='green')
        self.download_result.grid(row=1, column=0, columnspan=3, pady=5)

        
        self.upload_frame = tk.Frame(root, bg='#001632')
        self.upload_frame.pack(pady=10)

        self.upload_icon = tk.Label(self.upload_frame, image=self.upload_icon_image, bg='#001632', fg='#34ffea')
        self.upload_icon.grid(row=0, column=0, padx=10)

        self.upload_title = tk.Label(self.upload_frame, text="Upload Speed:", font=self.font_medium, bg='#001632', fg='#34ffea')
        self.upload_title.grid(row=0, column=1)

        self.upload_speed = tk.Label(self.upload_frame, text="", font=self.font_large, bg='#001632', fg='orange')
        self.upload_speed.grid(row=0, column=2)

        self.upload_result = tk.Label(self.upload_frame, text="", font=self.font_medium, bg='#001632', fg='orange')
        self.upload_result.grid(row=1, column=0, columnspan=3, pady=5)

        
        self.test_button = tk.Button(
            root,
            text="Run Speed Test",
            command=self.run_speed_test,
            image=self.test_button_image,
            compound=tk.LEFT,
            font=self.font_medium,
            bg='#0066cc',  
            fg='white',  
            relief=tk.FLAT,  
            padx=10,  
            pady=5,  
            borderwidth=0, 
        )
        self.test_button.pack(pady=20)

        self.test_button.bind("<Enter>", self.on_enter)
        self.test_button.bind("<Leave>", self.on_leave)

        
        self.progress_bar = ttk.Progressbar(root, mode="indeterminate", length=200)

    def setup_icons(self):
        
        download_icon_filename = "download_icon.png"
        upload_icon_filename = "upload_icon.png"
        test_button_icon_filename = "test_button_icon.png"

        
        self.download_icon_image = Image.open(download_icon_filename).resize((32, 32))
        self.download_icon_image = ImageTk.PhotoImage(self.download_icon_image)

        self.upload_icon_image = Image.open(upload_icon_filename).resize((32, 32))
        self.upload_icon_image = ImageTk.PhotoImage(self.upload_icon_image)

        self.test_button_image = Image.open(test_button_icon_filename).resize((32, 32))
        self.test_button_image = ImageTk.PhotoImage(self.test_button_image)

    def on_enter(self, event):
        
        self.test_button.config(bg="#0052cc")  

    def on_leave(self, event):
        
        self.test_button.config(bg='#0066cc')  

    def run_speed_test(self):
       
        self.test_button.config(state=tk.DISABLED)

       
        self.progress_bar.pack(pady=10)
        self.progress_bar.start()

        
        threading.Thread(target=self.run_speed_test_thread).start()

    def run_speed_test_thread(self):
       
        download_speed = 0.0
        upload_speed = 0.0

        try:
            st = speedtest.Speedtest()
           
            download_speed = st.download() / 1_000_000  
            upload_speed = st.upload() / 1_000_000 
        except speedtest.SpeedtestCLIError as e:
            print(f"Speed test error: {e}")
            
            self.show_error_message("Speed Test Error", f"An error occurred during the speed test:\n{e}")
        except speedtest.SpeedtestBestServerFailure as e:
            print(f"Best server error: {e}")
            
            self.show_error_message("Best Server Error", f"Unable to connect to servers to test latency.")
        except Exception as e:
            print(f"Error: {e}")
           
            self.show_error_message("Error", f"An unexpected error occurred:\n{e}")
        finally:
           
            self.update_results(download_speed, upload_speed)

    def update_results(self, download_speed, upload_speed):
        
        self.download_speed.config(text=f"{download_speed:.2f} Mbps")
        self.upload_speed.config(text=f"{upload_speed:.2f} Mbps")

       
        self.download_result.config(text="Result: Download complete!", fg='white')
        self.upload_result.config(text="Result: Upload complete!", fg='white')

        
        self.progress_bar.stop()
        self.progress_bar.pack_forget()

       
        self.test_button.config(state=tk.NORMAL)

    def show_error_message(self, title, message):
        
        tk.messagebox.showerror(title, message)

if __name__ == "__main__":
    root = tk.Tk()
    app = InternetSpeedTestApp(root)
    root.mainloop()
