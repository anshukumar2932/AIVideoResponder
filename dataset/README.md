# Lip Reading Viseme Dataset Creation

## Overview

This project focuses on building a **viseme-based video dataset** from a lip-reading corpus using alignment files and corresponding speaker videos. The goal is to extract short video clips representing different mouth shapes (visemes) associated with spoken words, which can later be used for:

* Talking head / avatar generation
* Speech-driven facial animation
* Lip-sync research
* Multimodal AI experiments

The workflow combines **forced alignment timestamps**, **video processing**, and **computer vision-based lip analysis**.

---

## Dataset Used

The dataset contains:

* `.align` files — word-level timestamps
* Video files — speaker utterances with the same filename stem
* Single speaker recordings
* GRID-style timestamps (1/10000 second units)

Example alignment format:

```
0 23750 sil
23750 29500 bin
29500 34000 blue
34000 35500 at
35500 41000 f
41000 47250 two
47250 53000 now
53000 74500 sil
```

Where:

* First number = start time
* Second number = end time
* Third value = spoken word
* `sil` and `sp` represent silence (ignored)

---

## Step 1 — Vocabulary Extraction

All `.align` files were parsed to:

* Extract unique words across the dataset
* Build file → words mapping
* Remove silence tokens

Result:

* **53 unique words vocabulary**

This vocabulary is later used to guide clip extraction and viseme grouping.

---

## Step 2 — Basic Viseme Mapping

An initial rule-based mapping grouped words into mouth shapes:

* Round lips
* Wide lips
* Closed lips
* Sibilant sounds
* Neutral

Example:

```python
VISeme_MAP = {
    "viseme_round": {"blue", "two", "u", "o", "zero"},
    "viseme_wide": {"three", "e", "green", "please"},
    "viseme_closed": {"bin", "b", "p", "m"},
    "viseme_sibilant": {"six", "seven", "s", "z"},
    "viseme_neutral": {"at", "with", "again", "now", "place", "set", "lay", "white", "red"}
}
```

---

## Step 3 — Clip Extraction Using Alignment

Using `ffmpeg`, video clips were extracted directly from timestamps:

* Alignment timestamps converted from GRID units to seconds
* Corresponding video file matched by filename
* Clips saved into viseme-specific folders

Output structure example:

```
viseme_dataset/
    viseme_round/
    viseme_wide/
    viseme_closed/
    viseme_sibilant/
    viseme_neutral/
```

---

## Step 4 — Advanced AI-Based Lip Analysis

To improve timing accuracy and viseme classification, an advanced pipeline was implemented using:

### MediaPipe Face Mesh

* 468 facial landmarks
* Accurate lip localization
* Real-time performance

### Extracted Lip Features

* Mouth Aspect Ratio (MAR)
* Lip width
* Lip height
* Motion energy between frames
* Temporal articulation scoring

These features allow detection of:

* Peak articulation frame
* Mouth opening phases
* Transition boundaries

---

## Step 5 — Adaptive Window Selection

Instead of fixed timestamps, the system:

1. Scans frames between word start and end
2. Computes articulation score per frame
3. Detects peak mouth motion
4. Expands window around peak using threshold
5. Extracts optimal clip duration (0.25–0.6 sec)

This produces more accurate viseme clips compared to raw alignment slicing.

---

## Step 6 — AI-Based Viseme Classification

A geometry-based AI classifier categorizes mouth shapes into:

* `viseme_closed`
* `viseme_partial`
* `viseme_round`
* `viseme_wide`
* `viseme_open_big`
* `viseme_open_small`
* `viseme_sibilant`
* `viseme_neutral`

This approach avoids the need for training a machine learning model while still achieving good accuracy.

---

## Step 7 — Final Dataset Generation

For each word:

* Up to **3 clips per word** are extracted
* Best articulation window selected
* Clips saved into predicted viseme folder

Final dataset contains:

* Clean lip motion clips
* Organized by mouth shape
* Consistent frame rate and encoding

---

## Technologies Used

* Python
* OpenCV
* MediaPipe FaceMesh
* NumPy
* FFmpeg
* tqdm (progress tracking)

---

## Key Achievements

✅ Extracted vocabulary from alignment files
✅ Built word-to-video indexing system
✅ Implemented automated clip extraction pipeline
✅ Developed geometry-based viseme AI classifier
✅ Created structured viseme dataset from raw videos
✅ Improved timing accuracy using adaptive window detection

---

## Possible Future Improvements

* Deep learning viseme classifier (CNN / Transformer)
* Mouth region cropping dataset
* Real-time talking avatar generation
* Phoneme-to-viseme synthesis engine
* Multi-speaker dataset expansion

---

## Author

Aditya Singh
Project: Lip Reading / Talking Head Dataset Pipeline

---
