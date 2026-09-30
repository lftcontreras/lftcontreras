"""Checagens de unidades e identidades contábeis do exemplo."""
import unittest
from simular import calcular, simular


class TestSimulacao(unittest.TestCase):
    def test_tributo_por_fora_embutido_no_consumo(self):
        # Compra de 120 = base de 100 + tributo de 20.
        self.assertEqual(calcular(1000, 120, .20, .5), (20, 10, 10))

    def test_limites(self):
        self.assertEqual(calcular(1000, 120, 0, 1), (0, 0, 0))
        self.assertEqual(calcular(1000, 120, .20, 1)[2], 0)
        for args in ((0, 120), (1000, -1), (1000, 120, -.1), (1000, 120, .2, 1.1)):
            with self.assertRaises(ValueError):
                calcular(*args)

    def test_identidades_e_elegibilidade(self):
        for linha in simular():
            self.assertAlmostEqual(linha['tributo_bruto'], linha['cashback'] + linha['tributo_liquido'])
            self.assertGreaterEqual(linha['tributo_liquido'], 0)
            if linha['grupo'] > 3:
                self.assertEqual(linha['cashback'], 0)


if __name__ == '__main__':
    unittest.main()
