import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pytesseract

# Configurar la ruta de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class OCRApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Extractor de Texto de Imágenes")
        self.root.geometry("800x800")
        self.root.resizable(False, False)
        
        # Contenedor para los botones superiores
        top_frame = tk.Frame(root)
        top_frame.pack(pady=10)

        # Botón para cargar imagen
        self.upload_btn = tk.Button(top_frame, text="Seleccionar Imagen", command=self.cargar_imagen, font=("Arial", 12))
        self.upload_btn.grid(row=0, column=0, padx=10)

        # Botón para comenzar de nuevo
        self.reset_btn = tk.Button(top_frame, text="Comenzar de Nuevo", command=self.reiniciar_interfaz, font=("Arial", 12), state=tk.DISABLED)
        self.reset_btn.grid(row=0, column=1, padx=10)

        # Área para mostrar la imagen seleccionada
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)

        # Etiqueta para el texto extraído
        self.text_label = tk.Label(root, text="Texto Extraído:", font=("Arial", 14))
        self.text_label.pack(pady=5)

        # Cuadro de texto para mostrar el texto extraído
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=15, font=("Arial", 12))
        self.text_area.pack(padx=10, pady=5)

        # Contenedor para los botones inferiores
        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=10)

        # Botón para copiar texto
        self.copy_btn = tk.Button(bottom_frame, text="Copiar Texto Extraído", command=self.copiar_texto, font=("Arial", 12), state=tk.DISABLED)
        self.copy_btn.grid(row=0, column=0, padx=10)

        # Botón para guardar texto
        self.save_btn = tk.Button(bottom_frame, text="Guardar Texto", command=self.guardar_texto, font=("Arial", 12), state=tk.DISABLED)
        self.save_btn.grid(row=0, column=1, padx=10)

        # Variable para la ruta de la imagen
        self.ruta_imagen = ""

    def cargar_imagen(self):
        """
        Permite seleccionar una imagen y extraer texto usando Tesseract OCR.
        """
        try:
            ruta = filedialog.askopenfilename(
                title="Seleccionar Imagen",
                filetypes=[("Archivos de Imagen", "*.jpg *.jpeg *.png *.bmp *.tiff")]
            )
            if not ruta:
                return

            self.ruta_imagen = ruta

            # Mostrar la imagen seleccionada
            img = Image.open(self.ruta_imagen)
            img.thumbnail((400, 300))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.config(image=img_tk)
            self.image_label.image = img_tk

            # Extraer texto con Tesseract OCR
            texto = pytesseract.image_to_string(img, lang="spa")
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, texto)

            # Activar botones relevantes
            self.copy_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    def copiar_texto(self):
        """
        Copia el texto extraído al portapapeles.
        """
        texto = self.text_area.get(1.0, tk.END).strip()
        if texto:
            self.root.clipboard_clear()
            self.root.clipboard_append(texto)
            self.root.update()
            messagebox.showinfo("Copiado", "El texto se copió al portapapeles.")
        else:
            messagebox.showwarning("Sin Texto", "No hay texto para copiar.")

    def guardar_texto(self):
        """
        Guarda el texto extraído en un archivo de texto.
        """
        try:
            texto = self.text_area.get(1.0, tk.END).strip()
            if not texto:
                messagebox.showwarning("Advertencia", "No hay texto para guardar.")
                return

            # Abrir un cuadro de diálogo para seleccionar la ubicación y nombre del archivo
            archivo_guardar = filedialog.asksaveasfilename(
                title="Guardar Texto",
                defaultextension=".txt",
                filetypes=[("Archivos de Texto", "*.txt"), ("Todos los Archivos", "*.*")]
            )

            if not archivo_guardar:
                return  # Si el usuario cancela el guardado, no hacer nada

            with open(archivo_guardar, "w", encoding="utf-8") as archivo:
                archivo.write(texto)
            messagebox.showinfo("Éxito", f"Texto guardado en '{archivo_guardar}'")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

    def reiniciar_interfaz(self):
        """
        Restablece la interfaz a su estado inicial.
        """
        self.text_area.delete(1.0, tk.END)
        self.image_label.config(image="")  # Limpiar la imagen
        self.ruta_imagen = ""
        self.copy_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.DISABLED)
        self.reset_btn.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = OCRApp(root)
    root.mainloop()
