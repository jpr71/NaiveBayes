import math, os, pickle, re, random


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
      #if not (os.path.isfile("Positive_Best") and os.path.isfile("Negative_Best")):
      self.train()
      #self.positive = self.load("Positive_Best")
      #self.negative = self.load("Negative_Best")

   # def train(self):
   #    """Trains the Bayes Sentiment Classifier. Returns metrics to determine correctnes"""
   #    IFileList = []
   #    positive_dict = {}
   #    negative_dict = {}
   #    test_cases = set()
   #    quantity = 0
   #    correct = 0
   #    positive_correct = 0
   #    positive_quantity= 0
   #    negative_correct = 0
   #    negative_quantity= 0
   #    for fFileObj in os.walk("cross_validation/"):
   #       IFileList = fFileObj[2]
   #       break
   #    test = self.pickFile(test_cases)
   #    print "test: ", test
   #    test_cases.add(test)
   #    counter = 0
   #    while quantity < 10:
   #       positive_dict = {}
   #       negative_dict = {}
   #       if os.path.isfile("Positive_Best") and os.path.isfile("Negative_Best"):
   #          os.remove("Positive_Best")
   #          os.remove("Negative_Best")
   #       for review in IFileList:
   #          sText = self.loadFile("cross_validation/" + review)
   #          word_list = self.tokenize(sText)
   #          if not (review[9] == str(test)):
   #             if review[7] == "1":
   #                for word in word_list:
   #                   if negative_dict.has_key(word):
   #                      negative_dict[word] = negative_dict[word] + 1
   #                   else:
   #                      negative_dict[word] = 1
   #             else:
   #                for word in word_list:
   #                   if positive_dict.has_key(word):
   #                      positive_dict[word] = positive_dict[word] + 1
   #                   else:
   #                      positive_dict[word] = 1
   #          else:
   #             print review[9]
   #             print "getting text"
   #             test_text = self.loadFile("cross_validation/"+ review)
   #             sentiment = review[7]
   #       self.save(positive_dict, "Positive_Best")
   #       self.save(negative_dict, "Negative_Best")
   #       self.positive = self.load("Positive_Best")
   #       self.negative = self.load("Negative_Best")
   #       value = self.classify(test_text)
   #       if value == sentiment:
   #          correct += 1
   #          if sentiment == "1":
   #             negative_correct += 1
   #             negative_quantity += 1
   #          else:
   #             positive_correct += 1
   #             positive_quantity += 1
   #       else:
   #          if value == "1":
   #             negative_quantity += 1
   #          else:
   #             positive_quantity += 1
   #       quantity += 1
   #       test = self.pickFile(test_cases)
   #       test_cases.add(test)
   #    print test_cases
   #    return self.results(quantity,correct, positive_correct, negative_correct, positive_quantity, negative_quantity)

   def train(self):
      """Trains the Naive Bayes Sentiment Classifier."""
      IFileList = []
      positive_dict = {}
      negative_dict = {}
      for fFileObj in os.walk("reviews/"):
         IFileList = fFileObj[2]
         break

      for review in IFileList:
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
      self.save(positive_dict, "Positive_Best")
      self.save(negative_dict, "Negative_Best")

   def pickFile(self,tests):
      """ A function that takes a set as an input and randomly picks a file, if the number of the file is
      already in the set, then it picks another file until there are no more files to pick """
      print "pickFile"
      number = random.randint(0,9)
      size = len(tests)
      if size == 10:
         return False
      else:
         while number in tests:
            number = random.randint(0,9)
      return number

   def results(self,quantity, correct, positive, negative, pos_q, neg_q):
      precision_positive = positive/float(pos_q)
      print "Positive Precision: ", precision_positive
      precision_negative = negative/float(neg_q)
      print "Negative Precision: ", precision_negative
      positive_recall = float(positive)/5
      print "Positive Recall: ", positive_recall
      negative_recall = float(negative)/5
      print "Negative Recall: ", negative_recall
      positive_f_measure = (2*precision_positive*positive_recall)/float((precision_positive + positive_recall))
      print "Positive F-Measure: ", positive_f_measure
      negative_f_measure = (2*precision_negative*negative_recall)/float((precision_negative + negative_recall))
      print "Negative F-Measure: ", negative_f_measure




   def classify(self, sText):
      """Given a target string sText, this function returns the most likely document
      class to which the target string belongs (i.e., positive, negative or neutral).
      """
      contrasting_conjunctions = set(["however", "However", "but", "But", "nevertheless", "Nevertheless", "nonetheless", "Nonetheless", "notwithstanding", "Notwithstanding", "despite", "Despite", "spite", "Spite"])
      word_list = self.tokenize(sText)
      positive = self.probabilityPositive(word_list)
      negative = self.probabilityNegative(word_list)
      #difference = abs(positive-negative)
      #print "difference: ", difference
      #if difference < 1:
      # return "neutral"

      # if there's a contrasting conjunction switch the positive and negative values e.g. "This movie had a great plot, great actors BUT it was terrible.".
      for word in word_list:
         if word in contrasting_conjunctions:
            temp = positive
            positive = negative
            negative = temp
      print "positive: ", positive
      print "negative: ", negative
      if positive > negative:
         return "5"
      else:
         return "1"

   def probabilityPositive(self,lst):
      """Determines the probability of a text being positive given a list of the words
      contained in the text given as reference the training document Positive"""
      probability_positive = 0
      positive_features = 0.825
      add_positive = False
      for word in lst:
         if self.positive.has_key(word):
            if add_positive:
               #if there word in front of a not is negative then add the value of the negative to the positive probability, eg. not good = bad
               probability_positive += math.log(2*(self.negative[word]+1)/float(1-positive_features))
            else:
               probability_positive += math.log((self.positive[word]+1)/float(positive_features))
         else:
            probability_positive += math.log(1/float(positive_features))
         add_positive = False
         if word == "not":
            next_word = lst[lst.index(word) + 1]
            result = self.classify(next_word)
            if result == "negative":
               print "in Ppositive"
               add_positive = True
      return abs(probability_positive)

   def probabilityNegative(self,lst):
      """Determines the probability of a text being positive given a list of the words
      contained in the text given as reference the training document Positive"""
      probability_negative = 0
      negative_features = 0.175
      add_negative = False
      for word in lst:
         if self.negative.has_key(word):
            if add_negative:
               #Same as with the positive probability, it assigns the value of a positive feature to the negative probability if there's a not in front of a positive word. eg. not bad = good
               probability_negative += math.log(2*(self.positive[word]+1)/float(1-negative_features))
            else:
               probability_negative += math.log((self.negative[word]+1)/float(negative_features))
         else:
            probability_negative += math.log(1/float(negative_features))
         add_negative = False
         if word == "not":
            next_word = lst[lst.index(word) + 1]
            result = self.classify(next_word)
            if result == "positive":
               print "in pNegative"
               add_negative = True
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
