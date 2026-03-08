import numpy as np
from scipy.stats import norm

def calculate_d1_d2(S,K,T,r,sigma):
    d1=(np.log(S/K)+(r+0.5*sigma**2)*T)/(sigma*np.sqrt(T))
    d2=d1-sigma*np.sqrt(T)
    return d1,d2

def black_scholes_call(S,K,T,r,sigma):
    d1,d2=calculate_d1_d2(S,K,T,r,sigma)
    return S*norm.cdf(d1)-K*np.exp(-r*T)*norm.cdf(d2)

def black_scholes_put(S,K,T,r,sigma):
    d1,d2=calculate_d1_d2(S,K,T,r,sigma)
    return K*np.exp(-r*T)*norm.cdf(-d2)-S*norm.cdf(-d1)

# Greeks
def delta_call(S,K,T,r,sigma):
    d1,_=calculate_d1_d2(S,K,T,r,sigma)
    return norm.cdf(d1)

def gamma(S,K,T,r,sigma):
    d1,_=calculate_d1_d2(S,K,T,r,sigma)
    return norm.pdf(d1)/(S*sigma*np.sqrt(T))

def vega(S,K,T,r,sigma):
    d1,_=calculate_d1_d2(S,K,T,r,sigma)
    return S*norm.pdf(d1)*np.sqrt(T)

def implied_volatility_call(market_price,S,K,T,r,
                            initial_guess=0.2,tolerance=1e-6,max_iterations=100):
    sigma=initial_guess
    for _ in range(max_iterations):
        price=black_scholes_call(S,K,T,r,sigma)
        v=vega(S,K,T,r,sigma)
        diff=price-market_price
        if abs(diff)<tolerance:
            return sigma
        sigma=sigma-diff/v
    return sigma
