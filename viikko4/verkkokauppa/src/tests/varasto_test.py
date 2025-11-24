import unittest
from unittest.mock import Mock, ANY
from varasto import Varasto
from tuote import Tuote
from kauppa import Kauppa


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.kirjanpito_mock = Mock()
        self.varasto = Varasto(kirjanpito=self.kirjanpito_mock)
        self.pankki_mock = Mock()
        self.viite_mock = Mock()
        self.viite_mock.uusi.return_value = 42

    def test_hae_tuote_ja_saldo(self):
        tuote = self.varasto.hae_tuote(1)
        self.assertIsNotNone(tuote)
        self.assertEqual(tuote.id, 1)
        self.assertEqual(self.varasto.saldo(1), 100)

    def test_hae_tuote_none_for_missing(self):
        self.assertIsNone(self.varasto.hae_tuote(999))

    def test_ota_varastosta_vahentaa_ja_kirjaa(self):
        tuote = self.varasto.hae_tuote(1)
        saldo_ennen = self.varasto.saldo(1)
        self.varasto.ota_varastosta(tuote)
        self.assertEqual(self.varasto.saldo(1), saldo_ennen - 1)
        # varmistetaan että kirjanpitoon lisättiin tapahtuma
        self.kirjanpito_mock.lisaa_tapahtuma.assert_called()
        kutsu_arg = self.kirjanpito_mock.lisaa_tapahtuma.call_args[0][0]
        self.assertIn('otettiin varastosta', kutsu_arg)

    def test_palauta_varastoon_kasvattaa_ja_kirjaa(self):
        tuote = self.varasto.hae_tuote(1)
        saldo_ennen = self.varasto.saldo(1)
        self.varasto.palauta_varastoon(tuote)
        self.assertEqual(self.varasto.saldo(1), saldo_ennen + 1)
        self.kirjanpito_mock.lisaa_tapahtuma.assert_called()
        kutsu_arg = self.kirjanpito_mock.lisaa_tapahtuma.call_args[0][0]
        self.assertIn('palautettiin varastoon', kutsu_arg)

    def test_palautus_ei_riko_uusia_tuoteinstansseja(self):
        # luodaan uusi Tuote-instanssi jolla sama id kuin varastossa
        uusi_tuote = Tuote(1, 'uusi nimi', 999)
        saldo_ennen = self.varasto.saldo(1)
        self.varasto.palauta_varastoon(uusi_tuote)
        # saldon pitää kasvaa yhdellä (samasta id:stä huolimatta)
        self.assertEqual(self.varasto.saldo(1), saldo_ennen + 1)

    def test_ei_varastossa_palauttaa_summan_nolla(self):
        kauppa = Kauppa(self.varasto, self.pankki_mock, self.viite_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(99)  # ei ole varastossa
        kauppa.tilimaksu("integraatio", "000")

        self.pankki_mock.tilisiirto.assert_called_with("integraatio", 42, "000", ANY, 0)

    def test_osto_varastossa_laskee_oikean_summan(self):
        tuote = Tuote(1, "testituote", 10)
        self.varasto.palauta_varastoon(tuote)

        kauppa = Kauppa(self.varasto, self.pankki_mock, self.viite_mock)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("integraatio", "001")

        odotettu = self.varasto.hae_tuote(1).hinta
        self.pankki_mock.tilisiirto.assert_called_with("integraatio", 42, "001", ANY, odotettu)
