import socket
import threading
from queue import Queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog

# --- Configuration ---
DEFAULT_HOST = '127.0.0.1'
DEFAULT_START_PORT = 1
DEFAULT_END_PORT = 1024
DEFAULT_TIMEOUT = 1

# --- Globals ---
port_queue = Queue()
open_ports_tcp = []
open_ports_udp = []
print_lock = threading.Lock()

# --- Scanner logic ---
def scan_tcp(host, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((host, port))
        if result == 0:
            with print_lock:
                open_ports_tcp.append(port)
        s.close()
    except Exception as e:
        print(f"TCP error on port {port}: {e}")

def scan_udp(host, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(timeout)
        try:
            s.sendto(b"", (host, port))
            with print_lock:
                open_ports_udp.append(port)
        except Exception as e:
            print(f"UDP error on port {port}: {e}")
        s.close()
    except Exception as e:
        print(f"UDP socket error: {e}")

def worker(host, timeout, protocol):
    while True:
        port = port_queue.get()
        try:
            if protocol in ("TCP", "Both"):
                scan_tcp(host, port, timeout)
            if protocol in ("UDP", "Both"):
                scan_udp(host, port, timeout)
        except Exception as e:
            print(f"Worker error: {e}")
        finally:
            port_queue.task_done()

def run_scan(host, start_port, end_port, timeout, num_threads, protocol, output_widget):
    open_ports_tcp.clear()
    open_ports_udp.clear()
    for port in range(start_port, end_port + 1):
        port_queue.put(port)
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(host, timeout, protocol), daemon=True)
        thread.start()
    port_queue.join()

    results = []
    if open_ports_tcp:
        results.append("TCP Open Ports:\n" + "\n".join(str(p) for p in sorted(open_ports_tcp)))
    if open_ports_udp:
        results.append("UDP Open Ports:\n" + "\n".join(str(p) for p in sorted(open_ports_udp)))
    if not results:
        results = ["No open ports found."]
    final_text = "\n\n".join(results)

    output_widget.config(state="normal")
    output_widget.delete(1.0, tk.END)
    output_widget.insert(tk.END, final_text)
    output_widget.config(state="disabled")

# --- Save Results ---
def save_results():
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if not file_path:
            return
        content = output_box.get(1.0, tk.END).strip()
        if not content:
            messagebox.showwarning("Save Results", "No results to save.")
            return
        with open(file_path, "w") as f:
            f.write(content)
        messagebox.showinfo("Save Results", f"Results saved to {file_path}")
    except Exception as e:
        messagebox.showerror("Save Error", f"Could not save results:\n{e}")

# --- Tkinter UI ---
def start_scan():
    try:
        host = host_entry.get() or DEFAULT_HOST
        start_port = int(start_port_entry.get() or DEFAULT_START_PORT)
        end_port = int(end_port_entry.get() or DEFAULT_END_PORT)
        timeout = float(timeout_entry.get() or DEFAULT_TIMEOUT)
        num_threads = int(threads_entry.get() or 10)
        protocol = protocol_var.get()
        run_scan(host, start_port, end_port, timeout, num_threads, protocol, output_box)
        notebook.select(results_frame)  # switch to Results tab automatically
    except ValueError:
        messagebox.showerror("Error", "Invalid input values.")

# --- Dark Theme Setup ---
BG_COLOR = "#1e1e1e"
FG_COLOR = "#e0e0e0"
ACCENT_COLOR = "#00ffff"
BTN_BG = "#2d2d2d"
ENTRY_BG = "#2a2a2a"
RESULT_BG = "#000000"
RESULT_FG = "#00ff00"

root = tk.Tk()
root.title("Noble Crow Port Scanner")
root.configure(bg=BG_COLOR)

style = ttk.Style()
style.theme_use("default")
style.configure("TNotebook", background=BG_COLOR, borderwidth=0)
style.configure("TNotebook.Tab", background=BTN_BG, foreground=ACCENT_COLOR, font=("Consolas", 11))
style.map("TNotebook.Tab", background=[("selected", RESULT_BG)], foreground=[("selected", RESULT_FG)])

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# --- Tab 1: Scan Settings ---
settings_frame = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(settings_frame, text="Scan Settings")

def styled_label(master, text, row, col):
    lbl = tk.Label(master, text=text, bg=BG_COLOR, fg=FG_COLOR, font=("Consolas", 11))
    lbl.grid(row=row, column=col, sticky="e", pady=3)

def styled_entry(master, default, row, col):
    ent = tk.Entry(master,
                   bg=ENTRY_BG,
                   fg="red",              # input text is red
                   insertbackground="red", # caret is red
                   relief="flat",
                   font=("Consolas", 11))
    ent.insert(0, default)
    ent.grid(row=row, column=col, pady=3)
    return ent

styled_label(settings_frame, "Host:", 0, 0)
host_entry = styled_entry(settings_frame, DEFAULT_HOST, 0, 1)

styled_label(settings_frame, "Start Port:", 1, 0)
start_port_entry = styled_entry(settings_frame, DEFAULT_START_PORT, 1, 1)

styled_label(settings_frame, "End Port:", 2, 0)
end_port_entry = styled_entry(settings_frame, DEFAULT_END_PORT, 2, 1)

styled_label(settings_frame, "Timeout (s):", 3, 0)
timeout_entry = styled_entry(settings_frame, DEFAULT_TIMEOUT, 3, 1)

styled_label(settings_frame, "Threads:", 4, 0)
threads_entry = styled_entry(settings_frame, 10, 4, 1)

styled_label(settings_frame, "Protocol:", 5, 0)
protocol_var = tk.StringVar(value="TCP")
protocol_menu = tk.OptionMenu(settings_frame, protocol_var, "TCP", "UDP", "Both")
protocol_menu.config(bg=BTN_BG, fg=ACCENT_COLOR, relief="flat", font=("Consolas", 11))
protocol_menu.grid(row=5, column=1, pady=3)

scan_btn = tk.Button(settings_frame, text="Start Scan", command=start_scan,
                     bg=BTN_BG, fg=ACCENT_COLOR, activebackground=ACCENT_COLOR,
                     activeforeground=BG_COLOR, relief="flat", font=("Consolas", 12, "bold"))
scan_btn.grid(row=6, column=0, columnspan=2, pady=10)

# --- Tab 2: Results ---
results_frame = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(results_frame, text="Results")

output_box = scrolledtext.ScrolledText(results_frame, width=70, height=20,
                                       bg=RESULT_BG, fg=RESULT_FG,
                                       font=("Consolas", 11), relief="flat")
output_box.pack(padx=10, pady=10)
output_box.config(state="disabled")

save_btn = tk.Button(results_frame, text="Save Results", command=save_results,
                     bg=BTN_BG, fg=ACCENT_COLOR, relief="flat", font=("Consolas", 12, "bold"))
save_btn.pack(pady=10)

# --- Tab 3: About ---
about_frame = tk.Frame(notebook, bg=BG_COLOR)
notebook.add(about_frame, text="About")

tk.Label(about_frame, text="Noble Crow Port Scanner\nDark Mode Edition",
         bg=BG_COLOR, fg=ACCENT_COLOR, font=("Consolas", 14, "bold")).pack(pady=20)
tk.Label(about_frame, text="Use responsibly on authorized networks only.",
         bg=BG_COLOR, fg=FG_COLOR, font=("Consolas", 11)).pack(pady=10)

root.mainloop()
