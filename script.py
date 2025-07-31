import os
import shutil
import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox
from pathlib import Path
import webbrowser
from PIL import Image, ImageTk
import sys
import psutil  # NEW: for process checking

# --- Helper to find resource path (supports .exe bundles) ---
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Paths
APPDATA = Path(os.getenv("LOCALAPPDATA"))
SETTINGS_DIR = APPDATA / "SWTOR" / "swtor" / "settings"
PROFILES_DIR = SETTINGS_DIR / "Profiles"
BASE_FILE = SETTINGS_DIR / "client_settings.ini"
QR_CODE_PATH = resource_path("qrcode.png")  # Bundled path

# Ensure Profiles directory exists
PROFILES_DIR.mkdir(parents=True, exist_ok=True)

# URLs
DONATION_URL = "https://www.paypal.com/ncp/payment/YKTMT6CB4JJMJ"
YOUTUBE_URL = "https://youtube.com/@CashMfinMoney"
TWITCH_URL = "https://twitch.tv/CashMfinMoney"
TIKTOK_URL = "https://www.tiktok.com/@CashMfinMoney"

# --- Process helper to detect SWTOR ---
def get_swtor_process():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() == "swtor.exe":
            return proc
    return None

# --- Profile functions ---
def get_profiles():
    return [f.name for f in PROFILES_DIR.glob("*.ini")]

def save_profile():
    profile_name = simpledialog.askstring("Save Profile", "Enter profile name:")
    if not profile_name:
        return
    dest = PROFILES_DIR / f"{profile_name}.ini"
    try:
        shutil.copyfile(BASE_FILE, dest)
        refresh_list()
    except FileNotFoundError:
        messagebox.showerror("Error", f"{BASE_FILE.name} not found.")

def load_profile():
    proc = get_swtor_process()
    if proc:
        answer = messagebox.askyesno(
            "SWTOR Running",
            "SWTOR must be closed before loading a profile.\n"
            "Do you want to close SWTOR now?"
        )
        if answer:
            try:
                proc.terminate()
                proc.wait(timeout=5)
                messagebox.showinfo("Closed", "SWTOR was closed successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Could not close SWTOR: {e}")
                return
        else:
            return  # User chose not to close SWTOR, cancel loading

    selection = listbox.get(tk.ACTIVE)
    if not selection:
        return
    src = PROFILES_DIR / selection
    try:
        shutil.copyfile(src, BASE_FILE)
        messagebox.showinfo("Loaded", f"{selection} loaded as current settings.")
    except FileNotFoundError:
        messagebox.showerror("Error", f"Profile {selection} not found.")

def delete_profile():
    selection = listbox.get(tk.ACTIVE)
    if not selection:
        return
    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete the profile:\n\n{selection}?"
    )
    if confirm:
        try:
            os.remove(PROFILES_DIR / selection)
            refresh_list()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete profile: {e}")

def refresh_list():
    listbox.delete(0, tk.END)
    for profile in get_profiles():
        listbox.insert(tk.END, profile)

def open_url(url):
    webbrowser.open(url)

# --- Splash screen ---
def show_splash():
    splash = tk.Tk()
    splash.iconbitmap(resource_path("icon.ico"))
    splash.title("CashMfinMoney's SWTOR Profile Manager")
    splash.geometry("500x650")
    splash.configure(padx=20, pady=20)

    msg = (
        "👋 Hey there! Thanks for using this tool.\n\n"
        "• I've JUST STARTED my content creation journey, and I'm pursuing it FULL TIME whilst being a full time student.\n"
        "• I've created this software as a means for self-promotion and as a useful tool for my fellow SWTOR players.\n"
        "• If you'd like to support me, I've included my donation QR code. ANYTHING HELPS. \n"
        "• HOWEVER, If you're unable to donate, you can help me IMMENSELY by FOLLOWING my channels.\n"
        "• *OR* - If you'd like to send me a thanks, or some in-game credits - I am on Star Forge and Satele Shan.\n"
        "• Imperial Side Character Name: Kash Monhee\n"
        "• Republic Side Character Name: Dekarris Vaan\n"
    )
    tk.Label(splash, text=msg, wraplength=460, justify="left").pack(pady=(0, 15))

    if os.path.exists(QR_CODE_PATH):
        img = Image.open(QR_CODE_PATH)
        img = img.resize((180, 180))
        qr_img = ImageTk.PhotoImage(img)
        qr_label = tk.Label(splash, image=qr_img)
        qr_label.image = qr_img
        qr_label.pack(pady=10)
    else:
        tk.Label(splash, text="QR code image not found.").pack(pady=10)

    links_frame = tk.Frame(splash)
    links_frame.pack(pady=10)

    def make_link(parent, text, url):
        link = tk.Label(parent, text=text, fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
        link.pack(pady=3)
        link.bind("<Button-1>", lambda e: open_url(url))

    make_link(links_frame, "💸 Donate via PayPal", DONATION_URL)
    make_link(links_frame, "📺 YouTube", YOUTUBE_URL)
    make_link(links_frame, "🎮 Twitch", TWITCH_URL)
    make_link(links_frame, "📱 TikTok", TIKTOK_URL)

    def on_continue():
        splash.destroy()
        show_main()

    tk.Button(splash, text="Maybe Later", command=on_continue).pack(pady=20)
    splash.mainloop()

# --- Main UI ---
def show_main():
    global listbox
    root = tk.Tk()
    root.geometry("400x400")
    root.title("CashMfinMoney's SWTOR Profile Manager")
    root.iconbitmap(resource_path("icon.ico"))
    tk.Button(root, text="Save Current as New Profile", command=save_profile).pack()
    tk.Button(root, text="Load Selected Profile", command=load_profile).pack()
    tk.Button(root, text="Delete Selected Profile", command=delete_profile).pack()

    listbox = Listbox(root, width=50)
    listbox.pack()
    refresh_list()

    root.mainloop()

# --- Start app ---
if __name__ == "__main__":
    show_splash()
