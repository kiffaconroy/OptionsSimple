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
    dt = self.T / self.N
    u = math.exp(self.sigma * math.sqrt(dt))
    d = 1.0 / u
    p = (math.exp(self.r * dt) - d) / (u-d)
    ev = 0.0
    for j in range(self.N + 1):
      S_T = self.S * (u ** j) * (d ** (self.N - j))
      if self.putcall == 'call':
        payoff = max(S_T - self.K, 0.0)
      else:
        payoff = max(self.K - S_T, 0.0)
      prob = math.comb(self.N, j) * (p ** j) * ((1-p) ** (self.N - j))
      ev += prob * payoff
    return(ev * math.exp(self.T * (-self.r)))
