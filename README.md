## Questions 

## 1. Understand and visualize the dataset

To begin, we want to make `audio_segments.csv` more readable and better understand the distribution of the labels.
Complete the functions in `q1.py` then fill in and run the cells in `visualization.ipynb` under the **Question 1** section.

Looking at `audio_segments.csv`, the labels of each video correspond to the label ID and not the actual label name.

## 2. Download and process the data

Now that we have cleaned the `.csv`, it is time to move on to what really interests us: the audio.
Complete the functions in `q2.py` which will be the building blocks of our small data processing pipeline.
One function should download the audio and the other should cut the audio to include only the segment mentioned in the `.csv`.

## 3. Build the dataset with a pipeline

With these building blocks, we will build a very small data pipeline to download and process the entire dataset.
Complete the functions in `q3.py` then run the cells in `visualize.ipynb`.

## 4. Visualize the audio
Now that the segments are downloaded, complete the cells in `visualize.ipynb` to listen to and visualize some of the audio samples.

# References 
- https://research.google.com/audioset//download.html
- https://regexone.com/ 
