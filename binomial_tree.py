import math
class BinomialTree:
  def __init__(self, S: float, K: float, T: float, r: float, sigma: float, N: int, putcall: str = 'call'):
    self.S = S
    self.K = K
    self.T = T
    self.r = r
    self.sigma = sigma
    self.N = N
    self.putcall = putcall.lower()

  def price(self) -> float:
    """Calc european option price and return"""
    if self.putcall not in ['call', 'put']:
      raise ValueError("must be call or put")

    if self.T <= 0 or self.N <= 0:
      if self.putcall == 'call':
        return max(self.S - self.K, 0.0)
      else:
        return max(self.K - self.S, 0.0)

    dt = self.T / self.N
    u = math.exp(self.sigma * math.sqrt(dt))
    d = 1.0 / u

    if math.isclose(u, d):
      # Deterministic case (e.g. sigma = 0)
      S_T = self.S * math.exp(self.r * self.T)
      if self.putcall == 'call':
        payoff = max(S_T - self.K, 0.0)
      else:
        payoff = max(self.K - S_T, 0.0)
      return payoff * math.exp(-self.r * self.T)

    p = (math.exp(self.r * dt) - d) / (u - d)

    # Initialize terminal payoffs
    payoffs = [0.0] * (self.N + 1)
    for j in range(self.N + 1):
      S_T = self.S * (u ** j) * (d ** (self.N - j))
      if self.putcall == 'call':
        payoffs[j] = max(S_T - self.K, 0.0)
      else:
        payoffs[j] = max(self.K - S_T, 0.0)

    # Work backward
    discount = math.exp(-self.r * dt)
    for i in range(self.N - 1, -1, -1):
      for j in range(i + 1):
        payoffs[j] = (p * payoffs[j + 1] + (1 - p) * payoffs[j]) * discount

    return payoffs[0]

if __name__ == '__main__':
    # Example parameters:
    # S = 100 (Stock Price), K = 100 (Strike Price), T = 1.0 (Time to Maturity in years)
    # r = 0.05 (Risk-free Rate), sigma = 0.2 (Volatility), N = 1000 (Steps)
    tree = BinomialTree(S=100.0, K=121.0, T=0.88, r=0.05, sigma=0.97, N=100, putcall='call')
    print(f"Option Price (Call): {tree.price():.4f}")

