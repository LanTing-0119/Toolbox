import scipy.stats as stats
import numpy as np
import matplotlib as plt

# Generate data points
x = np.linspace(-3, 10, 500)
normal = stats.norm(loc=2, scale=np.sqrt(2)).pdf(x)
poisson = stats.poisson(mu=2).pmf(np.round(x))

# Critical value for alpha = 0.05 in a one-tailed normal test (right tail)
critical_value = stats.norm(loc=2, scale=np.sqrt(2)).ppf(0.95)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(x, normal, label='Normal Distribution (μ=2, σ²=2)', color='blue')
plt.stem(x, poisson, linefmt='orange', markerfmt='ro', basefmt=" ", label='Poisson Distribution (λ=2)', use_line_collection=True)

# Mark critical region
plt.axvline(x=critical_value, color='red', linestyle='--', label=f'Critical value (α=0.05): {critical_value:.2f}')
plt.fill_between(x, 0, normal, where=(x >= critical_value), color='red', alpha=0.2)

# Labels and legend
plt.title("Type I Error Increase: Misusing Normal Instead of Poisson Distribution")
plt.xlabel("Observed Value")
plt.ylabel("Probability Density / Mass")
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()