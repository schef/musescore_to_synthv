import unittest
from unittest.mock import patch

import mscx_to_svp


class CroatianPhonemeTests(unittest.TestCase):
    def test_final_stops_do_not_add_a_vowel(self):
        with patch.object(mscx_to_svp, "use_hr_dict", True):
            for lyric, expected in [("Kad", "k aa d"), ("sad", "s aa d"), ("put", "p uh t")]:
                with self.subTest(lyric=lyric):
                    self.assertEqual(mscx_to_svp.generate_phonemes(lyric), expected)

    def test_syllabic_r_keeps_its_vowel(self):
        with patch.object(mscx_to_svp, "use_hr_dict", True):
            self.assertEqual(mscx_to_svp.generate_phonemes("prst"), "p ax r s t")

    def test_note_preserves_lyrics_and_corrected_phonemes(self):
        with patch.object(mscx_to_svp, "use_hr_dict", True):
            note = mscx_to_svp.build_note_data(0, mscx_to_svp.ONE_BEAT, "Kad", 60)
            self.assertEqual(note["lyrics"], "Kad")
            self.assertEqual(note["phonemes"], "k aa d")

    def test_continuation_notes_have_no_phoneme_override(self):
        for use_hr_dict in [False, True]:
            with patch.object(mscx_to_svp, "use_hr_dict", use_hr_dict):
                for lyric in ["-", "", None]:
                    with self.subTest(use_hr_dict=use_hr_dict, lyric=lyric):
                        note = mscx_to_svp.build_note_data(mscx_to_svp.ONE_BEAT, mscx_to_svp.ONE_BEAT, lyric, 62)
                        self.assertEqual(note["lyrics"], "-")
                        self.assertEqual(note["phonemes"], "")


if __name__ == "__main__":
    unittest.main()
