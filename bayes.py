# Name: Chris Dayal & Joshua Roberts
# Date: 5/11/15
# Description:
#
#

import math, os, pickle, re


class Bayes_Classifier:
   #positive files = 11129
   #positive frequency = 631382
   #percentage positve = 0.8027264858626659
   #percentage of frequencies that are positive = 0.825
   #negative files = 2735
   #negative frequency = 134120
   #percentage negative = 0.1972735141373341
   #percentage of frequencies that are negative = 0.175
   def __init__(self):
      """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
      cache of a trained classifier has been stored, it loads this cache.  Otherwise,
      the system will proceed through training.  After running this method, the classifier
      is ready to classify input text."""
      if os.path.isfile("Positive") and os.path.isfile("Negative"):
         self.positive = self.load("Positive")
         self.negative = self.load("Negative")
      else:
         self.train



   def train(self):
      """Trains the Naive Bayes Sentiment Classifier."""
      IFileList = []
      positive_dict = {}
      negative_dict = {}
      for fFileObj in os.walk("reviews/"):
         IFileList = fFileObj[2]
         break

      for review in IFileList:
         count = 0
         sText = self.loadFile("reviews/" + review)
         word_list = self.tokenize(sText)
         if review[7] == '1':
            for word in word_list:
               if negative_dict.has_key(word):
                  negative_dict[word] = negative_dict[word] + 1
               else:
                  negative_dict[word] = 1
         else:
            for word in word_list:
               if positive_dict.has_key(word):
                  positive_dict[word] = positive_dict[word] + 1
               else:
                  positive_dict[word] = 1
      self.save(positive_dict, "Positive")
      self.save(negative_dict, "Negative")


   def classify_bayes(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      word_list = self.tokenize(sText)
      positive = self.probabilityPositive(word_list)
      negative = self.probabilityNegative(word_list)
      difference = abs(positive-negative)
      print "positive: ", positive
      print "negative: ", negative
      print "difference: ", difference
      if difference < 1:
         return "neutral"
      elif positive > negative:
         return "positive"
      else:
         return "negative"


   def probabilityPositive(self,lst):
      """Determines the probability of a text being positive given a list of the words
      contained in the text given as reference the training document Positive"""
      probability_positive = 0
      positive_features = 0.825
      for word in lst:
         if self.positive.has_key(word):
            probability_positive += math.log((self.positive[word]+1)/float(positive_features))
         else:
            probability_positive += math.log(1/float(positive_features))
      return abs(probability_positive)

   def probabilityNegative(self,lst):
      """Determines the probability of a text being positive given a list of the words
      contained in the text given as reference the training document Positive"""
      probability_negative = 0
      negative_features = 0.175
      for word in lst:
         if self.negative.has_key(word):
            probability_negative += math.log((self.negative[word]+1)/float(negative_features))
         else:
            probability_negative += math.log(1/float(negative_features))
      return abs(probability_negative)


   def loadFile(self, sFilename):
      """Given a file name, return the contents of the file as a string."""
      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt

   def save(self, dObj, sFilename):
      """Given an object and a file name, write the object to the file using pickle."""

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()

   def load(self, sFilename):
      """Given a file name, load and return the object stored in the file."""

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText):
      """Given a string of text sText, returns a list of the individual tokens that
      occur in that string (in order)."""

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))

      if sToken != "":
         lTokens.append(sToken)

      return lTokens
