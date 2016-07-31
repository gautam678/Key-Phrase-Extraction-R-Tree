# Key-Phrase-Extraction-R-Tree



Key Phrase Extraction using R-Tree is a module written in Python that tells how closely a keyword is related to other keywords in a document.

  - Insert your text files in the transcript and keys folder
  - Run the final_working_model.py program
  - Output is a list of images which gives a histogram of how closely a keyword is associated with others.

### Packages Needed
Key Phrase Extraction using R-Tree uses a number of packages to work properly:
 - Matplotlib - Plotting graphs and histograms
- glob - Used to work with more than one file
- re - Parsing texts
- rtree - Rtree implementation in python
- numpy - for array and data manipulation

### Data
###### Transcript folder -
 This folder contains text files which are scraped from the internet. Usually these files talk about one single topic.
###### keys folder -
This folder contains the list of keywords to the corresponding text files in the transcript folder. They can either be in .key or .txt format.

### Running the code
Navigate to the folder which has the python codes and run

```cmd
python final_working_model.py
```
 This will prompt the main file to run
 
 
### Output Samples
 Once you run the code, the program will generate plots for each keyword in a document. the plots will look something like this
###### Layer -
  
![alt text](https://github.com/gautam678/Key-Phrase-Extraction-R-Tree/blob/master/Images/layer.png)

Here we can see that the Keyword 'Layer' is closely associated with Lipid because this has occured 4 times in the document wherver layer has occured

###### Polar Molecules -
![alt text](https://github.com/gautam678/Key-Phrase-Extraction-R-Tree/blob/master/Images/ploar_molecuke.png)

 Here we can see that the Keyword Polar Molecules is closely associated with 'hexose molecule' because this has occured 4 times in the document wherver layer has occured
