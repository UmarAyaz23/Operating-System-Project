import os
import threading
import subprocess
import shutil
import numpy as np
from tkinter import Tk, Menu, filedialog, messagebox, Frame, Label, Button, simpledialog, Entry, Listbox
import multiprocessing

class YBOS:
    def __init__(self):
        self.root = Tk()
        self.root.title("THE Y-BAND OS")
        self.users = {"Umar": "008", "Saaniya": "018", "Anuf": "019", "Zeeshan": "026"}
        self.current_directory = os.getcwd()
        self.shared_data = SharedData()
        self.user_listbox = None
        self.create_login_frame()
        self.root.mainloop()


    def create_login_frame(self):
        self.login_frame = Frame(self.root, bg="#333333")
        self.login_frame.pack(padx=0, pady=0)
        
        Label(self.login_frame, text="AVAILABLE USERS", font=("Century Gothic", 12, "bold"), bg="#333333", fg = "white").pack(pady=5)
        self.user_listbox = Listbox(self.login_frame, selectmode="single", font=("Century Gothic", 12), bg="#DCDCDC")
        
        for user in self.users:
            self.user_listbox.insert("end", user)
        self.user_listbox.pack(pady = 5, padx = 5)
        self.user_listbox.bind("<Double-Button-1>", lambda event: self.prompt_password())
        Button(self.login_frame, text="LOGIN", font = ("Century Gothic", 12, "bold"), command=self.prompt_password, bg="#DCDCDC", fg="black").pack(pady=5)


    def prompt_password(self):
        self.username = self.user_listbox.get(self.user_listbox.curselection())
        
        if self.username in self.users:
            self.login_frame.pack_forget()
            self.password_frame = Frame(self.root, bg="#333333")
            self.password_frame.pack(padx=0, pady=0)
            
            Label(self.password_frame, text=f"Hello {self.username}! \nEnter Password:", font=("Century Gothic", 12), bg="#333333", fg = "white").pack(pady=5)
            self.password_entry = Entry(self.password_frame, show='*')
            self.password_entry.pack(padx = 10, pady=5)
            self.password_entry.bind("<Return>", lambda event: self.validate_login())
            
            Button(self.password_frame, text="LOGIN", font = ("Century Gothic", 10, "bold"),command=self.validate_login, bg="#DCDCDC", fg="black").pack(pady=5)
            self.password_entry.focus_set()
        else:
            messagebox.showerror("Error", "Invalid username.")
            

    def validate_login(self):
        password = self.password_entry.get()
        if self.users[self.username] == password:
            self.password_frame.pack_forget()
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Invalid password.")
            

    def create_main_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        main_menu = Menu(menubar, tearoff=0)
        
        menubar.add_cascade(label="File", menu=main_menu)
        user_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="User Management", menu=user_menu)
        user_menu.add_command(label="Create User", command=self.create_user)
        user_menu.add_command(label="Delete User", command=self.delete_user)
        user_menu.add_command(label="Edit User", command=self.edit_user)
        user_menu.add_command(label="List Users", command=self.list_users)
        
        process_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Process Management", menu=process_menu)
        process_menu.add_command(label="Sort Array Process", command=self.create_sorting_process)
        #process_menu.add_command(label="IPC", command=self.ipc_process_communication)  # New Menu Item for IPC
        
        app_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Applications", menu=app_menu)
        app_menu.add_command(label="Open Firefox", command=self.open_firefox)
        app_menu.add_command(label="Open Image Viewer", command=self.open_image_viewer)
        app_menu.add_command(label="Open Calculator", command=self.open_calculator)  # New Menu Item for Calculator
        app_menu.add_command(label="Open Recycle Bin", command=self.open_recycle_bin)  # New Menu Item for Recycle Bin
        
        program_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Custom Programs", menu=program_menu)
        program_menu.add_command(label="Execute Program", command=self.execute_program)
        program_menu.add_command(label="Delete Program", command=self.delete_program)
        
        matrix_menu = Menu(main_menu, tearoff=0)
        main_menu.add_cascade(label="Matrix Operations", menu=matrix_menu)
        matrix_menu.add_command(label="Add Matrices", command=self.add_matrices)
        matrix_menu.add_command(label="Subtract Matrices", command=self.subtract_matrices)
        matrix_menu.add_command(label="Multiply Matrices", command=self.multiply_matrices)
        
        self.create_gui()

    def create_gui(self):
        frame = Frame(self.root, bg="#DCDCDC")
        frame.pack(padx=0, pady=0)
        
        Label(frame, text="THE Y-BAND OS", font=("Century Gothic", 16, "bold", "italic"), bg="#DCDCDC", fg="black", width=15).grid(row=0, column=0, columnspan=4, pady=5)
        
        button_config = {
            "font": ("candara", 12),
            "bg": "#333333",
            "fg": "white",
            "width": 20  # Adjust the width to make them equal
        }

        Button(frame, text="Create Folder", command=self.create_folder, **button_config).grid(row=1, column=0, padx=5, pady=5)
        Button(frame, text="Create File", command=self.create_file, **button_config).grid(row=1, column=1, padx=5, pady=5)
        Button(frame, text="Change File Rights", command=self.change_rights, **button_config).grid(row=1, column=2, padx=5, pady=5)
        Button(frame, text="Sort Array Process", command=self.create_sorting_process, **button_config).grid(row=1, column=3, padx=5, pady=5)
        
        Button(frame, text="View Task Manager", command=self.view_task_manager, **button_config).grid(row=2, column=0, padx=5, pady=5)
        Button(frame, text="Open Firefox", command=self.open_firefox, **button_config).grid(row=2, column=1, padx=5, pady=5)
        Button(frame, text="Open Image Viewer", command=self.open_image_viewer, **button_config).grid(row=2, column=2, padx=5, pady=5)
        Button(frame, text="Execute Program", command=self.execute_program, **button_config).grid(row=2, column=3, padx=5, pady=5)

        Button(frame, text="Delete Program", command=self.delete_program, **button_config).grid(row=3, column=0, padx=5, pady=5)
        Button(frame, text="Backup System", command=self.backup_system, **button_config).grid(row=3, column=1, padx=5, pady=5)
        Button(frame, text="Search File", command=self.search_file, **button_config).grid(row=3, column=2, pady=5)
        Button(frame, text="Quit", command=self.root.destroy, font = ("candara", 12), bg = "maroon", fg = "white", width = 20).grid(row=3, column=3, pady=5)


    def create_folder(self):
        folder_name = simpledialog.askstring("Create Folder", "Enter folder name:")
        if folder_name:
            folder_path = os.path.join(self.current_directory, folder_name)
            os.makedirs(folder_path, exist_ok=True)
            messagebox.showinfo("Success", f"Folder '{folder_name}' created successfully.")

    def create_file(self):
        file_name = simpledialog.askstring("Create File", "Enter file name:")
        if file_name:
            file_path = os.path.join(self.current_directory, file_name)
            with open(file_path, 'w') as file:
                pass
            messagebox.showinfo("Success", f"File '{file_name}' created successfully.")

    def change_rights(self):
        file_path = filedialog.askopenfilename(title="Select File to Change Rights")
        if file_path:
            permission_str = simpledialog.askstring("Change Rights", "Enter permissions (e.g., 777, 752, etc.):")
            if permission_str.isdigit() and len(permission_str) == 3:
                os.chmod(file_path, int(permission_str, 8))
                messagebox.showinfo("Success", f"Permissions of file '{file_path}' changed successfully.")
            else:
                messagebox.showerror("Error", "Invalid permissions format.")

    def open_firefox(self):
        try:
            subprocess.Popen(['firefox'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Firefox. Error: {e}")

    def open_image_viewer(self):
        file_path = filedialog.askopenfilename(title="Select Image File")
        if file_path:
            try:
                subprocess.Popen(['xdg-open', file_path])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open Image Viewer. Error: {e}")

    def open_calculator(self):
        try:
            subprocess.Popen(['gnome-calculator'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Calculator. Error: {e}")

    def open_recycle_bin(self):
        try:
            subprocess.Popen(['nautilus', 'trash:///'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open Recycle Bin. Error: {e}")

    def execute_program(self):
        file_path = filedialog.askopenfilename(title="Select Program to Execute")
        if file_path:
            try:
                subprocess.Popen(['python', file_path])
            except Exception as e:
                messagebox.showerror("Error", f"Failed to execute program. Error: {e}")

    def delete_program(self):
        file_path = filedialog.askopenfilename(title="Select Program to Delete")
        if file_path:
            try:
                os.remove(file_path)
                messagebox.showinfo("Success", f"Program '{file_path}' deleted successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete program. Error: {e}")

    def backup_system(self):
        backup_dir = filedialog.askdirectory(title="Select Backup Directory")
        if backup_dir:
            backup_path = os.path.join(backup_dir, "system_backup")
            os.makedirs(backup_path, exist_ok=True)
            for root, dirs, files in os.walk(self.current_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    shutil.copy2(file_path, backup_path)
            messagebox.showinfo("Success", f"System backup created at '{backup_path}'.")

    def search_file(self):
        search_term = simpledialog.askstring("Search File", "Enter file name or pattern:")
        if search_term:
            result = []
            for root, dirs, files in os.walk(self.current_directory):
                for file in files:
                    if search_term in file:
                        result.append(os.path.join(root, file))
            if result:
                messagebox.showinfo("Search Results", "\n".join(result))
            else:
                messagebox.showinfo("Search Results", "No files found.")
                

    def list_users(self):
        users_list = "\n".join(self.users.keys())
        messagebox.showinfo("List of Users", users_list)

    def create_user(self):
        new_username = simpledialog.askstring("Create User", "Enter new username:")
        if new_username in self.users:
            messagebox.showerror("Error", "Username already exists.")
        else:
            new_password = simpledialog.askstring("Create User", "Enter new password:")
            self.users[new_username] = new_password
            messagebox.showinfo("Success", f"User '{new_username}' created successfully.")

    def delete_user(self):
        username = simpledialog.askstring("Delete User", "Enter username to delete:")
        if username in self.users:
            del self.users[username]
            messagebox.showinfo("Success", f"User '{username}' deleted successfully.")
        else:
            messagebox.showerror("Error", "Username not found.")

    def edit_user(self):
        username = simpledialog.askstring("Edit User", "Enter username to edit:")
        if username in self.users:
            new_password = simpledialog.askstring("Edit User", "Enter new password:")
            self.users[username] = new_password
            messagebox.showinfo("Success", f"Password for user '{username}' updated successfully.")
        else:
            messagebox.showerror("Error", "Username not found.")

    def view_task_manager(self):
        try:
            subprocess.Popen(['gnome-system-monitor'])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open task manager. Error: {e}")

    def create_sorting_process(self):
        array_str = simpledialog.askstring("Sort Array", "Enter numbers to sort (comma-separated):")
        if array_str:
            array = list(map(int, array_str.split(',')))
            sort_process = threading.Thread(target=self.sort_array, args=(array,))
            sort_process.start()

    def sort_array(self, array):
        sorted_array = sorted(array)
        messagebox.showinfo("Sorted Array", f"Original array: {array}\nSorted array: {sorted_array}")

    def add_matrices(self):
        matrix1 = self.get_matrix_input("Enter first matrix as a 2D list (e.g., [[1, 2], [3, 4]]):")
        matrix2 = self.get_matrix_input("Enter second matrix as a 2D list (e.g., [[5, 6], [7, 8]]):")
        if matrix1 is not None and matrix2 is not None:
            if matrix1.shape != matrix2.shape:
                messagebox.showerror("Error", "Matrices must have the same dimensions.")
                return
            result = np.zeros(matrix1.shape)
            threads = []
            for i in range(matrix1.shape[0]):
                thread = threading.Thread(target=self.add_matrix_row, args=(matrix1, matrix2, result, i))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            messagebox.showinfo("Result", f"Resultant Matrix:\n{result}")

    def subtract_matrices(self):
        matrix1 = self.get_matrix_input("Enter first matrix as a 2D list (e.g., [[1, 2], [3, 4]]):")
        matrix2 = self.get_matrix_input("Enter second matrix as a 2D list (e.g., [[5, 6], [7, 8]]):")
        if matrix1 is not None and matrix2 is not None:
            if matrix1.shape != matrix2.shape:
                messagebox.showerror("Error", "Matrices must have the same dimensions.")
                return
            result = np.zeros(matrix1.shape)
            threads = []
            for i in range(matrix1.shape[0]):
                thread = threading.Thread(target=self.subtract_matrix_row, args=(matrix1, matrix2, result, i))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            messagebox.showinfo("Result", f"Resultant Matrix:\n{result}")

    def multiply_matrices(self):
        matrix1 = self.get_matrix_input("Enter first matrix as a 2D list (e.g., [[1, 2], [3, 4]]):")
        matrix2 = self.get_matrix_input("Enter second matrix as a 2D list (e.g., [[5, 6], [7, 8]]):")
        if matrix1 is not None and matrix2 is not None:
            if matrix1.shape[1] != matrix2.shape[0]:
                messagebox.showerror("Error", "Number of columns in the first matrix must be equal to the number of rows in the second matrix.")
                return
            result = np.zeros((matrix1.shape[0], matrix2.shape[1]))
            threads = []
            for i in range(matrix1.shape[0]):
                thread = threading.Thread(target=self.multiply_matrix_row, args=(matrix1, matrix2, result, i))
                threads.append(thread)
                thread.start()
            for thread in threads:
                thread.join()
            messagebox.showinfo("Result", f"Resultant Matrix:\n{result}")

    def get_matrix_input(self, prompt):
        try:
            matrix_str = simpledialog.askstring("Matrix Input", prompt)
            matrix = np.array(eval(matrix_str))
            return matrix
        except Exception as e:
            messagebox.showerror("Error", f"Invalid matrix input. Please try again.\n{e}")
            return None

    def add_matrix_row(self, matrix1, matrix2, result, row):
        result[row] = matrix1[row] + matrix2[row]

    def subtract_matrix_row(self, matrix1, matrix2, result, row):
        result[row] = matrix1[row] - matrix2[row]

    def multiply_matrix_row(self, matrix1, matrix2, result, row):
        result[row] = np.dot(matrix1[row], matrix2)

    def ipc_process_communication(self):
        choice = simpledialog.askstring("IPC Communication", "Do you want the parent process to (write/read)?")
        if choice:
            if choice.lower() == "write":
                parent_write = True
            elif choice.lower() == "read":
                parent_write = False
            else:
                messagebox.showerror("Error", "Invalid choice. Please enter 'write' or 'read'.")
                return

            # Create a pipe
            parent_conn, child_conn = multiprocessing.Pipe()

            # Define the child process function
            def child_process(conn, parent_write):
                if parent_write:
                    conn.send("Hello from Child Process!")
                else:
                    message = conn.recv()
                    print("Child Process received:", message)
                conn.close()

            # Create and start the child process
            p = multiprocessing.Process(target=child_process, args=(child_conn, parent_write))
            p.start()

            if parent_write:
                parent_conn.send("Hello from Parent Process!")
                message = parent_conn.recv()
                messagebox.showinfo("IPC Communication", f"Parent Process received: {message}")
            else:
                message = parent_conn.recv()
                messagebox.showinfo("IPC Communication", f"Parent Process received: {message}")
                parent_conn.send("Hello from Parent Process!")

            parent_conn.close()
            p.join()

class SharedData:
    def __init__(self):
        self.data = None

if __name__ == "__main__":
    YBOS()
