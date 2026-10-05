"""Local credential dialog. Password visibility never implies persistence."""
import tkinter as tk
from tkinter import simpledialog, ttk


class LoginDialog:
    def __init__(self, hidden=False):
        self.root = tk.Tk()
        if hidden:
            self.root.withdraw()
        self.root.title("佳明中国区登录")
        self.root.resizable(False, False)
        self.result = None
        self.email = tk.StringVar(self.root)
        self.password = tk.StringVar(self.root)
        self.visible = tk.BooleanVar(self.root, value=False)
        self.message = tk.StringVar(self.root)

        frame = ttk.Frame(self.root, padding=20)
        frame.grid()
        ttk.Label(frame, text="请输入 Garmin 中国区账号", font=("Microsoft YaHei UI", 12)).grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 12)
        )
        ttk.Label(frame, text="账号邮箱").grid(row=1, column=0, sticky="w", padx=(0, 12))
        self.email_entry = ttk.Entry(frame, textvariable=self.email, width=42)
        self.email_entry.grid(row=1, column=1, pady=5)
        ttk.Label(frame, text="密码").grid(row=2, column=0, sticky="w")
        self.password_entry = ttk.Entry(frame, textvariable=self.password, width=42)
        self.password_entry.grid(row=2, column=1, pady=5)
        ttk.Checkbutton(frame, text="显示密码", variable=self.visible, command=self.update_visibility).grid(
            row=3, column=1, sticky="w", pady=5
        )
        ttk.Label(frame, text="可核对或粘贴密码；密码不会保存到文件。").grid(
            row=4, column=0, columnspan=2, sticky="w", pady=8
        )
        ttk.Label(frame, textvariable=self.message, foreground="#b42318").grid(
            row=5, column=0, columnspan=2, sticky="w"
        )
        ttk.Button(frame, text="登录中国区", command=self.submit).grid(
            row=6, column=0, columnspan=2, sticky="e", pady=(10, 0)
        )
        self.root.bind("<Return>", lambda event: self.submit())
        self.root.protocol("WM_DELETE_WINDOW", self.cancel)
        self.update_visibility()
        self.email_entry.focus_set()

    def update_visibility(self):
        self.password_entry.configure(show="" if self.visible.get() else "*")

    def submit(self):
        email = self.email.get().strip()
        password = self.password.get()
        if not email or not password:
            self.message.set("请填写账号邮箱和密码。")
            return
        # Preserve password spaces and case exactly as entered.
        self.result = (email, password)
        self.email.set("")
        self.password.set("")
        self.root.destroy()

    def cancel(self):
        self.email.set("")
        self.password.set("")
        self.root.destroy()

    def ask(self):
        self.root.mainloop()
        if self.result is None:
            raise KeyboardInterrupt
        return self.result


def ask_credentials():
    return LoginDialog().ask()


def ask_mfa():
    root = tk.Tk()
    root.withdraw()
    try:
        code = simpledialog.askstring("佳明验证码", "请输入佳明刚刚发送的验证码：", parent=root)
    finally:
        root.destroy()
    if code is None:
        raise KeyboardInterrupt
    return code.strip()
