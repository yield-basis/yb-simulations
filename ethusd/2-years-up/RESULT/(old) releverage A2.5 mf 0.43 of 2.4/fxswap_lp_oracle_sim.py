import math


class FXSwapLPOracleSim:
    """Python simulation of FXSwapLPOracle._portfolio_value()."""

    PRECISION = 10**18
    WAD = 10**18
    WAD2 = WAD * WAD
    WAD3 = WAD2 * WAD

    A_PRECISION = 10**4
    MAX_A = 100_000
    MAX_A_RAW = MAX_A * A_PRECISION

    BISECTION_ITERS = 64
    PRICE_TOL_REL = 10**6

    def __init__(self, A: float):
        """
        Args:
            A: Pool amplification coefficient (A_true, not A_raw).
        """
        if A <= 0 or A > self.MAX_A:
            raise ValueError(f"A must be in [1, {self.MAX_A}]")
        self.A = A
        self.A_raw = int(A * self.A_PRECISION)

    def portfolio_value(self, price_oracle: int, price_scale: int) -> int:
        """
        Simulates FXSwapLPOracle._portfolio_value().

        Args:
            price_oracle: pool.price_oracle() (coin0 per coin1, 1e18 precision)
            price_scale: pool.price_scale() (1e18 precision)
        """
        if price_oracle <= 0:
            raise ValueError("price_oracle must be > 0")
        if price_scale <= 0:
            raise ValueError("price_scale must be > 0")

        p_scaled = (price_oracle * self.PRECISION) // price_scale
        return self._portfolio_value(self.A_raw, p_scaled)

    @classmethod
    def _x_from_y(cls, A_raw: int, y: int) -> int:
        b1 = cls.WAD - (4 * A_raw * (cls.WAD - y) // cls.A_PRECISION)
        term = (4 * A_raw * cls.WAD3) // (cls.A_PRECISION * y)
        rad = math.isqrt(b1 * b1 + term)
        if rad <= b1:
            return 0
        return ((rad - b1) * cls.A_PRECISION) // (8 * A_raw)

    @classmethod
    def _p_from_y(cls, A_raw: int, y: int) -> int:
        x = cls._x_from_y(A_raw, y)
        if x == 0:
            return (1 << 256) - 1

        term4a = (4 * A_raw * x) // cls.A_PRECISION
        return ((term4a + cls.WAD3 // (4 * y * y)) * cls.WAD) // (
            term4a + cls.WAD3 // (4 * x * y)
        )

    @classmethod
    def _y_from_bisection(cls, A_raw: int, p: int) -> int:
        if p < cls.WAD:
            raise ValueError("p must be >= WAD for bisection branch")

        lo = cls.WAD // 10**5
        hi = cls.WAD // 2 + 1

        for _ in range(cls.BISECTION_ITERS):
            mid = (lo + hi) // 2
            pm = cls._p_from_y(A_raw, mid)
            tol_abs = p // cls.PRICE_TOL_REL

            if pm > p:
                if pm - p <= tol_abs:
                    return mid
                lo = mid
            else:
                if p - pm <= tol_abs:
                    return mid
                hi = mid

            if hi - lo <= 1:
                return hi

        raise RuntimeError("Didn't converge")

    @classmethod
    def _get_x_y(cls, A_raw: int, p: int) -> tuple[int, int]:
        if A_raw <= 0 or A_raw > cls.MAX_A_RAW:
            raise ValueError(f"A_raw must be in [1, {cls.MAX_A_RAW}]")
        if p == 0:
            raise ValueError("p must be != 0")

        if p < cls.WAD:
            p_inv = (cls.WAD2 + p // 2) // p
            y_inv = cls._y_from_bisection(A_raw, p_inv)
            x_inv = cls._x_from_y(A_raw, y_inv)
            return y_inv, x_inv

        y = cls._y_from_bisection(A_raw, p)
        x = cls._x_from_y(A_raw, y)
        return x, y

    @classmethod
    def _portfolio_value(cls, A_raw: int, p: int) -> int:
        x, y = cls._get_x_y(A_raw, p)
        return x + (p * y) // cls.WAD
