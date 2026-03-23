import math


class FXSwapLPOracleSim:
    """Float simulation of FXSwapLPOracle math (no fixed-point precisions)."""

    MAX_A = 100_000

    BISECTION_ITERS = 128
    PRICE_TOL_REL = 1e-6

    def __init__(self, A: float):
        """
        Args:
            A: Pool amplification coefficient (A_true).
        """
        if A <= 0 or A > self.MAX_A:
            raise ValueError(f"A must be in [1, {self.MAX_A}]")
        self.A = float(A)

        self.ema0_oracle = None
        self.ema0_scale = None

    def get_price(self, method: str, d):
        match method:
            case 'price_oracle':
                return self.from_price_oracle(d['price_oracle'], 1 + d['profit'])
            case 'price_scale':
                return self.from_price_scale(d['price_scale'], 1 + d['profit'])
            case 'actual_portfolio_value':
                return self.actual_portfolio_value([d['token0'], d['token1']], d['price_oracle'], 2e7)
            case 'lp_price':
                return self.lp_price(d['price_oracle'], d['price_scale'], [d['token0'], d['token1']], 2e7)

    def from_price_oracle(self, price_oracle: float, virtual_price: float=1.0):
        return (price_oracle / self.ema0_oracle) ** 0.5 * virtual_price

    def from_price_scale(self, price_scale: float, virtual_price: float=1.0):
        return (price_scale / self.ema0_scale) ** 0.5 * virtual_price

    @classmethod
    def actual_portfolio_value(cls, tokens: list, price_oracle: float, total_supply: float):
        return (tokens[0] + price_oracle * tokens[1]) / total_supply

    def lp_price(self, price_oracle: float, price_scale: float, tokens: list, total_supply: float) -> float:
        p_scaled = price_oracle / price_scale
        balances = self._get_x_y(self.A, p_scaled)

        D = self._get_D(tokens[0], price_scale * tokens[1])

        return (balances[0] + p_scaled * balances[1]) * D / total_supply

    def _get_D(self, x: float, y: float, *, max_iters: int = 255, tol: float = 1e-12) -> float:
        S = x + y
        D = S
        Ann = 4.0 * self.A

        for _ in range(max_iters):
            D_P = D * D / (2.0 * x)
            D_P = D_P * D / (2.0 * y)
            D_next = ((Ann * S + 2.0 * D_P) * D) / ((Ann - 1.0) * D + 3.0 * D_P)
            if abs(D_next - D) <= tol * max(1.0, D_next):
                return D_next
            D = D_next

        raise RuntimeError("D didn't converge")

    @classmethod
    def _x_from_y(cls, A: float, y: float) -> float:
        b1 = 1.0 + 4.0 * A * (y - 1.0)
        term = 4.0 * A / y
        rad = math.sqrt(b1 * b1 + term)
        if rad <= b1:
            return 0.0
        return (rad - b1) / (8.0 * A)

    @classmethod
    def _p_from_y(cls, A: float, y: float) -> float:
        x = cls._x_from_y(A, y)
        if x <= 0:
            return math.inf

        term4a = 4.0 * A
        num = term4a + 1.0 / (4.0 * x * y * y)
        den = term4a + 1.0 / (4.0 * x * x * y)
        return num / den

    @classmethod
    def _y_from_bisection(cls, A: float, p: float) -> float:
        if p < 1.0:
            raise ValueError("p must be >= 1 for bisection branch")

        lo = 1e-12
        hi = 0.5

        for _ in range(cls.BISECTION_ITERS):
            mid = (lo + hi) / 2.0
            pm = cls._p_from_y(A, mid)
            tol_abs = max(p * cls.PRICE_TOL_REL, 1e-15)

            if pm > p:
                if pm - p <= tol_abs:
                    return mid
                lo = mid
            else:
                if p - pm <= tol_abs:
                    return mid
                hi = mid

            if hi - lo <= 1e-15:
                return hi

        raise RuntimeError("Didn't converge")

    @classmethod
    def _get_x_y(cls, A: float, p: float) -> tuple[float, float]:
        if p < 1.0:
            p_inv = 1.0 / p
            y_inv = cls._y_from_bisection(A, p_inv)
            x_inv = cls._x_from_y(A, y_inv)
            return y_inv, x_inv

        y = cls._y_from_bisection(A, p)
        x = cls._x_from_y(A, y)
        return x, y

    @classmethod
    def _portfolio_value(cls, A: float, p: float) -> float:
        x, y = cls._get_x_y(A, p)
        return x + p * y
