# Optativo-I
notas = [7, 4, 9, 6, 3, 8, 10, 5]

# Aprobados (>= 7) con comprensión + filtro
aprobados = [n for n in notas if n >= 7]

# Estadísticas
promedio = sum(notas) / len(notas)
mejor = max(notas)
ordenadas = sorted(notas, reverse=True)

print(f"Aprobados: {aprobados}")
print(f"Promedio: {promedio:.2f}")
print(f"Mejor nota: {mejor}")
print(f"Ranking: {ordenadas}")
