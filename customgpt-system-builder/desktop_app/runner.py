"""Forge Python Runner. Only execute code you trust: it runs with your Windows user permissions."""
import ast, importlib.util, os, subprocess, sys, tempfile, threading, tkinter as tk
from tkinter import filedialog, messagebox, ttk
MAP={"PIL":"Pillow","cv2":"opencv-python","yaml":"PyYAML","sklearn":"scikit-learn","bs4":"beautifulsoup4","dotenv":"python-dotenv","serial":"pyserial"}
STDLIB=getattr(sys,"stdlib_module_names",set())
def imports(src):
 tree=ast.parse(src); names=set()
 for n in ast.walk(tree):
  if isinstance(n,ast.Import): names.update(a.name.split('.')[0] for a in n.names)
  elif isinstance(n,ast.ImportFrom) and n.module: names.add(n.module.split('.')[0])
 return sorted(n for n in names if n not in STDLIB and n!='__future__')
class App(tk.Tk):
 def __init__(self):
  super().__init__();self.title('Forge Python Runner');self.geometry('900x680');self.proc=None
  bar=ttk.Frame(self,padding=10);bar.pack(fill='x');ttk.Label(bar,text='FORGE / PYTHON RUNNER',font=('Segoe UI',15,'bold')).pack(side='left');ttk.Button(bar,text='Открыть .py',command=self.open).pack(side='right');ttk.Button(bar,text='Сохранить',command=self.save).pack(side='right',padx=6)
  ttk.Label(self,text='Интерпретатор: '+sys.executable,padding=10).pack(anchor='w');self.edit=tk.Text(self,font=('Consolas',10),bg='#171721',fg='#d6f0e2',insertbackground='white');self.edit.pack(fill='both',expand=True,padx=10);self.edit.insert('1.0','print("Hello from Forge!")\n')
  row=ttk.Frame(self,padding=10);row.pack(fill='x');ttk.Button(row,text='▶ Запустить',command=self.run).pack(side='left');ttk.Button(row,text='Остановить',command=self.stop).pack(side='left',padx=6);self.status=ttk.Label(row,text='Готово');self.status.pack(side='right');self.out=tk.Text(self,height=9,bg='#09090e',fg='#d5d1e6');self.out.pack(fill='x',padx=10,pady=(0,10));self.path=None
 def log(self,s): self.out.insert('end',s);self.out.see('end')
 def open(self):
  p=filedialog.askopenfilename(filetypes=[('Python','*.py')]);
  if p:
   self.path=p;self.edit.delete('1.0','end');self.edit.insert('1.0',open(p,encoding='utf-8-sig').read())
 def save(self):
  p=self.path or filedialog.asksaveasfilename(defaultextension='.py',filetypes=[('Python','*.py')]);
  if p: open(p,'w',encoding='utf-8').write(self.edit.get('1.0','end-1c'));self.path=p
 def run(self):
  src=self.edit.get('1.0','end-1c')
  try: mods=imports(src)
  except SyntaxError as e: messagebox.showerror('SyntaxError',str(e));return
  missing=[]
  for m in mods:
   try: absent=importlib.util.find_spec(m) is None
   except (ImportError,ValueError): absent=True
   if absent: missing.append(MAP.get(m,m))
  if missing and messagebox.askyesno('Установить библиотеки','pip install '+', '.join(missing)+' ?\nУстанавливай только доверенные пакеты.'):
   p=subprocess.run([sys.executable,'-m','pip','install',*sorted(set(missing))],capture_output=True,text=True);self.log(p.stdout+p.stderr)
   if p.returncode: messagebox.showerror('pip','Установка не удалась');return
  elif missing:return
  path=os.path.join(tempfile.gettempdir(),'forge_user_script.py');open(path,'w',encoding='utf-8').write(src);self.status.config(text='Запуск…')
  def worker():
   self.proc=subprocess.Popen([sys.executable,'-u',path],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace',cwd=os.path.dirname(self.path) if self.path else os.getcwd())
   for line in self.proc.stdout:self.after(0,self.log,line)
   code=self.proc.wait();self.after(0,lambda:self.status.config(text='Завершено: '+str(code)))
  threading.Thread(target=worker,daemon=True).start()
 def stop(self):
  if self.proc and self.proc.poll() is None:self.proc.terminate();self.status.config(text='Остановка…')
if __name__=='__main__':App().mainloop()
