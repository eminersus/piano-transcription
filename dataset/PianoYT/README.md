# README PianoYT dataset (May 2020)

This directory contains the PianoYT dataset that is released as part of the ICASSP 2020 paper:

A. S. Koepke, O. Wiles, Y. Moses, A. Zisserman, "Sight to sound: An end-to-end approach for visual piano transcription". In ICASSP 2020

## PianoYT videos
The pianoyt_videos.csv file contains the following columns:
videoID, video url, train/test split, crop

* train/test split is indicated with 1 for train and 3 for test
* The crop occupies 4 columns and is given in the format: (min y, max y, min x, max x)

The video frames were extracted with their native framerate.

## MIDI data
The MIDI data was extracted using:

Hawthorne, C., Elsen, E., Song, J., Roberts, A., Simon, I., Raffel, C., Engel, J., Oore, S. and Eck, D., Onsets and frames: Dual-objective piano transcription. In ISMIR 2018

It can be found in the pianoyt_MIDI folder, with one MIDI file per video (audio_videoID.0.midi, where videoID corresponds to the videoID in the csv file).

## LICENSE
The PianoYT dataset is available to download for commercial/research purposes under a Creative Commons Attribution 4.0 International License. The copyright remains with the original owners of the videos. A complete version of the license can be found in the license.txt provided.
