WordBoundary
============
AN EXPERIMENT IN THE DETECTION AND
SEGMENTATION OF WORD BOUNDARIES

Introduction

Speech technology has become commonplace due to the steady progress of the technologies computers need to understand and recognize speech. The detection and segmentation of word boundaries are essential for natural language understanding in both humans and computers. In general, words convey semantic units, a direct mapping from the signifier to the signified. More specifically, in prosody, stress and syllables are located at the level of the word containing linguistically rich information and gives rise to studies in phonotactics. For example, the words to produce and the produce, depending on the speaker, contain identical phonemes but distinct prosodic structures – the stress in the former falls on the second syllable, and the stress in the latter falls on the first. This project seeks to experiment with simple techniques in detecting and segmenting word boundaries.

1.1 Previous Studies

Today, large corpora of linguistic data are learned from and probabilistic models (i.e. hidden Markov models) including n-grams, parts-of-speech tagging, and syntactic parsing are used. Vicsi and Szaszák [1] looked at word boundaries in Hungarian and Finnish. In these languages, since the first syllable is always stressed, detecting stress was a very strong indicator for beginnings words. They used a rule-based approach, looking at peaks of the energy within the signal and fundamental frequencies and setting the peaks against a threshold for stress detection. Waheed et al [2] addressed the issue of word boundary detection in quiet and noisy environments. They showed that entropy-based contrasts outperform energy-based algorithms, providing a more efficient way of preprocessing the signal for HMM based schemes. Tsiartas et al [3] found that the accuracy of word boundary detection was relatively poor when primarily looking at acoustic features including short-time energy, short-time zero crossing rate and short-time pitch frequency. They introduced lexical cues and found considerable improvements. Finally and perhaps most influential to this study, Kochanski et al [4] found that fundamental frequency was a poor indicator of stressed syllables, and instead, loudness and duration was much more reliable.

1.2 Current Study

The approach of this study is simple, and will not include the use of probabilistic models and will remain within the time domain; detecting periods of silence will hopefully be a strong indicator of where the words boundaries are – speakers tend to pause between words indicating the sentence and word boundaries. Inverting these intervals will give the locations of the words within the sound signal. The simplicity has both its benefits and its downfalls. On the one hand, it aligns well with the small scope of the project, allows for relatively quick results, and is a straightforward introduction to speech recognition which is known to be a tremendously difficult task. On the other hand, the results will be somewhat inaccurate and this inaccuracy will be a barrier to more in-depth analysis on pitch accents and on the syllabic structures.

1.3 What is a word?

In many writing systems, words are separated by spaces. However, in languages like Chinese, this is not the case, and in these languages especially, how the word is defined is still in debate. One of the reasons refers to the typology of the language in which languages that are highly synthetic, or composed of many morphemes, can convey the same information in one word to, say, ten words in English. Furthermore, free morphemes are those that do not attach to other words and are freestanding and in English, the infinitive is usually represented by to such as to eat or to play. While infinitives are considered two words in English, in other languages, it is not so clear. In philosophy, words represent semantic units, but defining negation not as a word then becomes a problem. Therefore cross-linguistically, there is not a universal definition for a word, and in this experiment, the term word will just mean token, rather than type. This will be important when looking at utterances from a collection of languages.

...

2.3 Methodology

My approach involves basic statistics within the time domain using a sliding window. The biggest obstacle in separating silence periods is noise found within the speech signal – absolute silence in the sound signal will have amplitude of 0, but rarely do speech signals contain absolute silence. Furthermore, the noise level differs from signal to signal, and therefore the implementation must be able account for this. Therefore I looked at formulating a threshold for silence.
