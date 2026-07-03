"""
SANDRAY

Module:
    audio.silence

Purpose:
    Detects the end of speech in PCM audio captured by audio.recorder.
"""

import math
import sys
from array import array


class SilenceDetector:
    """Detect sustained silence after speech has started."""

    def __init__(
        self,
        timeout=1.5,
        threshold=300,
        sample_rate=16000,
        sample_width=2,
        speech_start_duration=0.06
    ):
        if timeout <= 0:
            raise ValueError(
                "Silence timeout must be greater than zero."
            )

        if threshold < 0:
            raise ValueError(
                "Silence threshold cannot be negative."
            )

        if sample_rate <= 0:
            raise ValueError(
                "Sample rate must be greater than zero."
            )

        if sample_width != 2:
            raise ValueError(
                "SilenceDetector requires 16-bit PCM audio."
            )

        if speech_start_duration <= 0:
            raise ValueError(
                "Speech start duration must be greater than zero."
            )

        self.threshold = int(threshold)
        self.sample_rate = int(sample_rate)
        self.sample_width = int(sample_width)

        self.required_silence_samples = max(
            1,
            int(round(timeout * sample_rate))
        )

        self.required_speech_samples = max(
            1,
            int(round(speech_start_duration * sample_rate))
        )

        self.speech_detected = False
        self._speech_samples = 0
        self._silence_samples = 0

    def process(self, pcm_data):
        """
        Process one block of signed 16-bit little-endian PCM audio.

        Returns True when speech has started and the configured amount
        of continuous silence has followed it.
        """

        if not pcm_data:
            return False

        if len(pcm_data) % self.sample_width != 0:
            raise ValueError(
                "PCM data is not aligned to 16-bit samples."
            )

        sample_count = len(pcm_data) // self.sample_width
        level = self._rms(pcm_data)

        if not self.speech_detected:
            if level > self.threshold:
                self._speech_samples += sample_count

                if (
                    self._speech_samples
                    >= self.required_speech_samples
                ):
                    self.speech_detected = True
                    self._silence_samples = 0
            else:
                self._speech_samples = 0

            return False

        if level > self.threshold:
            self._silence_samples = 0
            return False

        self._silence_samples += sample_count

        return (
            self._silence_samples
            >= self.required_silence_samples
        )

    @staticmethod
    def _rms(pcm_data):
        samples = array("h")
        samples.frombytes(pcm_data)

        if sys.byteorder != "little":
            samples.byteswap()

        if not samples:
            return 0

        mean_square = sum(
            sample * sample
            for sample in samples
        ) // len(samples)

        return math.isqrt(mean_square)
