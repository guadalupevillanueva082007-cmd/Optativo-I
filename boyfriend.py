import sys
import time

def printLyrics():
    # Tupla con (línea_de_texto, velocidad_por_caracter)
    lines = (
        ("Your boy boy b-b-b-b-b-boyfriend", 0.08),
        ("Your boy boy b-b-b-b-b-boyfriend", 0.08),
        ("Have you ever had the feeling you're drawn to someone?", 0.06),
        ("(Yeah)", 0.10),
        ("And there isn't anything they could have said or done?", 0.05),
        ("And everyday I see you on your own", 0.06),
        ("And I can't believe that you're alone", 0.06),
        ("Looking for a, looking for a...", 0.07),
        ("That you're looking for a boyfriend (yeah)", 0.07),
        ("Is your boyfriend (yeah)", 0.09),
        ("All I really want is to be your...", 0.08),
        ("Your boy boy b-b-b-b-b-boyfriend", 0.08)
    )

    # Tiempos de pausa entre cada línea (en segundos)
    delays = [0.4, 0.5, 0.6, 0.3, 0.5, 0.4, 0.6, 0.5, 0.8, 0.7, 0.6, 1.0]

    try:
        for i, (line, char_delay) in enumerate(lines):
            for char in line:
                print(f"\033[1;37m{char}\033[0m", end="")  # Texto en negrita/blanco
                sys.stdout.flush()
                time.sleep(char_delay)
            print()
            if i < len(delays):
                time.sleep(delays[i])
    finally:
        time.sleep(2)

if __name__ == "__main__":
    printLyrics()