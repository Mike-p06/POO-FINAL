import numpy as np
import matplotlib.pyplot as plt

# Definir el eje x
x = np.linspace(0, 10, 400)
# Aproximación de f'(x) con una función suave
f_prime = np.sin(x) * np.cos(0.5*x)

# Aproximación de la segunda derivada f''(x)
f_double_prime = np.gradient(f_prime, x)  # Calcula la derivada de f'(x)

# Identificar intervalos de concavidad
concava_abajo = f_double_prime < 0  # Cóncava hacia abajo donde f''(x) < 0
concava_arriba = f_double_prime > 0  # Cóncava hacia arriba donde f''(x) > 0

# Crear la figura
plt.figure(figsize=(8, 5))
plt.axhline(0, color='black', linewidth=1)
plt.axvline(0, color='black', linewidth=1)
plt.plot(x, f_prime, label=r"$f'(x)$", color='purple', linewidth=2)

# Resaltar intervalos de concavidad
plt.fill_between(x, f_prime, where=concava_abajo, color='red', alpha=0.3, label="Cóncava hacia abajo")
plt.fill_between(x, f_prime, where=concava_arriba, color='blue', alpha=0.3, label="Cóncava hacia arriba")

# Etiquetas
plt.xlabel("x")
plt.ylabel(r"$f'(x)$")
plt.title("Concavidad de f(x) basada en f'(x)")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.show()
