import tkinter as tk
from tkinter import messagebox
from collections import Counter

# Частоты букв в английском языке
english_letter_freq = {
    'E': 12.70, 'T': 9.06, 'A': 8.17, 'O': 7.51, 'I': 6.97, 'N': 6.75,
    'S': 6.33, 'H': 6.09, 'R': 5.99, 'D': 4.25, 'L': 4.03, 'C': 2.78,
    'U': 2.76, 'M': 2.41, 'W': 2.36, 'F': 2.23, 'G': 2.02, 'Y': 1.97,
    'P': 1.93, 'B': 1.49, 'V': 0.98, 'K': 0.77, 'X': 0.15, 'J': 0.15,
    'Q': 0.10, 'Z': 0.07
}

# Функция шифрования Цезаря
def caesar_cipher(text, shift):
    result = ""
    for i in range(len(text)):
        char = text[i]
        if char.isupper():
            result += chr((ord(char) + shift - 65) % 26 + 65)
        elif char.islower():
            result += chr((ord(char) + shift - 97) % 26 + 97)
        else:
            result += char
    return result

# Функция дешифровки
def caesar_decipher(text, shift):
    return caesar_cipher(text, -shift)

# Функция для оценки "правдоподобности" расшифрованного текста
def score_text(text):
    # Считаем частоту каждой буквы в тексте
    text = text.upper()
    letter_count = Counter(filter(str.isalpha, text))
    total_letters = sum(letter_count.values())

    # Если нет букв (например, текст только из символов), возвращаем низкую оценку
    if total_letters == 0:
        return float('-inf')

    # Считаем оценку текста, сравнивая частоты с английским языком
    score = 0
    for letter, count in letter_count.items():
        letter_frequency = (count / total_letters) * 100
        if letter in english_letter_freq:
            score += abs(english_letter_freq[letter] - letter_frequency)

    return score

# Функция для взлома шифра Цезаря с частотным анализом
def caesar_break_smart(text):
    best_shift = 0
    best_score = float('inf')
    best_decryption = ""

    for shift in range(1, 26):
        decrypted_text = caesar_cipher(text, -shift)
        score = score_text(decrypted_text)
        
        # Чем меньше разница в частотах, тем лучше текст
        if score < best_score:
            best_score = score
            best_shift = shift
            best_decryption = decrypted_text

    return best_decryption, best_shift

# Интерфейс приложения
def encrypt_text():
    try:
        text = input_text.get("1.0", tk.END).strip()
        shift = int(shift_entry.get())
        encrypted_text = caesar_cipher(text, shift)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, encrypted_text)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числовое значение сдвига.")

def decrypt_text():
    try:
        text = input_text.get("1.0", tk.END).strip()
        shift = int(shift_entry.get())
        decrypted_text = caesar_decipher(text, shift)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, decrypted_text)
    except ValueError:
        messagebox.showerror("Ошибка", "Введите числовое значение сдвига.")

# Умный взлом шифра с использованием частотного анализа
def break_cipher_smart():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Ошибка", "Введите текст для взлома.")
        return
    decrypted_text, shift = caesar_break_smart(text)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, f"Наиболее вероятный сдвиг: {shift}\nРасшифрованный текст: {decrypted_text}")

# Создаем главное окно
window = tk.Tk()
window.title("Шифр Цезаря")

# Метка для ввода текста
input_label = tk.Label(window, text="Введите текст:")
input_label.pack()

# Поле ввода текста
input_text = tk.Text(window, height=5, width=40)
input_text.pack()

# Метка для ввода сдвига
shift_label = tk.Label(window, text="Введите сдвиг:")
shift_label.pack()

# Поле ввода сдвига
shift_entry = tk.Entry(window)
shift_entry.pack()

# Кнопка для шифрования
encrypt_button = tk.Button(window, text="Зашифровать", command=encrypt_text)
encrypt_button.pack()

# Кнопка для дешифровки
decrypt_button = tk.Button(window, text="Расшифровать", command=decrypt_text)
decrypt_button.pack()

# Кнопка для умного взлома
break_button = tk.Button(window, text="Взломать шифр (умный)", command=break_cipher_smart)
break_button.pack()

# Поле вывода результата
output_label = tk.Label(window, text="Результат:")
output_label.pack()

# Поле вывода текста
output_text = tk.Text(window, height=10, width=40)
output_text.pack()

# Запуск главного цикла
window.mainloop()
