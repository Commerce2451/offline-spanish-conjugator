"""Basic smoke tests for the Offline Spanish Conjugator.

Run from the project folder with:
    python3 -m unittest discover -s tests
"""

import unittest

import app


class TestIrregularOverrides(unittest.TestCase):
    def check_forms(self, verb, tense_title, expected):
        forms = app.IRREGULAR_OVERRIDES[verb][tense_title]
        self.assertEqual(forms, expected)

    def test_ser_present(self):
        self.check_forms("ser", "Present", {
            "1s": "soy", "2s": "eres", "3s": "es",
            "1p": "somos", "2p": "sois", "3p": "son",
        })

    def test_ir_present(self):
        self.check_forms("ir", "Present", {
            "1s": "voy", "2s": "vas", "3s": "va",
            "1p": "vamos", "2p": "vais", "3p": "van",
        })

    def test_tener_subjunctive_present(self):
        self.check_forms("tener", "Subjunctive Present", {
            "1s": "tenga", "2s": "tengas", "3s": "tenga",
            "1p": "tengamos", "2p": "tengáis", "3p": "tengan",
        })

    def test_decir_preterite(self):
        self.check_forms("decir", "Preterite", {
            "1s": "dije", "2s": "dijiste", "3s": "dijo",
            "1p": "dijimos", "2p": "dijisteis", "3p": "dijeron",
        })

    def test_saber_present(self):
        self.check_forms("saber", "Present", {
            "1s": "sé", "2s": "sabes", "3s": "sabe",
            "1p": "sabemos", "2p": "sabéis", "3p": "saben",
        })


class TestRegularHelpers(unittest.TestCase):
    def test_regular_participles(self):
        self.assertEqual(app.past_participle("hablar"), "hablado")
        self.assertEqual(app.past_participle("comer"), "comido")
        self.assertEqual(app.past_participle("vivir"), "vivido")

    def test_regular_gerunds(self):
        self.assertEqual(app.gerund("hablar"), "hablando")
        self.assertEqual(app.gerund("comer"), "comiendo")
        self.assertEqual(app.gerund("vivir"), "viviendo")


if __name__ == "__main__":
    unittest.main()
